use std::{
    collections::{HashMap, HashSet},
    iter::zip,
    sync::{Arc, Mutex},
};

use anyhow::{bail, Context, Error, Result};
use cached::Cached;
use itertools::Itertools;
use macro_rules_attribute::apply;
use pyo3::exceptions::PyValueError;
use smallvec::SmallVec as Sv;
use thiserror::Error;

use super::{
    circuit_optimizer::{optimize_and_evaluate, OptimizationSettings},
    cumulant::{dim_permutation_for_circuits, partitions},
    get_update::{
        Batcher, IterateMatchResults, IterativeMatcherRc, Matcher, Transform, TransformRc,
    },
    visit_circuit, Add, CircResult, CircuitNode, CircuitRc, CircuitType, Cumulant, DiscreteVar,
    Einsum, GeneralFunction, HashBytes, Index, ScalarConstant,
};
use crate::{
    all_imports::{Shape, Slice, TensorAxisIndex, TensorIndex},
    cached_method,
    py_types::{Tensor, PY_UTILS},
    pyo3_prelude::*,
    python_error_exception,
};

fn count_elements(s: &Shape) -> usize {
    s.iter().product()
}

#[pyfunction]
pub fn default_var_matcher() -> IterativeMatcherRc {
    Matcher::types(vec![CircuitType::DiscreteVar])
        .filter(
            true,
            None,
            None,
            Matcher::types(vec![CircuitType::Cumulant]).into(),
        )
        .into()
}

pub trait SampleSpecTrait {
    /// Like the python method, but modify inplace (via mutex or other interior mutability)
    fn sample_var(&self, d: &DiscreteVar) -> Result<CircuitRc>;
    fn get_empirical_weights(&self) -> CircuitRc;
    fn get_overall_weight(&self) -> CircuitRc {
        ScalarConstant::nrc(
            count_elements(&self.get_sample_shape()) as f64,
            Sv::new(),
            None,
        )
    }
    fn get_sample_shape(&self) -> Shape;
    fn get_transform(self) -> TransformRc
    where
        Self: Sized + Sync + Send + 'static,
    {
        Transform::new_func_err(move |circ| self.sample_var(circ.as_discrete_var_unwrap())).rc()
    }
    fn get_sampler(
        self,
        var_matcher: IterativeMatcherRc,
        default_fancy_validate: bool,
        suffix: Option<String>,
    ) -> Batcher
    where
        Self: Sized + Sync + Send + 'static,
    {
        Batcher::new(
            vec![(var_matcher, self.get_transform())],
            true,
            default_fancy_validate,
            suffix,
        )
    }
}

#[pyclass(subclass, name = "SampleSpec")]
#[derive(Clone, Debug, PyClassDeriv)]
pub struct PySampleSpecBase; // fake sub class, could be made real later if needed

#[pyclass(extends=PySampleSpecBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct RandomSampleSpec {
    #[pyo3(get)]
    shape: Shape,
    #[pyo3(get)]
    replace: bool,
    #[pyo3(get, set)]
    probs_and_group_evaluation_settings: OptimizationSettings,
    // kinda dumb that we use a mutex here. Certainly overkill in a particular sense...
    indices_cache: Arc<Mutex<cached::UnboundCache<HashBytes, Tensor>>>,
}

