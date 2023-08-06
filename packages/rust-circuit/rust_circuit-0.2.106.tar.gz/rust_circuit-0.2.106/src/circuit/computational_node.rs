use std::{cmp::Ordering, iter::zip};

use anyhow::{bail, Context, Result};
use itertools::Itertools;
use macro_rules_attribute::apply;
use num_bigint::BigUint;
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use smallvec::SmallVec as Sv;

use super::{
    algebraic_rewrite::{add_deduplicate, add_flatten_once, remove_add_few_input},
    check_canon_axes,
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
    pycall,
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
                bail!(ConstructError::EinsumLenShapeDifferentFromAxes {
                    circuit_name: circ.name_cloned(),
                    circuit_len_shape: circ.info().rank(),
                    len_axes: axes.len(),
                });
            }
            for (&circuit_shape, axis) in circ.info().shape.iter().zip(axes) {
                let existing_shape = *out.entry(*axis).or_insert(circuit_shape);
                if existing_shape != circuit_shape {
                    bail!(ConstructError::EinsumShapeDifferent {
                        circuit_name: circ.name_cloned(),
                        circuit_shape,
                        axis: *axis as usize,
                        existing_shape,
                    });
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

    #[staticmethod]
    #[args(use_1_weights = "false", name = "None")]
    pub fn from_weighted_list(
        nodes_and_weights: Vec<(CircuitRc, f64)>,
        use_1_weights: bool,
        name: Option<String>,
    ) -> Result<Self> {
        let children = nodes_and_weights
            .iter()
            .map(|(node, weight)| {
                if use_1_weights || *weight != 1. {
                    Einsum::scalar_mul(node.to_owned(), *weight, None).rc()
                } else {
                    node.to_owned()
                }
            })
            .collect();
        Self::try_new(children, name)
    }

    #[staticmethod]
    pub fn minus(positive: CircuitRc, negative: CircuitRc, name: Option<String>) -> Result<Self> {
        positive.sub(negative, name)
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
        // spec must be valid because we enforce that on construction!
        // TODO: reduce axes nums!
        let mut out = Self {
            node: node.clone(),
            spec,
            name: Default::default(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);

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

    pub fn unflatten(node: CircuitRc, shape: Shape, name: Option<String>) -> Result<Self> {
        if node.ndim() != 1 {
            bail!(ConstructError::UnflattenButNDimNot1 { ndim: node.ndim() })
        }
        Ok(Rearrange::new(node, RearrangeSpec::unflatten(shape)?, name))
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
            RearrangeSpec::from_einops_string(string)
                .context("failed to construct spec for Rearrange::from_einops_string")?,
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
                    TensorAxisIndex::Tensor(tensor) => {
                        TensorAxisIndex::Tensor(tensor.hashed().try_into().unwrap())
                    }
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

    // TODO: add support for synchronized index construction like python
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

    fn convert_axis(nodes: &[CircuitRc], axis: i64, is_stack: bool) -> Result<usize> {
        if nodes.is_empty() {
            bail!(ConstructError::ConcatZeroNodes {})
        }
        let extra = if is_stack { 1 } else { 0 };
        Ok(check_canon_axes(nodes[0].info().rank() + extra, &[axis])?[0])
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
        axis: i64,
        name: Option<&str>,
    ) -> Result<PyClassInitializer<Concat>> {
        let axis = Self::convert_axis(&nodes, axis, false)?;
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

    pub fn get_sizes_at_axis(&self) -> Vec<usize> {
        self.nodes
            .iter()
            .map(|x| x.info().shape[self.axis])
            .collect()
    }

    #[staticmethod]
    pub fn stack(nodes: Vec<CircuitRc>, axis: i64, name: Option<String>) -> Result<Self> {
        let axis = Self::convert_axis(&nodes, axis, true)?;
        let to_cat = nodes
            .into_iter()
            .map(|c| {
                c.unsqueeze(
                    vec![axis],
                    c.name().map(|s| format!("{}_unsqueeze_stack", s)),
                )
                .map(|x| x.rc())
            })
            .collect::<Result<_>>()
            .context("failed to unsqueeze for stack (axis invalid?)")?;
        Self::try_new(to_cat, axis, name).context("failed to concat for stack after unsqueeze")
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
pub fn flat_concat(circuits: Vec<CircuitRc>) -> Result<Concat> {
    let flatteneds = circuits
        .iter()
        .map(|x| -> Result<_> {
            Ok(Rearrange::try_new(
                x.clone(),
                RearrangeSpec::flatten_usize(x.info().rank())?,
                Some("flatten".to_owned()),
            )
            .unwrap()
            .rc())
        })
        .collect::<Result<_>>()?;
    Ok(Concat::try_new(flatteneds, 0, Some("flat_concat".to_owned())).unwrap())
}

#[pyfunction]
pub fn flat_concat_back(circuits: Vec<CircuitRc>) -> Result<(Concat, Vec<CircuitRc>)> {
    let flat = flat_concat(circuits.clone())?;
    let sections = flat.get_sizes_at_axis();
    let starts = cumsum(&sections);
    let out = (
        flat.clone(),
        zip(circuits, zip(starts, sections))
            .map(|(c, (start, sec))| {
                Ok(Rearrange::nrc(
                    Index::nrc(
                        flat.crc(),
                        TensorIndex(vec![TensorAxisIndex::new_plain_slice(start, start + sec)]),
                        None,
                    ),
                    RearrangeSpec::unflatten(c.info().shape.clone())?,
                    None,
                ))
            })
            .collect::<Result<_>>()?,
    );
    Ok(out)
}

/// input is shape (batch_dims..batch_dims, conv_dims..conv_dims, in_channels)
/// filter is shape (batch_dims_broadcastable_with_input..b,out_channels, conv_dims..conv_dims, in_channels)
/// some features this API can represent aren't actually supported yet bc pytorch
/// doesn't expose all options
/// Batch dims on filter aren't supported yet
/// different padding before and after not supported yet
#[pyclass(unsendable, extends=PyCircuitBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct Conv {
    #[pyo3(get)]
    pub input: CircuitRc,
    #[pyo3(get)]
    pub filter: CircuitRc,
    #[pyo3(get)]
    pub stride: Vec<usize>,
    #[pyo3(get)]
    pub padding: Vec<(usize, usize)>,

    info: CachedCircuitInfo,
    name: Option<String>,
}

impl Conv {
    #[apply(new_rc_unwrap)]
    pub fn try_new(
        input: CircuitRc,
        filter: CircuitRc,
        stride: Vec<usize>,
        padding: Vec<(usize, usize)>,
        name: Option<String>,
    ) -> Result<Self> {
        let dims = stride.len();
        if stride.len() != padding.len() {
            bail!(ConstructError::ConvStridePaddingNotFull {
                stride: stride.len(),
                padding: padding.len(),
            });
        }
        if dims > 3 {
            bail!(ConstructError::NotSupportedYet {
                string: "Conv over more than 3 dims not supported".to_owned(),
            });
        }

        let mut out = Self {
            input,
            filter,
            stride,
            padding,
            name: Default::default(),
            info: Default::default(),
        };
        out.info.shape = out.try_compute_shape()?;
        out.name = out.auto_name(name);
        // todo check not too many axes / oob
        out.init_info()
    }

    pub fn try_compute_shape(&self) -> Result<Shape> {
        let dims = self.dims();
        let input_batch_shape =
            if let Some(input_batch_rank) = self.input.info().rank().checked_sub(dims + 1) {
                Ok::<Shape, ConstructError>(
                    self.input.info().shape[..input_batch_rank]
                        .iter()
                        .cloned()
                        .collect(),
                )
            } else {
                bail!(ConstructError::ConvInputWrongShape {});
            }?;

        let filter_batch_shape =
            if let Some(filter_batch_rank) = self.filter.info().rank().checked_sub(dims + 2) {
                Ok::<Shape, ConstructError>(
                    self.input.info().shape[..filter_batch_rank]
                        .iter()
                        .cloned()
                        .collect(),
                )
            } else {
                bail!(ConstructError::ConvFilterWrongShape {});
            }?;
        let output_batch_shape =
            broadcast_shapes(&vec![input_batch_shape.clone(), filter_batch_shape.clone()])
                .context("input and filter shapes dont broadcast")?;

        if !filter_batch_shape.is_empty() {
            bail!(ConstructError::NotSupportedYet {
                string: format!(
                    "Batch dims on filter aren't supported yet, found {:?}",
                    filter_batch_shape
                ),
            });
        }
        let out_channels = self.filter.info().shape[filter_batch_shape.len()];
        let in_channels = self.filter.info().shape[self.filter.info().rank() - 1];
        if in_channels != self.input.info().shape[self.input.info().rank() - 1] {
            bail!(ConstructError::ConvInputFilterDifferentNumInputChannels {
                filter: in_channels,
                input: self.input.info().shape[self.input.info().rank() - 1],
            });
        }
        let input_conv_shape =
            &self.input.info().shape[input_batch_shape.len()..input_batch_shape.len() + dims];
        let filter_kernel_shape = &self.filter.info().shape
            [self.filter.info().rank() - dims - 1..self.filter.info().rank() - 1];
        let input_conv_shape_padded_minus_edges: Shape =
            zip(input_conv_shape, zip(&self.padding, filter_kernel_shape))
                .map(|(input_l, (padding, kernel_l))| {
                    input_l - (kernel_l - 1) + padding.0 + padding.1
                })
                .collect();
        let new_conv_shape: Shape = zip(&input_conv_shape_padded_minus_edges, &self.stride)
            .map(|(i, s)| {
                if i % s != 0 {
                    Err(ConstructError::ConvStrideMustDivide {
                        shape: input_conv_shape_padded_minus_edges
                            .iter()
                            .cloned()
                            .collect(),
                        stride: self.stride.clone(),
                    })
                    .context("hi")
                } else {
                    Ok(i / s)
                }
            })
            .collect::<Result<Shape>>()?;

        Ok(output_batch_shape
            .into_iter()
            .chain(new_conv_shape)
            .chain(std::iter::once(out_channels))
            .collect())
    }
}

circuit_node_extra_impl!(Conv);

impl CircuitNode for Conv {
    circuit_node_auto_impl!("a329465f-a18f-4313-a2a6-51d8ebad7dd6");

    fn compute_shape(&self) -> Shape {
        self.info().shape.clone()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.input.info().hash);
        hasher.update(&self.filter.info().hash);
        for (i, (j, k)) in zip(&self.stride, &self.padding) {
            hasher.update(&i.to_le_bytes());
            hasher.update(&j.to_le_bytes());
            hasher.update(&k.to_le_bytes());
        }
        hasher
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        Box::new([self.input.clone(), self.filter.clone()].into_iter())
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        // todo: this doesn't state all available axis linkings
        vec![
            (0..self.input_batch_shape().len())
                .map(Some)
                .chain(vec![
                    None;
                    self.input.info().rank()
                        - self.input_batch_shape().len()
                ])
                .collect(),
            vec![None; self.filter.info().rank()],
        ]
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            f(0, self.input.clone())?,
            f(1, self.filter.clone())?,
            self.stride.clone(),
            self.padding.clone(),
            self.name.clone(),
        )
    }

    fn eval_tensors(&self, tensors: &[Tensor], _device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        pycall!(
            PY_UTILS.conv,
            (
                self.dims(),
                tensors[0].clone(),
                tensors[1].clone(),
                self.stride.clone(),
                self.padding.clone(),
            ),
            anyhow
        )
    }

    fn intermediate_cost_bound(&self) -> usize {
        self.info().numel_usize()
    }
}

impl CircuitNodeAutoName for Conv {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| self.input.name().map(|n| "Conv ".to_owned() + n))
    }
}

#[derive(FromPyObject)]
pub enum ConvPaddingShorthand {
    Single(usize),
    Symmetric(Vec<usize>),
    Full(Vec<(usize, usize)>),
}

impl ConvPaddingShorthand {
    pub fn expand(self, l: usize) -> Vec<(usize, usize)> {
        match self {
            ConvPaddingShorthand::Single(single) => vec![(single, single); l],
            ConvPaddingShorthand::Symmetric(sym) => sym.into_iter().map(|s| (s, s)).collect(),
            ConvPaddingShorthand::Full(full) => full,
        }
    }
}

#[pymethods]
impl Conv {
    #[cfg(feature = "real-pyo3")]
    #[new]
    #[args(groups = "1", padding = "ConvPaddingShorthand::Single(0)")]
    fn new_py(
        input: CircuitRc,
        filter: CircuitRc,
        stride: Vec<usize>,
        padding: ConvPaddingShorthand,
        name: Option<String>,
    ) -> PyResult<PyClassInitializer<Conv>> {
        let padding = padding.expand(stride.len());
        let out = Conv::try_new(input, filter, stride, padding, name)?;

        Ok(out.into_init())
    }
    pub fn dims(&self) -> usize {
        self.stride.len()
    }
    pub fn input_batch_shape(&self) -> Shape {
        self.input.info().shape[..self.info().rank() - 1 - self.dims()]
            .iter()
            .cloned()
            .collect()
    }
}
