use std::{cmp::Ordering, iter::zip};

use anyhow::{Context, Result};
use itertools::Itertools;
use macro_rules_attribute::apply;
use num_bigint::BigUint;
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use smallvec::SmallVec as Sv;

use super::{
    algebraic_rewrite::{add_deduplicate, add_flatten_once, remove_add_few_input},
    prelude::*,
    py_circuit_items::PY_CIRCUIT_ITEMS,
    CachedCircuitInfo, ConstructError, PyCircuitBase, ScalarConstant, Shape,
};
use crate::{
    circuit_node_auto_impl,
    circuit_node_extra_impl,
    new_rc_unwrap,
    opt_einsum::EinsumSpec,
    py_types::{
        einops_repeat, einsum_py, make_diagonal_py, scalar_to_tensor, scalar_to_tensor_py,
        ExtraPySelfOps, PyEinsumAxes, Tensor, PY_UTILS,
    },
    pyo3_prelude::*,
    rearrange_spec::RearrangeSpec, // TODO: use new rearrange spec
    sv,
    tensor_util::{
        broadcast_shapes, Slice, TensorAxisIndex, TensorIndex, TorchDeviceDtype, TorchDeviceDtypeOp,
    },
    util::{
        cumsum, dict_to_list, {hashmap_collect_except_duplicates, AxisInt},
    },
};

// we could use u64 instead of u8 if we wanted.
// this is u8, so we want to use multiple of 8 inline so we don't pad
pub type EinsumAxes = Sv<[AxisInt; 8]>;

/// our Einsum supports diag output
/// this means `a->aa` is valid and produces a tensor with the input on the diagonal
/// also `aa->aa` only copies the diagonal, and ignores the rest
#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct Einsum {
    pub args: EinsumArgs,
    pub out_axes: EinsumAxes,
    info: CachedCircuitInfo,
    name: Option<String>,
}

circuit_node_extra_impl!(Einsum);

impl CircuitNode for Einsum {
    circuit_node_auto_impl!("ed15422c-7c02-40c2-a3c2-e9224514d063");

    fn compute_shape(&self) -> Shape {
        let map = self.shape_map().unwrap();
        self.out_axes.iter().map(|a| *map.get(a).unwrap()).collect()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.out_axes);
        for (c, axes) in &self.args {
            // no need to delimit because we have hash each loop
            hasher.update(&c.info().hash);
            hasher.update(axes);
        }

        hasher
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let out_inv: HashMap<AxisInt, usize> = hashmap_collect_except_duplicates(
            self.out_axes.iter().enumerate().map(|(i, x)| (*x, i)),
        );
        self.input_axes()
            .map(|ints| {
                ints.iter()
                    .map(|i| {
                        if ints.iter().filter(|z| *z == i).count() > 1 {
                            return None;
                        }
                        out_inv.get(i).cloned()
                    })
                    .collect()
            })
            .collect()
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(self.args.iter().map(|a| a.0.clone()))
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.args
                .iter()
                .enumerate()
                .map(move |(i, (circ, axes))| -> Result<_> {
                    Ok((f(i, circ.clone())?, axes.clone()))
                })
                .collect::<Result<_, _>>()?,
            self.out_axes.clone(),
            self.name.clone(),
        )
    }

    fn self_flops(&self) -> BigUint {
        self.get_spec().flops()
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            if self.args.is_empty() {
                return Ok(scalar_to_tensor_py(py, 1., sv![], device_dtype.clone())?);
            }
            let out_axes_deduped: EinsumAxes = self.out_axes.iter().unique().cloned().collect();
            let result_non_diag: Tensor = einsum_py(
                py,
                zip(tensors.iter().cloned(), self.input_axes().cloned()).collect(),
                out_axes_deduped.clone(),
            )?;

            if out_axes_deduped.len() != self.out_axes.len() {
                Ok(make_diagonal_py(
                    py,
                    &result_non_diag,
                    out_axes_deduped,
                    self.out_axes.clone(),
                )?)
            } else {
                Ok(result_non_diag)
            }
        })
    }
}