macro_rules! py_forward_sample_spec {
    ($type:ty) => {
        #[pymethods]
        impl $type {
            #[pyo3(name = "sample_var")]
            fn sample_var_py(&self, d: &DiscreteVar) -> Result<CircuitRc> {
                self.sample_var(d)
            }
            #[pyo3(name = "get_empirical_weights")]
            fn get_empirical_weights_py(&self) -> CircuitRc {
                self.get_empirical_weights()
            }
            #[pyo3(name = "get_overall_weight")]
            fn get_overall_weight_py(&self) -> CircuitRc {
                self.get_overall_weight()
            }
            #[pyo3(name = "get_sample_shape")]
            fn get_sample_shape_py(&self) -> Shape {
                self.get_sample_shape()
            }
            #[pyo3(name = "get_transform")]
            fn get_transform_py(&self) -> TransformRc {
                self.clone().get_transform()
            }
            #[pyo3(name = "get_sampler")]
            #[args(
                var_matcher = "default_var_matcher()",
                default_fancy_validate = "false",
                suffix = "\"sample\".to_owned()"
            )]
            fn get_sampler_py(
                &self,
                var_matcher: IterativeMatcherRc,
                default_fancy_validate: bool,
                suffix: Option<String>,
            ) -> Batcher {
                self.clone()
                    .get_sampler(var_matcher, default_fancy_validate, suffix)
            }
        }

        #[cfg(feature = "real-pyo3")]
        impl $type {
            fn into_init(self) -> PyClassInitializer<Self> {
                (self, PySampleSpecBase).into()
            }
        }

        impl IntoPy<PyObject> for $type {
            fn into_py(self, py: Python<'_>) -> PyObject {
                // this is slightly gross. I wonder if possible to do better?
                // when does this unwrap fail?
                #[cfg(feature = "real-pyo3")]
                {
                    Py::new(py, self.into_init()).unwrap().into_py(py)
                }

                #[cfg(not(feature = "real-pyo3"))]
                unimplemented!()
            }
        }
    };
}

py_forward_sample_spec!(RandomSampleSpec);

#[pymethods]
impl RandomSampleSpec {
    #[new]
    #[args(
        shape = "RandomSampleSpec::default().shape",
        replace = "RandomSampleSpec::default().replace",
        probs_and_group_evaluation_settings = "RandomSampleSpec::default().probs_and_group_evaluation_settings"
    )]
    fn new(
        shape: Shape,
        replace: bool,
        probs_and_group_evaluation_settings: OptimizationSettings,
    ) -> PyClassInitializer<Self> {
        Self {
            shape,
            replace,
            probs_and_group_evaluation_settings,
            ..Default::default()
        }
        .into_init()
    }

    pub fn indices_cache(&self) -> HashMap<HashBytes, Tensor> {
        self.indices_cache.lock().unwrap().get_store().clone()
    }
}

impl RandomSampleSpec {
    fn sample_impl(&self, probs_and_group: CircuitRc) -> Result<Tensor> {
        let key = probs_and_group.info().hash;
        if let Some(out) = self.indices_cache.lock().unwrap().cache_get(&key) {
            return Ok(out.clone());
        }

        let prob_tensor =
            optimize_and_evaluate(probs_and_group, self.probs_and_group_evaluation_settings)
                .context("failed to evaluate prob group")?;
        let out = sample_indices(prob_tensor, self.shape.clone(), self.replace)
            .context("failed to sample indices for discrete var")?;

        self.indices_cache
            .lock()
            .unwrap()
            .cache_set(key, out.clone());
        Ok(out)
    }
}

impl Default for RandomSampleSpec {
    fn default() -> Self {
        RandomSampleSpec {
            shape: Sv::new(),
            replace: true,
            probs_and_group_evaluation_settings: Default::default(),
            indices_cache: Arc::new(Mutex::new(cached::UnboundCache::new())),
        }
    }
}

fn sample_indices(input: Tensor, shape: Shape, replacement: bool) -> Result<Tensor, PyErr> {
    let indices = Python::with_gil(|py| {
        PY_UTILS
            .random_indices
            .call(py, (input, shape.clone(), replacement), None)?
            .extract::<Tensor>(py)
    })?;
    assert_eq!(indices.shape(), &shape);
    Ok(indices)
}
impl SampleSpecTrait for RandomSampleSpec {
    fn sample_var(&self, var: &DiscreteVar) -> Result<CircuitRc> {
        let indices = self
            .sample_impl(var.probs_and_group.clone())?
            .flatten() // flatten here, unflatten via rearrange
            .try_into()
            .unwrap();

        // TODO: use fancier approach when index supports that
        let res = Index::nrc(
            var.values.clone(),
            TensorIndex::new_single(TensorAxisIndex::Tensor(indices), 0, 1),
            None,
        )
        .unflatten_axis(0, self.shape.clone(), None)
        .unwrap()
        .rc();
        Ok(res)
    }
    fn get_empirical_weights(&self) -> CircuitRc {
        ScalarConstant::new(
            1. / count_elements(&self.shape) as f64,
            self.shape.clone(),
            Some("empirical_weights_for_sampled".to_owned()),
        )
        .rc()
    }

    fn get_sample_shape(&self) -> Shape {
        self.shape.clone()
    }
}

#[pyclass(extends=PySampleSpecBase)]
#[derive(Debug, Clone, PyClassDeriv)]
pub struct RunDiscreteVarAllSpec {
    #[pyo3(get)]
    groups: Vec<CircuitRc>,
    #[pyo3(get)]
    subsets: Vec<Slice>,
}

impl RunDiscreteVarAllSpec {
    fn try_new(groups: Vec<CircuitRc>, subsets: Option<Vec<Slice>>) -> Result<Self> {
        if groups.iter().any(|g| g.info().rank() != 1) {
            bail!(SampleError::GroupWithIncorrectNdim { groups })
        }
        if let Some(sub) = &subsets && sub.len() != groups.len() {
            bail!(SampleError::DifferentNumSubsetsThanGroups{subset_len: sub.len(), groups_len: groups.len()})
        }

        Ok(Self {
            groups: groups.clone(),
            subsets: subsets.clone().unwrap_or_else(|| {
                groups
                    .iter()
                    .map(|_| Slice {
                        start: None,
                        stop: None,
                    })
                    .collect()
            }),
        })
    }

    pub fn indexed_groups(&self) -> Vec<CircuitRc> {
        zip(self.groups.clone(), self.subsets.clone())
            .map(|(g, s)| {
                Index::try_new(g, TensorIndex(vec![TensorAxisIndex::Slice(s)]), None)
                    .unwrap()
                    .rc()
            })
            .collect()
    }

    fn get_unnorm_empirical_weights(&self) -> CircuitRc {
        Einsum::new_outer_product(self.indexed_groups(), None, None).rc()
    }
}

py_forward_sample_spec!(RunDiscreteVarAllSpec);

impl Default for RunDiscreteVarAllSpec {
    fn default() -> Self {
        RunDiscreteVarAllSpec {
            groups: vec![],
            subsets: vec![],
        }
    }
}

#[pymethods]
impl RunDiscreteVarAllSpec {
    #[new]
    #[args(subsets = "None")]
    fn py_new(
        groups: Vec<CircuitRc>,
        subsets: Option<Vec<Slice>>,
    ) -> Result<PyClassInitializer<Self>> {
        Self::try_new(groups, subsets).map(Self::into_init)
    }

    #[staticmethod]
    #[args(circuits = "*")]
    fn create_full_from_circuits(circuits: Vec<CircuitRc>) -> Result<Self> {
        let mut discrete_vars_groups: HashSet<CircuitRc> = HashSet::new();
        let mut add_all_groups = |circ: CircuitRc| {
            visit_circuit(circ, |sub| {
                if let Some(var) = sub.as_discrete_var() {
                    discrete_vars_groups.insert(var.probs_and_group.clone());
                } else if sub.is_var() {
                    bail!(SampleError::UnhandledVarError { circ: sub })
                }
                Ok(())
            })
        };

        for c in circuits {
            add_all_groups(c)?;
        }
        Self::try_new(discrete_vars_groups.into_iter().collect_vec(), None)
    }
}