pub type EinsumArgs = Vec<(CircuitRc, EinsumAxes)>;
impl Einsum {
    pub fn input_circuits(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.args.iter().map(|(circ, _)| circ.clone()))
    }

    pub fn input_axes(&self) -> Box<dyn Iterator<Item = &EinsumAxes> + '_> {
        Box::new(self.args.iter().map(|(_, axes)| axes))
    }

    pub fn shape_map(&self) -> Result<HashMap<AxisInt, usize>> {
        let mut out = HashMap::default();
        for (circ, axes) in &self.args {
            if circ.info().rank() != axes.len() {
                return Err(ConstructError::EinsumLenShapeDifferentFromAxes {
                    circuit_name: circ.name_cloned(),
                    circuit_len_shape: circ.info().rank(),
                    len_axes: axes.len(),
                }
                .into());
            }
            for (&circuit_shape, axis) in circ.info().shape.iter().zip(axes) {
                let existing_shape = *out.entry(*axis).or_insert(circuit_shape);
                if existing_shape != circuit_shape {
                    return Err(ConstructError::EinsumShapeDifferent {
                        circuit_name: circ.name_cloned(),
                        circuit_shape,
                        axis: *axis as usize,
                        existing_shape,
                    }
                    .into());
                }
            }
        }

        Ok(out)
    }
    #[apply(new_rc_unwrap)]
    pub fn try_new(args: EinsumArgs, out_axes: EinsumAxes, name: Option<String>) -> Result<Self> {
        // TODO: reduce axes nums!
        let mut out = Self {
            args,
            out_axes,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);

        let map = out.shape_map()?; // catch errors

        for a in &out.out_axes {
            if !map.contains_key(a) {
                return Err(ConstructError::EinsumOutputNotSubset {}.into());
            }
        }

        // could reuse hashmap if helped with perf
        out.init_info()
    }

    pub fn try_from_spec(
        spec: &EinsumSpec,
        circuits: &[CircuitRc],
        name: Option<String>,
    ) -> Result<Self> {
        // TODO: maybe check int sizes!
        assert_eq!(spec.input_ints.len(), circuits.len());
        let to_idx =
            |vals: &[usize]| -> EinsumAxes { vals.iter().map(|&x| x as AxisInt).collect() };
        Self::try_new(
            circuits
                .iter()
                .zip(&spec.input_ints)
                .map(|(c, vals)| (c.clone(), to_idx(vals)))
                .collect(),
            to_idx(&spec.output_ints),
            name,
        )
    }

    pub fn axes_in_input(&self) -> HashSet<AxisInt> {
        // could be 256 bit bitmask
        self.input_axes().flatten().copied().collect()
    }
}

impl CircuitNodeAutoName for Einsum {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.input_circuits().any(|x| x.name().is_none()) {
                None
            } else {
                Some(
                    self.input_circuits()
                        .filter_map(|x| {
                            x.name().map(|y| {
                                if y.len() > 100 {
                                    "...".to_owned()
                                } else {
                                    y.to_owned()
                                }
                            })
                        })
                        .collect::<Vec<String>>()
                        .join(" * "),
                )
            }
        })
    }
}

pub struct PyEinsumArgs(EinsumArgs);

#[cfg(feature = "real-pyo3")]
impl<'source> FromPyObject<'source> for PyEinsumArgs {
    fn extract(args_obj: &'source PyAny) -> PyResult<Self> {
        let args: Vec<(CircuitRc, EinsumAxes)> = args_obj.extract()?;

        Ok(PyEinsumArgs(args.into_iter().collect()))
    }
}

#[cfg(feature = "real-pyo3")]
impl IntoPy<PyObject> for PyEinsumArgs {
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.0
            .into_iter()
            .map(|(c, axes)| (c, PyEinsumAxes(axes)))
            .collect::<Vec<_>>()
            .into_py(py)
    }
}