impl SampleSpecTrait for RunDiscreteVarAllSpec {
    fn sample_var(&self, var: &DiscreteVar) -> CircResult {
        let this_group_i = match self
            .groups
            .iter()
            .position(|r| r.clone() == var.probs_and_group)
        {
            Some(g) => g,
            None => {
                return Err(Error::from(SampleError::UnhandledVarError {
                    circ: var.clone().rc(),
                })
                .context("this var wasn't in `groups`"));
            }
        };

        let axes_to_repeat = (0..self.groups.len())
            .filter(|i| *i != this_group_i)
            .collect_vec();

        let mut sampled_values = Index::nrc(
            var.values.clone(),
            TensorIndex(vec![TensorAxisIndex::Slice(self.subsets[this_group_i])]),
            None,
        );

        if axes_to_repeat.len() != 0 {
            let counts = self
                .groups
                .iter()
                .filter(|&g| g != &var.probs_and_group)
                .map(|g| g.info().shape[0])
                .collect();
            sampled_values = sampled_values
                .expand_at_axes(axes_to_repeat, counts, None)
                .unwrap()
                .rc();
        }
        Ok(sampled_values)
    }
    fn get_empirical_weights(&self) -> CircuitRc {
        let all_weights = self.get_unnorm_empirical_weights();
        let all_weights_sum = Einsum::nrc(
            vec![(
                all_weights.clone(),
                Sv::from_iter(0..(all_weights.info().rank() as u8)),
            )],
            Sv::default(),
            None,
        );
        all_weights
            .clone()
            .mul(
                GeneralFunction::new_by_name(vec![all_weights_sum], "reciprocal".to_owned(), None)
                    .unwrap()
                    .rc(),
                None,
            )
            .unwrap()
            .rc()
    }
    fn get_overall_weight(&self) -> CircuitRc {
        Einsum::nrc(
            vec![(
                self.get_unnorm_empirical_weights(),
                Sv::from_iter(0..(self.get_sample_shape().len() as u8)),
            )],
            Sv::default(),
            None,
        )
    }
    fn get_sample_shape(&self) -> Shape {
        self.get_empirical_weights().info().shape.clone()
    }
}

#[derive(FromPyObject, Clone)]
pub enum SampleSpec {
    RandomSampleSpec(RandomSampleSpec),
    RunDiscreteVarAllSpec(RunDiscreteVarAllSpec),
}

impl IntoPy<PyObject> for SampleSpec {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            SampleSpec::RandomSampleSpec(s) => s.into_py(py),
            SampleSpec::RunDiscreteVarAllSpec(s) => s.into_py(py),
        }
    }
}

impl SampleSpec {
    fn as_trait_obj(&self) -> &dyn SampleSpecTrait {
        match self {
            SampleSpec::RandomSampleSpec(s) => s,
            SampleSpec::RunDiscreteVarAllSpec(s) => s,
        }
    }
}

impl SampleSpecTrait for SampleSpec {
    fn sample_var(&self, d: &DiscreteVar) -> CircResult {
        self.as_trait_obj().sample_var(d)
    }
    fn get_empirical_weights(&self) -> CircuitRc {
        self.as_trait_obj().get_empirical_weights()
    }
    fn get_overall_weight(&self) -> CircuitRc {
        self.as_trait_obj().get_overall_weight()
    }
    fn get_sample_shape(&self) -> Shape {
        self.as_trait_obj().get_sample_shape()
    }
}

// type BatchTransform = fn(CircuitRc) -> CircuitRc;

#[pyclass(unsendable)]
#[derive(Clone)]
pub struct SampleTransform {
    // todo: make it respect names
    #[pyo3(get)]
    sampler: Batcher,
    #[pyo3(get)]
    cumulant_matcher: IterativeMatcherRc,
    #[pyo3(get)]
    sample_spec: SampleSpec,
    estimated_cache: cached::UnboundCache<HashBytes, CircuitRc>,
}

// TODO: add more configs/call backs as needed!
// like maybe add some options for automatically setting up compiler batching!
#[pymethods]
impl SampleTransform {
    #[new]
    #[args(
        var_matcher = "default_var_matcher()",
        cumulant_matcher = "Matcher::types(vec![CircuitType::Cumulant]).into()",
        suffix = "\"sample\".to_owned()"
    )]
    fn new(
        sample_spec: SampleSpec,
        var_matcher: IterativeMatcherRc,
        cumulant_matcher: IterativeMatcherRc,
        suffix: Option<String>,
    ) -> Self {
        let sampler = sample_spec.clone().get_sampler(var_matcher, false, suffix);
        Self {
            sampler,
            cumulant_matcher,
            sample_spec,
            estimated_cache: cached::UnboundCache::new(),
        }
    }

    // TODO: add more functions as needed!

    /// recusively estimate all cumulants
    #[pyo3(name = "estimate")]
    fn estimate_py(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        self.estimate(circuit)
    }
    pub fn sample(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        let out = self.sampler.batch(circuit.clone(), None)?;
        let is_orig_shape = out.shape() == circuit.shape();
        let is_sampled_shape = out.shape()
            == &self
                .sample_spec
                .get_sample_shape()
                .iter()
                .chain(circuit.shape())
                .cloned()
                .collect::<Shape>();
        assert!(is_orig_shape || is_sampled_shape);
        if is_orig_shape {
            Ok(out
                .expand_at_axes(
                    (0..self.sample_spec.get_sample_shape().len()).collect(),
                    self.sample_spec.get_sample_shape().into_vec(),
                    None,
                )?
                .rc())
        } else {
            Ok(out)
        }
    }
    pub fn estimate_and_sample(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        let circuit = self.estimate(circuit)?;
        self.sample(circuit)
    }
    pub fn __call__(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        self.estimate_and_sample(circuit)
    }
}