#[pymethods]
impl Einsum {
    #[cfg(feature = "real-pyo3")]
    #[new]
    #[args(args = "*", out_axes, name)]
    fn new_py(
        args: Vec<(CircuitRc, EinsumAxes)>,
        out_axes: EinsumAxes,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Self>> {
        let out = Self::try_new(args, out_axes, name)?;

        Ok(out.into_init())
    }

    #[staticmethod]
    #[args(nodes = "*", name)]
    pub fn from_einsum_string(
        string: &str,
        nodes: Vec<CircuitRc>,
        name: Option<String>,
    ) -> Result<Self> {
        let (input_ints, output_ints) = EinsumSpec::string_to_ints(string.to_owned());
        Self::try_new(zip(nodes, input_ints).collect(), output_ints, name)
    }

    #[staticmethod]
    #[args(nodes = "*", name)]
    pub fn from_fancy_string(
        string: &str,
        nodes: Vec<CircuitRc>,
        name: Option<String>,
    ) -> Result<Self> {
        let (input_ints, output_ints) = EinsumSpec::fancy_string_to_ints(string.to_owned());
        Self::try_new(zip(nodes, input_ints).collect(), output_ints, name)
    }

    #[staticmethod]
    pub fn new_diag(node: CircuitRc, ints: EinsumAxes, name: Option<String>) -> Self {
        let deduped = ints.iter().unique().cloned().collect();
        Einsum::try_new(vec![(node, deduped)], ints, name).unwrap()
    }

    #[staticmethod]
    pub fn new_trace(node: CircuitRc, ints: EinsumAxes, name: Option<String>) -> Self {
        let deduped = ints.iter().unique().cloned().collect();
        Einsum::try_new(vec![(node, ints)], deduped, name).unwrap()
    }

    #[staticmethod]
    #[args(nodes = "*", name)]
    pub fn from_spec_py(
        spec: EinsumSpec,
        nodes: Vec<CircuitRc>,
        name: Option<String>,
    ) -> Result<Self> {
        Self::try_from_spec(&spec, &nodes, name)
    }

    #[getter]
    fn out_axes(&self) -> PyEinsumAxes {
        PyEinsumAxes(self.out_axes.clone())
    }

    #[getter]
    fn args(&self) -> PyEinsumArgs {
        PyEinsumArgs(self.args.clone())
    }

    fn all_input_circuits(&self) -> Vec<CircuitRc> {
        self.input_circuits().collect()
    }

    fn all_input_axes(&self) -> Vec<PyEinsumAxes> {
        self.input_axes().cloned().map(PyEinsumAxes).collect()
    }

    pub fn reduced_axes(&self) -> HashSet<u8> {
        self.input_axes()
            .flatten()
            .filter(|i| !self.out_axes.contains(i))
            .copied()
            .collect()
    }

    pub fn next_axis(&self) -> u8 {
        self.input_axes()
            .flatten()
            .max()
            .map(|x| x + 1)
            .unwrap_or(0)
    }
    pub fn get_spec(&self) -> EinsumSpec {
        let to_usize = |vals: &[u8]| -> Vec<usize> { vals.iter().map(|&x| x as usize).collect() };
        EinsumSpec {
            input_ints: self.input_axes().map(|x| to_usize(x)).collect(),
            output_ints: to_usize(&self.out_axes),
            int_sizes: dict_to_list(
                &self
                    .shape_map()
                    .unwrap()
                    .iter()
                    .map(|(key, val)| (*key as usize, *val))
                    .collect(),
                None,
            ),
        }
    }
    #[staticmethod]
    pub fn scalar_mul(node: CircuitRc, scalar: f64, name: Option<String>) -> Self {
        let axes: EinsumAxes = (0..node.info().rank()).map(|x| x as u8).collect();
        Einsum::try_new(
            vec![
                (node, axes.clone()),
                (ScalarConstant::new(scalar, sv![], None).rc(), sv![]),
            ],
            axes,
            name,
        )
        .unwrap()
    }
    #[staticmethod]
    #[args(nodes = "*")]
    pub fn elementwise_broadcasted(nodes: Vec<CircuitRc>, name: Option<String>) -> Result<Einsum> {
        let out_shape = broadcast_shapes(&nodes.iter().map(|x| x.info().shape.clone()).collect())
            .context("failed to broadcast for einsum mul")?;
        let mut prev_one_shape = out_shape.len().saturating_sub(1) as u8;
        Einsum::try_new(
            nodes
                .iter()
                .map(|node| {
                    let rank_difference = out_shape.len() - node.info().rank();
                    (
                        node.clone(),
                        node.info()
                            .shape
                            .iter()
                            .enumerate()
                            .map(|(i, l)| {
                                if *l != out_shape[i + rank_difference] {
                                    prev_one_shape += 1;
                                    prev_one_shape
                                } else {
                                    (i + rank_difference) as u8
                                }
                            })
                            .collect(),
                    )
                })
                .collect(),
            (0u8..out_shape.len() as u8).collect(),
            name,
        )
    }
    #[staticmethod]
    pub fn empty(name: Option<String>) -> Self {
        Einsum::try_new(vec![], sv![], name).unwrap()
    }

    #[staticmethod]
    pub fn identity(node: CircuitRc, name: Option<String>) -> Self {
        let axes: EinsumAxes = (0..node.info().rank()).map(|x| x as u8).collect();
        Einsum::try_new(vec![(node, axes.clone())], axes, name).unwrap()
    }

    #[staticmethod]
    pub fn new_outer_product(
        nodes: Vec<CircuitRc>,
        name: Option<String>,
        out_axes_permutation: Option<Vec<usize>>,
    ) -> Self {
        let sections: Vec<_> = nodes.iter().map(|n| n.info().rank()).collect();
        let starts = cumsum(&sections);
        let mut out_axes: EinsumAxes = nodes
            .iter()
            .enumerate()
            .flat_map(|(i, _n)| (starts[i] as u8..(starts[i] + sections[i]) as u8))
            .collect();
        if let Some(permutation) = out_axes_permutation {
            let new_out_axes = permutation.iter().map(|i| out_axes[*i]).collect();
            out_axes = new_out_axes;
        }
        Einsum::try_new(
            nodes
                .iter()
                .enumerate()
                .map(|(i, n)| {
                    (
                        n.clone(),
                        (starts[i] as u8..(starts[i] + sections[i]) as u8).collect(),
                    )
                })
                .collect(),
            out_axes,
            name,
        )
        .unwrap()
    }

    pub fn evolve(&self, args: Option<EinsumArgs>, out_axes: Option<EinsumAxes>) -> Einsum {
        Einsum::try_new(
            args.unwrap_or_else(|| self.args.clone()),
            out_axes.unwrap_or_else(|| self.out_axes.clone()),
            self.name.clone(),
        )
        .unwrap()
    }

    pub fn normalize_ints(&self) -> Einsum {
        let spec = self.get_spec();
        let spec_normalized = spec.normalize();
        Einsum::try_from_spec(
            &spec_normalized,
            &self.input_circuits().collect::<Vec<CircuitRc>>(),
            self.name_cloned(),
        )
        .unwrap()
    }
}

/// Add supports broadcasting
#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct Add {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Add {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, name: Option<String>) -> Result<Self> {
        // TODO: reduce axes nums!
        let mut out = Self {
            nodes,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.compute_shape_maybe()
            .context("Sum isn't broadcastable")?;
        out.init_info()
    }