impl SampleTransform {
    fn estimate(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        self.estimate_impl(circuit, self.cumulant_matcher.clone())
    }

    #[apply(cached_method)]
    #[self_id(self_)]
    #[key(circuit.info().hash)]
    #[use_try]
    #[cache_expr(estimated_cache)]
    fn estimate_impl(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
    ) -> Result<CircuitRc> {
        let IterateMatchResults {
            updated,
            finished,
            found,
        } = matcher.match_iterate(circuit.clone())?;
        let mut new_circuit = circuit.clone();

        if !finished {
            let new_matcher = updated.unwrap_or(matcher.clone());
            new_circuit = circuit.map_children(|c| self_.estimate_impl(c, new_matcher.clone()))?;
        }
        if found && let Some(cum) = new_circuit.as_cumulant() {
            new_circuit = self_.estimate_cumulant(cum, matcher)?;
        }

        Ok(new_circuit)
    }

    fn estimate_cumulant(
        &mut self,
        cum: &Cumulant,
        matcher: IterativeMatcherRc,
    ) -> Result<CircuitRc> {
        match cum.nodes.len() {
            0 => Ok(ScalarConstant::new(1., Sv::new(), None).rc()),
            1 => {
                let sampled = self.sample(cum.children().next().unwrap())?;
                self.get_expectation(sampled)
            }
            _ => self.estimate_impl(factored_cumulant_expectation_rewrite(cum), matcher), /* continue with the same matcher */
        }
    }
    fn spec_nb_axes(&self) -> usize {
        self.sample_spec.get_sample_shape().len()
    }
    fn weights_sum(&self) -> CircuitRc {
        let spec_nb_axes = self.spec_nb_axes() as u8;
        Einsum::try_new(
            vec![(
                self.sample_spec.get_empirical_weights(),
                Sv::from_iter(0..spec_nb_axes),
            )],
            Sv::default(),
            None,
        )
        .unwrap()
        .rc()
    }
    fn normed_weights(&self) -> CircuitRc {
        let weight_sum_reciprocal =
            GeneralFunction::new_by_name(vec![self.weights_sum()], "reciprocal".to_owned(), None)
                .unwrap()
                .rc();

        self.sample_spec
            .get_empirical_weights()
            .mul(weight_sum_reciprocal, None)
            .unwrap()
            .rc()
    }

    fn get_expectation(&self, circuit: CircuitRc) -> CircResult {
        let circuit_rank = circuit.info().rank() as u8;
        let spec_nb_axes = self.spec_nb_axes() as u8;
        let name = self.suffix().and_then(|s| {
            circuit
                .name()
                .map(|c_name| format!("{}_{}_expectation", c_name, s))
        });
        Ok(Einsum::try_new(
            vec![
                (self.normed_weights(), Sv::from_iter(0..spec_nb_axes)),
                (circuit, Sv::from_iter(0..circuit_rank)),
            ],
            Sv::from_iter(spec_nb_axes..circuit_rank),
            name,
        )?
        .rc())
    }

    fn suffix(&self) -> Option<&str> {
        self.sampler.suffix()
    }
}