    pub fn try_from_counts(
        nodes: &HashMap<CircuitRc, usize>,
        name: Option<String>,
    ) -> Result<Self> {
        Self::try_new(
            nodes
                .iter()
                .flat_map(|(circ, &count)| vec![circ.clone(); count])
                .collect(),
            name,
        )
    }

    fn compute_shape_maybe(&self) -> Result<Shape> {
        broadcast_shapes(&self.nodes.iter().map(|x| x.info().shape.clone()).collect())
    }
}

#[pymethods]
impl Add {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn new_py(nodes: Vec<CircuitRc>, name: Option<String>) -> PyResult<PyClassInitializer<Self>> {
        let out = Self::try_new(nodes, name)?;

        Ok(out.into_init())
    }

    pub fn has_broadcast(&self) -> bool {
        !self
            .nodes
            .iter()
            .all(|node| node.info().shape == self.info().shape)
    }

    pub fn nodes_and_rank_differences(&self) -> Vec<(CircuitRc, usize)> {
        self.nodes
            .iter()
            .map(|node| (node.clone(), self.info().rank() - node.info().rank()))
            .collect()
    }

    pub fn flatten_once(&self) -> Self {
        add_flatten_once(self).unwrap_or(self.clone())
    }

    pub fn deduplicate(&self) -> Self {
        add_deduplicate(self).unwrap_or(self.clone())
    }

    pub fn elim_few(&self) -> CircuitRc {
        remove_add_few_input(self).unwrap_or(self.crc())
    }

    pub fn to_counts(&self) -> HashMap<CircuitRc, usize> {
        let mut counts = HashMap::default();
        for item in &self.nodes {
            *counts.entry(item.clone()).or_insert(0) += 1;
        }

        counts
    }
}

circuit_node_extra_impl!(Add);

impl CircuitNode for Add {
    circuit_node_auto_impl!("88fb29e5-c81e-47fe-ae4c-678b22994670");

    fn compute_shape(&self) -> Shape {
        self.compute_shape_maybe().unwrap() // assuming error was caught on creation, panicking now
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        for node in &self.nodes {
            hasher.update(&node.info().hash);
        }

        hasher
    }
    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.nodes_and_rank_differences()
            .iter()
            .map(|(node, rank_difference)| {
                node.info()
                    .shape
                    .iter()
                    .enumerate()
                    .map(|(i, _x)| {
                        if self.info().shape[i + rank_difference] == node.info().shape[i] {
                            Some(i + rank_difference)
                        } else {
                            None
                        }
                    })
                    .collect()
            })
            .collect()
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ.clone()))
                .collect::<Result<Vec<_>, _>>()?,
            self.name.clone(),
        )
    }

    fn self_flops(&self) -> BigUint {
        self.info.numel() * self.nodes.len()
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        if tensors.is_empty() {
            return Ok(scalar_to_tensor(0.0, sv!(), device_dtype.clone())?);
        }
        let mut out = tensors[0].clone();
        Python::with_gil(|py| {
            for tensor in tensors[1..].iter() {
                out = tensor.clone().py_add(py, out.clone()).unwrap();
            }
        });
        Ok(out)
    }
}

impl CircuitNodeAutoName for Add {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.children().any(|x| x.name().is_none()) {
                None
            } else {
                Some(
                    self.children()
                        .filter_map(|x| {
                            x.name().map(|y| {
                                if y.len() > 100 {
                                    "...".to_owned()
                                } else {
                                    y.to_owned()
                                }
                            })
                        })
                        .collect::<Vec<String>>()
                        .join(" + "),
                )
            }
        })
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct Rearrange {
    #[pyo3(get)]
    pub node: CircuitRc,
    #[pyo3(get)]
    pub spec: RearrangeSpec,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Rearrange {
    #[apply(new_rc_unwrap)]

    pub fn try_new(node: CircuitRc, spec: RearrangeSpec, name: Option<String>) -> Result<Self> {
        // TODO: reduce axes nums!
        let mut out = Self {
            node: node.clone(),
            spec,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        if !out.spec.is_valid() {
            return Err(ConstructError::InvalidRearrangeSpec { spec: out.spec }.into());
        }
        // check that known sizes of each axis divide the operand shape
        let input_sizes: Vec<u64> = out
            .spec
            .input_ints
            .iter()
            .map(|x| {
                x.iter()
                    .map(|y| {
                        let s = out.spec.int_sizes[*y as usize];
                        if s.is_none() {
                            1
                        } else {
                            s.unwrap()
                        }
                    })
                    .product()
            })
            .collect();
        let any_sizes_dont_divide = node
            .info()
            .shape
            .iter()
            .enumerate()
            .any(|(i, l)| *l as u64 % input_sizes[i] != 0);

        if input_sizes.len() != node.info().rank() || any_sizes_dont_divide {
            return Err(ConstructError::RearrangeWrongInputShape {
                spec: out.spec,
                shape: node.info().shape.clone(),
            }
            .into());
        }
        out.init_info()
    }

    pub fn evolve(&self, node: Option<CircuitRc>, spec: Option<RearrangeSpec>) -> Rearrange {
        Rearrange::try_new(
            node.unwrap_or_else(|| self.node.clone()),
            spec.unwrap_or_else(|| self.spec.clone()),
            self.name.clone(),
        )
        .unwrap()
    }

    pub fn nrc_elim_identity(
        node: CircuitRc,
        spec: RearrangeSpec,
        name: Option<String>,
    ) -> CircuitRc {
        if spec.is_identity() {
            node
        } else {
            Rearrange::nrc(node, spec, name)
        }
    }
}

circuit_node_extra_impl!(Rearrange);

impl CircuitNode for Rearrange {
    circuit_node_auto_impl!("13204d30-2f12-4edd-8765-34bc8b458ef2");

    fn compute_shape(&self) -> Shape {
        self.spec
            .conform_to_input_shape(&self.node.info().shape, false)
            .unwrap()
            .shapes()
            .unwrap()
            .1
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.node.info().hash);
        hasher.update(&self.spec.compute_hash());
        hasher
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![self
            .spec
            .input_ints
            .iter()
            .map(|ints| {
                if ints.len() != 1 {
                    return None;
                }
                self.spec.output_ints.iter().position(|z| z == ints)
            })
            .collect()]
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.node.clone())?,
            self.spec.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        einops_repeat(
            &tensors[0],
            self.spec.to_einops_string(false),
            self.spec.letter_sizes(),
        )
    }

    fn intermediate_cost_bound(&self) -> usize {
        // Most rearranges are free, but some involve a copy
        //
        // Cases include:
        // 1. Flattening axes out of order: a b -> (b a) is a copy unless either dimension is a singleton
        // 2. Flattening a repeat: a -> (a 2) is a copy
        // 3. Flattening a view with an offset/repeat:
        //    * If x = ones(4,4) and y = x[:, 1:] and z = repeat(y, 'a b -> (a b)'), z is a copy
        //    * If x = ones(4) and y = repeat(x, 'a -> 2 a') and z = repeat(y, 'a b -> (a b)'), z is a copy
        //
        // Because of the third case, we cannot confirm that a rearrange returns a view
        // and has cost 0 unless we have the stride and offset of the child nodes
        //
        // Thus, for now, we always return the upper bound cost of numel. We'll explicitly
        // track and propagate strides alongside shapes later to optimize this
        if self.spec.output_ints.iter().any(|x| x.len() > 1) {
            self.info().numel_usize()
        } else {
            // some flattens / repeats dont need copy, but we'd need stride to know that
            0
        }
    }
}