// TODO: maybe split me up. (not v important for the moment)
#[apply(python_error_exception)]
#[base_error_name(Sample)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum SampleError {
    #[error("This var wasn't handled by the corresponding function.")]
    UnhandledVarError { circ: CircuitRc },
    #[error("some probs_and_group has ndim != 1: {groups:?}")]
    GroupWithIncorrectNdim { groups: Vec<CircuitRc> },
    #[error("passed in {subset_len} but {groups_len} groups")]
    DifferentNumSubsetsThanGroups {
        subset_len: usize,
        groups_len: usize,
    },
}

/// Rewrite large cumulant as product and sum of smaller ones
/// Doesn't support nested cumulants
/// source: https://arxiv.org/pdf/1701.05420.pdf
#[pyfunction]
pub fn factored_cumulant_expectation_rewrite(cumulant: &Cumulant) -> CircuitRc {
    let children = cumulant.children().collect_vec();

    if children.len() <= 1 {
        return cumulant.crc();
    }

    let centered_moment = Cumulant::new(vec![centered_product(children.clone())], None).rc();

    let mut sub: Vec<(CircuitRc, f64)> = vec![(centered_moment.clone(), 1.)];

    for p_indexs in partitions(children.len()) {
        let p = p_indexs
            .iter()
            .map(|is| {
                is.iter()
                    .map(|i| (i.clone(), children[*i].clone()))
                    .collect_vec()
            })
            .collect_vec();

        if p.iter().any(|b| b.len() < 2) || p.len() == 1 {
            continue;
        }

        let cumulants = p
            .iter()
            .map(|circuits| {
                Cumulant::new_canon(circuits.iter().map(|(_, c)| c.clone()).collect_vec(), None)
                    .rc()
            })
            .collect_vec();

        let permutation = dim_permutation_for_circuits(
            p,
            cumulants
                .iter()
                .map(|c| c.children().collect_vec())
                .collect_vec(),
            children.len(),
        );

        let new_out = Einsum::new_outer_product(cumulants, None, Some(permutation)).rc();
        sub.push((new_out, -1.));
    }

    Add::from_weighted_list(sub.clone(), false, None)
        .unwrap()
        .rc()
}

fn centered_product(circuits: Vec<CircuitRc>) -> CircuitRc {
    Einsum::new_outer_product(
        circuits.iter().map(|c| center(c.clone())).collect(),
        None,
        None,
    )
    .rc()
}

fn center(c: CircuitRc) -> CircuitRc {
    Add::minus(c.clone(), Cumulant::new(vec![c], None).rc(), None)
        .unwrap()
        .rc()
}

// source: https://stackoverflow.com/questions/19368375/set-partitions-in-python
// fn partition<T>(collection: &Vec<T>) -> Vec<Vec<Vec<T>>>
// where
//     T: Clone,
// {
//     match collection.len() {
//         0 => vec![vec![]],
//         1 => vec![vec![collection.iter().map(|x| x.clone()).collect()]],
//         _ => {
//             let first = collection[0].clone();
//             let mut result = vec![];
//             for smaller in partition(&collection[1..].to_vec()) {
//                 for (n, subset) in smaller.iter().enumerate() {
//                     let mut first_and_subset = vec![first.clone()];
//                     first_and_subset.extend(copy_clonable(&subset));

//                     let e = copy_clonable(
//                         &smaller[..n]
//                             .iter()
//                             .chain(vec![first_and_subset].iter())
//                             .chain(&smaller[(n + 1)..])
//                             .map(|v| copy_clonable(v))
//                             .collect(),
//                     );

//                     result.push(e);
//                 }
//                 let mut first_alone = vec![vec![first.clone()]];
//                 first_alone.extend(smaller);
//                 result.push(first_alone);
//             }

//             result
//         }
//     }
// }

// fn copy_clonable<T>(v: &Vec<T>) -> Vec<T>
// where
//     T: Clone,
// {
//     v.iter().map(|x| x.clone()).collect()
// }

// #[test]
// fn test_partition() {
//     let v = vec![1, 2, 3];
//     let r = partition(&v);
//     assert_eq!(
//         vec![
//             vec![vec![1, 2, 3]],
//             vec![vec![1], vec![2, 3]],
//             vec![vec![1, 2], vec![3]],
//             vec![vec![2], vec![1, 3]],
//             vec![vec![1], vec![2], vec![3]]
//         ],
//         r
//     )
// }