impl CircuitNodeAutoName for Rearrange {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| self.node.name().map(|n| "rearrange ".to_owned() + n))
    }
}

#[pymethods]
impl Rearrange {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn new_py(
        node: CircuitRc,
        spec: RearrangeSpec,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Self>> {
        let out = Rearrange::try_new(node, spec, name)?;

        Ok(out.into_init())
    }

    #[staticmethod]
    pub fn from_einops_string(node: CircuitRc, string: &str, name: Option<String>) -> Result<Self> {
        Rearrange::try_new(
            node,
            RearrangeSpec::from_einops_string(string).ok_or(
                ConstructError::RearrangeStringInvalid {
                    string: string.to_owned(),
                },
            )?,
            name,
        )
    }

    pub fn conform_to_input_shape(&self, coerce: bool) -> Result<Self> {
        Ok(Rearrange::try_new(
            self.node.clone(),
            self.spec
                .conform_to_input_shape(&self.node.info().shape.clone(), coerce)
                .unwrap(),
            None,
        )
        .unwrap())
    }
}

/// Index indexes a node dimwise.
/// each axis can be Int, Slice, or 1-d tensor
/// and each 1-d tensor is iterated independently, unlike torch or numpy
/// tensor indices which are iterated together.

#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct Index {
    #[pyo3(get)]
    pub node: CircuitRc,
    #[pyo3(get, name = "idx")]
    pub index: TensorIndex,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Index {
    #[apply(new_rc_unwrap)]
    pub fn try_new(node: CircuitRc, index: TensorIndex, name: Option<String>) -> Result<Self> {
        let mut index = index;
        let node_rank = node.info().rank();
        match index.0.len().cmp(&node_rank) {
            Ordering::Greater => {
                return Err(ConstructError::IndexRankTooHigh {
                    index_rank: index.0.len(),
                    node_rank,
                }
                .into());
            }
            Ordering::Less => index.0.extend(vec![
                TensorAxisIndex::Slice(Slice {
                    start: None,
                    stop: None
                });
                node_rank - index.0.len()
            ]),
            _ => {}
        }

        let index = TensorIndex(
            index
                .0
                .into_iter()
                .map(|x| match x {
                    TensorAxisIndex::Tensor(tensor) => TensorAxisIndex::Tensor(tensor.hashed()),
                    _ => x,
                })
                .collect(),
        );

        index.validate(&node.info().shape)?;

        let mut out = Self {
            node,
            index,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }
}

circuit_node_extra_impl!(Index);

impl CircuitNode for Index {
    circuit_node_auto_impl!("3c655670-b352-4a5f-891c-0d7160609341");

    fn compute_shape(&self) -> Shape {
        self.index.apply_to_shape(&self.node.info().shape)
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.node.info().hash);
        hasher.update(&self.index.compute_hash());
        hasher
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let mut cur: i32 = -1;
        let result = vec![zip(&self.node.info().shape, &self.index.0)
            .map(|(l, idx)| {
                if !matches!(idx, TensorAxisIndex::Single(_)) {
                    cur += 1;
                }
                if idx.is_identity(*l) {
                    Some(cur as usize)
                } else {
                    None
                }
            })
            .collect()];
        result
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.node.clone())?,
            self.index.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            PY_CIRCUIT_ITEMS
                .circ_compiler_util
                .getattr(py, "IndexUtil")
                .unwrap()
                .getattr(py, "apply_dimwise")
                .unwrap()
                .call(py, (tensors[0].clone(), self.index.clone()), None)
                .map_err(|err| err.into())
                .map(|x| x.extract(py).unwrap())
        })
    }

    fn intermediate_cost_bound(&self) -> usize {
        // Index returns a view if all of the axis indices are not int tensors
        let has_tensor = self
            .index
            .0
            .iter()
            .any(|x| matches!(x, TensorAxisIndex::Tensor(_)));

        if has_tensor {
            // It might still return a view with int tensors in some cases, but we don't handle this
            self.info().numel_usize()
        } else {
            0
        }
    }

    fn device_dtype_extra<'a>(&'a self) -> Box<dyn Iterator<Item = TorchDeviceDtypeOp> + 'a> {
        Box::new(self.index.0.iter().filter_map(|x| match x {
            TensorAxisIndex::Tensor(tensor) if !tensor.shape().is_empty() => {
                let mut out: TorchDeviceDtypeOp = TorchDeviceDtype::from_tensor(tensor).into();
                out.dtype = None;
                Some(out)
            }
            _ => None,
        }))
    }
}

impl CircuitNodeAutoName for Index {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| self.node.name().map(|n| "idx ".to_owned() + n))
    }
}

#[pymethods]
impl Index {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn new_py(
        node: CircuitRc,
        index: TensorIndex,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Index>> {
        let out = Index::try_new(node, index, name)?;

        Ok(out.into_init())
    }

    pub fn slice_edges_to_none(&self) -> Self {
        Index::try_new(
            self.node.clone(),
            TensorIndex(
                zip(&self.index.0, &self.node.info().shape)
                    .map(|(ax, l)| match ax {
                        TensorAxisIndex::Slice(slice) => TensorAxisIndex::Slice(Slice {
                            start: if slice.start_u(*l) == 0 {
                                None
                            } else {
                                slice.start
                            },
                            stop: if slice.stop_u(*l) == *l {
                                None
                            } else {
                                slice.stop
                            },
                        }),
                        _ => ax.clone(),
                    })
                    .collect(),
            ),
            self.name_cloned(),
        )
        .unwrap()
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone)]
pub struct Concat {
    pub nodes: Vec<CircuitRc>,
    pub axis: usize,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Concat {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, axis: usize, name: Option<String>) -> Result<Self> {
        if nodes.is_empty() {
            return Err(ConstructError::ConcatZeroNodes {}.into());
        }
        let node_shape = &nodes[0].info().shape;
        for node in nodes.iter() {
            for (i, s) in node.info().shape.iter().enumerate() {
                if i != axis && *s != node_shape[i] {
                    return Err(ConstructError::ConcatShapeDifferent {
                        shapes: nodes.iter().map(|x| x.info().shape.clone()).collect(),
                    }
                    .into());
                }
            }
        }

        let mut out = Self {
            nodes,
            axis,
            info: Default::default(),
            name: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }
}

circuit_node_extra_impl!(Concat);

impl CircuitNode for Concat {
    circuit_node_auto_impl!("f2684583-c215-4f67-825e-6e4e51091ca7");

    fn compute_shape(&self) -> Shape {
        let mut shape = self.nodes[0].info().shape.clone();
        shape[self.axis] = self.nodes.iter().map(|n| n.info().shape[self.axis]).sum();
        shape
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        for node in &self.nodes {
            hasher.update(&node.info().hash);
        }
        hasher.update(&self.axis.to_le_bytes());
        hasher
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ.clone()))
                .collect::<Result<Vec<_>, _>>()?,
            self.axis,
            self.name.clone(),
        )
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![
            (0..self.info().rank())
                .map(|i| match i == self.axis {
                    true => None,
                    false => Some(i),
                })
                .collect();
            self.nodes.len()
        ]
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            PY_UTILS
                .torch
                .getattr(py, "cat")
                .unwrap()
                .call(py, (tensors.to_vec(), self.axis), None)
                .map_err(|err| err.into())
                .map(|x| x.extract(py).unwrap())
        })
    }
}

impl CircuitNodeAutoName for Concat {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.children().any(|x| x.name().is_none()) {
                None
            } else {
                Some(
                    self.children()
                        .filter_map(|x| {
                            x.name().map(|y| {
                                if y.len() > 100 {
                                    "...".to_owned()
                                } else {
                                    y.to_owned()
                                }
                            })
                        })
                        .collect::<Vec<String>>()
                        .join(" ++ "),
                )
            }
        })
    }
}

#[pymethods]
impl Concat {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn new_py(
        nodes: Vec<CircuitRc>,
        axis: usize,
        name: Option<&str>,
    ) -> PyResult<PyClassInitializer<Concat>> {
        let out = Self::try_new(nodes, axis, name.map(str::to_owned))?;

        Ok(out.into_init())
    }

    #[getter]
    fn nodes(&self) -> Vec<CircuitRc> {
        self.nodes.to_vec()
    }

    #[getter]
    fn axis(&self) -> usize {
        self.axis
    }

    pub fn get_sections(&self) -> Vec<usize> {
        self.nodes
            .iter()
            .map(|x| x.info().shape[self.axis])
            .collect()
    }
}

/// Scatter is equivelent to:
/// result = torch.zeros(shape)
/// result[index] = node.evaluate()
/// but index is considered dimwise
///
/// right now rewrites only work with slices, maybe will support others later
#[pyclass(extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct Scatter {
    #[pyo3(get)]
    pub node: CircuitRc,
    #[pyo3(get, name = "idx")]
    pub index: TensorIndex,
    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Scatter {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        node: CircuitRc,
        index: TensorIndex,
        shape: Shape,
        name: Option<String>,
    ) -> Result<Self> {
        let index_shape = index.apply_to_shape(&shape);
        if index.all_uslices().is_none() {
            return Err(ConstructError::ScatterIndexTypeUnimplemented { index }.into());
        }
        if index_shape[..] != node.info().shape[..] {
            return Err(ConstructError::ScatterShapeWrong {
                shape,
                index,
                index_shape,
            }
            .into());
        }

        let mut out = Self {
            node,
            index,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.info.shape = shape;
        // todo check not too many axes / oob
        out.init_info()
    }
}

circuit_node_extra_impl!(Scatter);

impl CircuitNode for Scatter {
    circuit_node_auto_impl!("50cce6d3-457c-4f52-9a23-1903bdc76533");

    fn compute_shape(&self) -> Shape {
        self.info().shape.clone()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.node.info().hash);
        hasher.update(&self.index.compute_hash());
        for i in &self.info().shape {
            hasher.update(&i.to_le_bytes());
        }
        hasher
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new(std::iter::once(self.node.clone()))
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        let mut cur: i32 = -1;
        vec![zip(&self.info().shape, &self.index.0)
            .enumerate()
            .map(|(i, (l, idx))| {
                if !matches!(idx, TensorAxisIndex::Single(_)) {
                    cur += 1;
                }
                if idx.is_identity(*l) {
                    Some(i as usize)
                } else {
                    None
                }
            })
            .collect()]
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.node.clone())?,
            self.index.clone(),
            self.info().shape.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        Python::with_gil(|py| {
            PY_CIRCUIT_ITEMS
                .circ_compiler_util
                .getattr(py, "ScatterFn")
                .unwrap()
                .call(py, (self.index.clone(), self.info().shape.clone()), None)
                .unwrap()
                .call(py, (tensors[0].clone(),), None)
                .map_err(|err| err.into())
                .map(|x| x.extract(py).unwrap())
        })
    }

    fn intermediate_cost_bound(&self) -> usize {
        self.info().numel_usize()
    }
}

impl CircuitNodeAutoName for Scatter {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| self.node.name().map(|n| "scatter ".to_owned() + n))
    }
}

#[pymethods]
impl Scatter {
    #[cfg(feature = "real-pyo3")]
    #[new]
    fn new_py(
        node: CircuitRc,
        index: TensorIndex,
        shape: Shape,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Scatter>> {
        let out = Scatter::try_new(node, index, shape, name)?;

        Ok(out.into_init())
    }

    pub fn is_identity(&self) -> bool {
        self.info().shape[..] == self.node.info().shape[..] && self.index.all_uslices().is_some()
    }
}

#[pyfunction]
pub fn flat_concat(circuits: Vec<CircuitRc>) -> Concat {
    let flatteneds = circuits
        .iter()
        .map(|x| {
            Rearrange::try_new(
                x.clone(),
                RearrangeSpec::flatten(x.info().rank()),
                Some("flatten".to_owned()),
            )
            .unwrap()
            .rc()
        })
        .collect();
    Concat::try_new(flatteneds, 0, Some("flat_concat".to_owned())).unwrap()
}

#[pyfunction]
pub fn flat_concat_back(circuits: Vec<CircuitRc>) -> (Concat, Vec<CircuitRc>) {
    let flat = flat_concat(circuits.clone());
    let sections = flat.get_sections();
    let starts = cumsum(&sections);
    (
        flat.clone(),
        zip(circuits, zip(starts, sections))
            .map(|(c, (start, sec))| {
                Rearrange::nrc(
                    Index::nrc(
                        flat.crc(),
                        TensorIndex(vec![TensorAxisIndex::new_plain_slice(start, start + sec)]),
                        None,
                    ),
                    RearrangeSpec::unflatten(c.info().shape.clone()),
                    None,
                )
            })
            .collect(),
    )
}
