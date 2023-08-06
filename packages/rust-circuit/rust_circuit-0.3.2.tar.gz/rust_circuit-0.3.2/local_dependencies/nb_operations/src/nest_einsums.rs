use std::vec;

use anyhow::{bail, Context, Result};
use circuit_base::{computational_node::EinsumArgs, CircuitNode, CircuitRc, Einsum};
use circuit_rewrites::algebraic_rewrite::make_einsum_ints_same_one_layer;
use get_update_node::{IterativeMatcher, IterativeMatcherRc, MatcherRc};
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, prelude::*};
use rr_util::{
    python_error_exception,
    rearrange_spec::{check_permutation, PermError},
    util::{flip_result_op, is_unique, AxisInt, EinsumAxes},
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use thiserror::Error;

#[pyclass]
#[derive(Clone, Debug)]
pub struct NestEinsumsRest {
    #[pyo3(get, set)]
    pub flat: bool,
}

#[pymethods]
impl NestEinsumsRest {
    #[new]
    #[args(flat = "false")]
    pub fn new(flat: bool) -> Self {
        Self { flat }
    }
}

#[derive(Clone, Debug, FromPyObject, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub enum IntOrMatcher {
    Int(usize),
    Matcher(MatcherRc),
}

#[derive(Clone, Debug, FromPyObject)]
pub enum NestEinsumsSpecMultiple {
    Rest(NestEinsumsRest),
    Many(Vec<NestEinsumsSpec>),
}

#[derive(Clone, Debug, FromPyObject)]
pub enum NestEinsumsSpecSub {
    Multiple(NestEinsumsSpecMultiple),
    Val(IntOrMatcher),
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct NestEinsumsSpecInfo {
    pub spec: NestEinsumsSpecMultiple,
    pub name: Option<String>,
    pub out_axes_perm: Option<EinsumAxes>,
}

#[pymethods]
impl NestEinsumsSpecInfo {
    #[new]
    pub fn new(
        spec: NestEinsumsSpecMultiple,
        name: Option<String>,
        out_axes_perm: Option<EinsumAxes>,
    ) -> Result<Self> {
        if let Some(axes) = &out_axes_perm {
            check_permutation(axes).context("out_axes_perm not permutation")?
        }
        Ok(Self {
            spec,
            name,
            out_axes_perm,
        })
    }
}

#[derive(Clone, Debug, FromPyObject)]
pub enum NestEinsumsSpec {
    Info(NestEinsumsSpecInfo),
    Sub(NestEinsumsSpecSub),
}

mod nest_einsum_match_prelude {
    pub use super::{
        NestEinsumsSpec::*, NestEinsumsSpecInfo as Named, NestEinsumsSpecMultiple::*,
        NestEinsumsSpecSub::*,
    };
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct NestEinsumsIdxsInfo {
    pub idxs: NestEinsumsIdxsItem,
    pub name: Option<String>,
    pub out_axes_perm: Option<EinsumAxes>,
}

#[pymethods]
impl NestEinsumsIdxsInfo {
    #[new]
    fn new(
        idxs: NestEinsumsIdxsItem,
        name: Option<String>,
        out_axes_perm: Option<EinsumAxes>,
    ) -> Result<Self> {
        if let Some(axes) = &out_axes_perm {
            check_permutation(axes).context("sorted_out_axes_perm not permutation")?
        }

        Ok(Self {
            idxs,
            name,
            out_axes_perm,
        })
    }
}

#[derive(Debug, Clone, FromPyObject)]
pub enum NestEinsumsIdxsItem {
    Single(usize),
    Many(Vec<NestEinsumsIdxsInfo>),
}

impl NestEinsumsIdxsItem {
    fn all_indices(&self) -> Vec<usize> {
        match self {
            Self::Single(x) => vec![*x],
            Self::Many(x) => x.into_iter().flat_map(|x| x.idxs.all_indices()).collect(),
        }
    }
    fn add(&self, n: usize) -> Self {
        match self {
            Self::Single(x) => Self::Single(x + n),
            Self::Many(x) => Self::Many(
                x.into_iter()
                    .map(|x| NestEinsumsIdxsInfo {
                        idxs: x.idxs.add(n),
                        ..x.clone()
                    })
                    .collect(),
            ),
        }
    }

    fn insert_exact_subset(
        &self,
        name_out_axes: Option<Option<String>>,
        exact_subsets: &mut HashMap<(usize, usize), NestEinsumsIdxsInfo>,
    ) -> Option<(usize, usize)> {
        let out = match self {
            Self::Single(item) => (*item, *item + 1),
            Self::Many(items) => {
                let (start, end) =
                    items
                        .iter()
                        .fold((usize::MAX, usize::MIN), |(start, end), item| {
                            if let Some((new_start, new_end)) = item
                                .idxs
                                .insert_exact_subset(Some(item.name.clone()), exact_subsets)
                            {
                                // we assume contiguous, so this is valid!
                                if end != usize::MIN {
                                    assert_eq!(end, new_start);
                                }
                                (start.min(new_start), end.max(new_end)) // this fold is a bit silly, we could just get first + last
                            } else {
                                return (start, end);
                            }
                        });
                if start == usize::MAX {
                    // empty einsum
                    return None;
                } else {
                    assert_ne!(end, usize::MIN);
                    (start, end)
                }
            }
        };
        if let Some(name) = name_out_axes {
            exact_subsets.insert(
                out,
                NestEinsumsIdxsInfo::new(self.clone(), name, None).unwrap(),
            );
        }
        Some(out)
    }
}

/// maintains invariant that indices are in sorted enumeration order
#[derive(Clone)]
pub struct NamedEnumeration(NestEinsumsIdxsItem);

impl NamedEnumeration {
    pub fn new(idxs: NestEinsumsIdxsItem) -> Self {
        let all_indices = idxs.all_indices();
        assert!(&all_indices == &(0..all_indices.len()).collect::<Vec<usize>>());
        Self(idxs)
    }

    fn exact_subset_to_named_idxs(&self) -> HashMap<(usize, usize), NestEinsumsIdxsInfo> {
        let mut out_map = HashMap::default();
        self.0.insert_exact_subset(None, &mut out_map);
        out_map
    }
}

pub fn check_permutation_rest(
    perm: &[usize],
    count: usize,
    allow_rest: bool,
) -> Result<HashSet<usize>> {
    let perm_set: HashSet<_> = perm.iter().cloned().collect();
    if perm.len() != perm_set.len() {
        bail!(PermError::IntsNotUnique {
            ints: perm.iter().cloned().collect()
        })
    }
    let count_set = (0..count).collect::<HashSet<_>>();
    if !perm_set.is_subset(&count_set) {
        bail!(NestEinsumsError::IntNotContainedInRangeCount {
            ints: perm.to_vec(),
            count,
            extra_ints: perm_set.difference(&count_set).cloned().collect()
        })
    }
    let rest: HashSet<usize> = count_set.difference(&perm_set).cloned().collect();
    if !allow_rest && rest.len() != 0 {
        bail!(NestEinsumsError::PermutationMissesIdxsAndNoRestInSpec { missed_idxs: rest })
    }
    Ok(rest)
}

impl NestEinsumsSpec {
    fn count_rest(&self) -> usize {
        use nest_einsum_match_prelude::*;
        match self {
            Sub(Val(_)) => 0,
            Sub(Multiple(Many(items)))
            | Info(Named {
                spec: Many(items), ..
            }) => items.iter().map(|x| x.count_rest()).sum(),
            Sub(Multiple(Rest(_))) | Info(Named { spec: Rest(_), .. }) => 1,
        }
    }

    fn check_rest_valid(&self) -> Result<()> {
        let count_rest = self.count_rest();
        if count_rest > 1 {
            bail!(NestEinsumsError::MultipleRest { count_rest });
        }
        Ok(())
    }

    pub fn all_vals(&self) -> Vec<IntOrMatcher> {
        use nest_einsum_match_prelude::*;
        match self {
            Sub(Val(val)) => vec![val.clone()],
            Sub(Multiple(Many(items)))
            | Info(Named {
                spec: Many(items), ..
            }) => items.iter().flat_map(|x| x.all_vals()).collect(),
            Sub(Multiple(Rest(_))) | Info(Named { spec: Rest(_), .. }) => Vec::new(),
        }
    }

    pub fn convert_to_named_idxs(
        &self,
        mapping: &HashMap<(usize, usize), NestEinsumsIdxsInfo>,
        circuits: &[CircuitRc],
    ) -> Result<NestEinsumsIdxsItem> {
        let all_vals = self.all_vals();
        let mut to_int = HashMap::default();
        let mut all_ints_vals = Vec::new();
        for v in all_vals {
            let out = match &v {
                IntOrMatcher::Int(v) => *v,
                IntOrMatcher::Matcher(matcher) => {
                    let all_matches = circuits
                        .iter()
                        .enumerate()
                        .filter_map(|(i, c)| {
                            flip_result_op(
                                matcher.call(c.clone()).map(|b| b.then_some((i, c.clone()))),
                            )
                        })
                        .collect::<Result<Vec<_>>>()?;
                    match &all_matches[..] {
                        [(single_val, _)] => *single_val,
                        [] => bail!(NestEinsumsError::MatcherMatchedNone {
                            matcher: matcher.clone()
                        }),
                        rest => bail!(NestEinsumsError::MatcherMatchedMultiple {
                            matcher: matcher.clone(),
                            matches: rest.iter().map(|(_, x)| x.clone()).collect()
                        }),
                    }
                }
            };
            to_int.insert(v.clone(), out);
            all_ints_vals.push(out);
        }
        let allow_rest = self.count_rest() == 1;
        let rest = check_permutation_rest(&all_ints_vals, circuits.len(), allow_rest)
            .context("ints from flattened spec not valid permutation")?;
        if circuits.is_empty() {
            return Ok(NestEinsumsIdxsItem::Many(Vec::new()));
        }
        let rest_items = Self::find_rest(rest, mapping);
        let mut all_items = self
            .convert_to_named_idxs_impl(mapping, &to_int, &rest_items, true)?
            .0;
        // this assert is valid because we pass in 'is_outer=True' above.
        assert_eq!(all_items.len(), 1);
        Ok(all_items.pop().unwrap().idxs)
    }

    fn find_rest(
        rest: HashSet<usize>,
        mapping: &HashMap<(usize, usize), NestEinsumsIdxsInfo>,
    ) -> Vec<NestEinsumsIdxsInfo> {
        let mut subset_keys: Vec<_> = mapping
            .keys()
            .cloned()
            .filter(|&(k_start, k_end)| rest.is_superset(&(k_start..k_end).collect()))
            .collect();
        subset_keys.sort();
        let final_keys: Vec<_> = subset_keys
            .iter()
            .cloned()
            .filter(|(k_start, k_end)| {
                // TODO: could toposort for efficiency
                !subset_keys.iter().any(|(k_inner_start, k_inner_end)| {
                    let is_different = k_start != k_inner_start || k_end != k_inner_end;
                    let inner_includes = k_inner_start <= k_start && k_inner_end >= k_end;
                    is_different && inner_includes
                })
            })
            .collect();

        // some quick debug checking
        for ((_, prior_end), (next_start, _)) in final_keys.iter().zip(final_keys.iter().skip(1)) {
            assert!(prior_end <= next_start);
        }
        let all_key_vals: HashSet<usize> = final_keys
            .iter()
            .flat_map(|&(start, end)| start..end)
            .collect();
        assert_eq!(all_key_vals, rest);

        final_keys.iter().map(|k| mapping[k].clone()).collect()
    }

    pub fn get_info(
        &self,
        all_ints: &[usize],
        mapping: &HashMap<(usize, usize), NestEinsumsIdxsInfo>,
    ) -> (Option<String>, Option<EinsumAxes>) {
        let start_r = *all_ints.iter().min().unwrap();
        let end_r = *all_ints.iter().max().unwrap() + 1;
        let orig_info = if all_ints.len() == end_r - start_r {
            mapping.get(&(start_r, end_r))
        } else {
            None
        };
        match self {
            Self::Info(NestEinsumsSpecInfo {
                name,
                out_axes_perm,
                ..
            }) => (name.clone(), out_axes_perm.clone()),

            Self::Sub(_) => (orig_info.map(|x| x.name.clone()).flatten(), None),
        }
    }

    pub fn convert_to_named_idxs_impl(
        &self,
        mapping: &HashMap<(usize, usize), NestEinsumsIdxsInfo>,
        mapping_to_int: &HashMap<IntOrMatcher, usize>,
        rest_items: &[NestEinsumsIdxsInfo],
        is_outer: bool,
    ) -> Result<(Vec<NestEinsumsIdxsInfo>, Vec<usize>)> {
        use nest_einsum_match_prelude::*;

        let res = match self {
            Sub(Val(val)) => {
                let int = mapping_to_int[val];
                return Ok((vec![mapping[&(int, int + 1)].clone()], vec![int]));
            }
            Sub(Multiple(Many(items)))
            | Info(Named {
                spec: Many(items), ..
            }) => {
                let (items_vec, subsets): (Vec<_>, Vec<_>) = items
                    .iter()
                    .map(|x| {
                        x.convert_to_named_idxs_impl(mapping, mapping_to_int, rest_items, false)
                    })
                    .collect::<Result<Vec<_>>>()?
                    .into_iter()
                    .unzip();
                let all_ints: Vec<_> = subsets.into_iter().flatten().collect();
                assert!(is_unique(&all_ints));
                if all_ints.len() == 0 {
                    return Ok((vec![], all_ints));
                }

                let (name, out_axes_perm) = self.get_info(&all_ints, mapping);

                (
                    vec![NestEinsumsIdxsInfo::new(
                        NestEinsumsIdxsItem::Many(items_vec.into_iter().flatten().collect()),
                        name,
                        out_axes_perm,
                    )
                    .unwrap()],
                    all_ints,
                )
            }
            Sub(Multiple(Rest(NestEinsumsRest { flat })))
            | Info(Named {
                spec: Rest(NestEinsumsRest { flat }),
                ..
            }) => {
                let all_ints: Vec<usize> = rest_items
                    .iter()
                    .flat_map(|x| x.idxs.all_indices())
                    .collect();
                assert!(is_unique(&all_ints));
                let rest_items = rest_items.iter().cloned().collect();
                let out_idxs = if *flat && !is_outer {
                    rest_items
                } else {
                    let (name, out_axes_perm) = self.get_info(&all_ints, mapping);
                    vec![NestEinsumsIdxsInfo::new(
                        NestEinsumsIdxsItem::Many(rest_items),
                        name,
                        out_axes_perm,
                    )
                    .unwrap()]
                };
                (out_idxs, all_ints)
            }
        };
        Ok(res)
    }
}

pub fn collect_named_idxs(args: &[(CircuitRc, Option<NamedEnumeration>)]) -> NamedEnumeration {
    let mut running_count = 0;
    let out = args
        .into_iter()
        .map(|(circ, maybe_items)| {
            let (new_item, additional_count) = match maybe_items {
                Some(items) => {
                    // not efficient but whatever
                    (items.0.add(running_count), items.0.all_indices().len())
                }
                None => (NestEinsumsIdxsItem::Single(running_count), 1),
            };
            running_count += additional_count;
            NestEinsumsIdxsInfo::new(new_item, circ.name_cloned(), None).unwrap()
        })
        .collect();
    NamedEnumeration::new(NestEinsumsIdxsItem::Many(out))
}

/// ignores 'found' and just looks at whether or not matcher has terminated yet.
/// In other words, uses the matcher as a 'traversal'.
pub fn einsum_flatten_impl(
    circ: CircuitRc,
    matcher: IterativeMatcherRc,
) -> Result<(CircuitRc, Option<NamedEnumeration>)> {
    // TODO: we could cache, but probably overkill
    let f = || -> Result<_> {
        if let Some(einsum) = circ.as_einsum() {
            // if einsum.args.len() > 0 {
            // if let chain ICE's compiler : /
            if let (Some(new_matcher), _) = matcher
                .match_iterate(circ.clone())?
                .none_if_finished(matcher)
            {
                return Ok(Some((einsum, new_matcher)));
            }
            // }
        }
        Ok(None)
    };

    let (einsum, new_matcher) = if let Some(x) = f()? {
        x
    } else {
        return Ok((circ, None));
    };

    let rec_on_children = einsum
        .input_circuits()
        .map(|c| einsum_flatten_impl(c, new_matcher.clone()))
        .collect::<Result<Vec<_>>>()?;
    let einsum = einsum.map_children_unwrap_idxs(|i| rec_on_children[i].0.clone());
    let einsum = make_einsum_ints_same_one_layer(&einsum);

    let new_args = einsum
        .args
        .clone()
        .into_iter()
        .zip(&rec_on_children)
        .flat_map(|((node, ints), (_, named_idxs))| {
            if named_idxs.is_some() {
                node.as_einsum().unwrap().args.clone()
            } else {
                vec![(node, ints)]
            }
        })
        .collect();

    Ok((
        Einsum::nrc(new_args, einsum.out_axes.clone(), einsum.name_cloned()),
        Some(collect_named_idxs(&rec_on_children)),
    ))
}

#[pyfunction]
pub fn einsum_flatten(einsum: Einsum, traversal: Option<IterativeMatcherRc>) -> Result<Einsum> {
    let traversal = traversal.unwrap_or(IterativeMatcher::noop_traversal().rc());
    einsum_flatten_impl(einsum.rc(), traversal)
        .map(|(circ, _)| circ.as_einsum().unwrap().normalize_ints())
}

#[pyfunction]
pub fn nest_einsums(
    einsum: Einsum,
    spec: NestEinsumsSpecSub, // use sub to disallow top level name which does nothing
    traversal: Option<IterativeMatcherRc>,
) -> Result<Einsum> {
    let spec = NestEinsumsSpec::Sub(spec);
    spec.check_rest_valid()?;
    let traversal = traversal.unwrap_or(IterativeMatcher::noop_traversal().rc());
    let (flat_einsum, enumeration) = einsum_flatten_impl(einsum.crc(), traversal.clone())?;
    if enumeration.is_none() {
        bail!(NestEinsumsError::TraversalMatchedNothing {
            traversal,
            circuit: einsum.crc()
        })
    }
    let flat_einsum = flat_einsum.as_einsum().unwrap().normalize_ints();
    let enumeration = enumeration.unwrap();
    let new_item = spec.convert_to_named_idxs(
        &enumeration.exact_subset_to_named_idxs(),
        &flat_einsum.input_circuits().collect::<Vec<_>>(),
    )?;

    nest_flat_einsum_strict(&flat_einsum, new_item)
}

#[pyfunction]
pub fn nest_flat_einsum_strict(flat_einsum: &Einsum, spec: NestEinsumsIdxsItem) -> Result<Einsum> {
    match spec {
        NestEinsumsIdxsItem::Single(_) => {
            assert_eq!(flat_einsum.args.len(), 1);
            Ok(flat_einsum.clone())
        }
        NestEinsumsIdxsItem::Many(specs) => nest_flat_einsum_strict_rec(
            &flat_einsum.args,
            flat_einsum.out_axes.clone(),
            specs,
            flat_einsum.name_cloned(),
        ),
    }
}

pub fn nest_flat_einsum_strict_rec(
    flat_einsum: &EinsumArgs,
    out_axes: EinsumAxes,
    specs: Vec<NestEinsumsIdxsInfo>,
    name: Option<String>,
) -> Result<Einsum> {
    // TODO: avoid quadratic running time...
    let all_ints: Vec<HashSet<AxisInt>> = specs
        .iter()
        .map(|spec| {
            spec.idxs
                .all_indices()
                .into_iter()
                .flat_map(|idx| &flat_einsum[idx].1)
                .cloned()
                .collect()
        })
        .collect();
    let out_axes_set = out_axes.iter().cloned().collect();

    let args = specs
        .into_iter()
        .enumerate()
        .map(|(i, spec)| {
            let out = match spec.idxs {
                NestEinsumsIdxsItem::Single(v) => flat_einsum[v].clone(),
                NestEinsumsIdxsItem::Many(sub_specs) => {
                    let my_ints = &all_ints[i];
                    let all_other_ints: HashSet<AxisInt> = all_ints
                        .iter()
                        .enumerate()
                        .filter(|(j, _)| j != &i)
                        .flat_map(|(_, ints)| ints)
                        .cloned()
                        .collect();
                    let all_other_ints: HashSet<_> =
                        all_other_ints.union(&out_axes_set).cloned().collect();
                    let out_ints = all_other_ints.intersection(my_ints).cloned();

                    // get out axes
                    let mut sub_out_axes: EinsumAxes = out_ints.collect();
                    sub_out_axes.sort();

                    // then permute
                    if let Some(perm) = spec.out_axes_perm {
                        if perm.len() != sub_out_axes.len() {
                            bail!(NestEinsumsError::PermHasWrongLen {
                                perm: perm.clone(),
                                expected_len: sub_out_axes.len()
                            })
                        }
                        sub_out_axes = perm.into_iter().map(|i| sub_out_axes[i as usize]).collect();
                    }

                    (
                        nest_flat_einsum_strict_rec(
                            flat_einsum,
                            sub_out_axes.clone(),
                            sub_specs,
                            spec.name,
                        )?
                        .rc(),
                        sub_out_axes,
                    )
                }
            };
            Ok(out)
        })
        .collect::<Result<EinsumArgs>>()?;

    Ok(Einsum::new(args, out_axes, name))
}

#[pyfunction]
pub fn nest_einsums_strict(
    einsum: Einsum,
    spec: NestEinsumsIdxsItem,
    traversal: Option<IterativeMatcherRc>,
) -> Result<Einsum> {
    let flat_einsum = einsum_flatten(einsum, traversal)?;
    nest_flat_einsum_strict(&flat_einsum, spec)
}

#[apply(python_error_exception)]
#[base_error_name(NestEinsums)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum NestEinsumsError {
    #[error("count_rest={count_rest}")]
    MultipleRest { count_rest: usize },
    #[error("matcher={matcher:?} matches={matches:?}")]
    MatcherMatchedMultiple {
        matcher: MatcherRc,
        matches: Vec<CircuitRc>,
    },
    #[error("matcher={matcher:?}")]
    MatcherMatchedNone { matcher: MatcherRc },
    #[error("traversal={traversal:?} circuit={circuit:?}")]
    TraversalMatchedNothing {
        traversal: IterativeMatcherRc,
        circuit: CircuitRc,
    },
    #[error("ints={ints:?} count={count} extra_ints={extra_ints:?}")]
    IntNotContainedInRangeCount {
        ints: Vec<usize>,
        count: usize,
        extra_ints: HashSet<usize>,
    },
    #[error("perm={perm:?} expected_len={expected_len}")]
    PermHasWrongLen {
        perm: EinsumAxes,
        expected_len: usize,
    },
    #[error("This einsum wasn't present in orig!")]
    OrigNumPermWhenNotPresentInOrig {},
    #[error("missed_idxs={missed_idxs:?}")]
    PermutationMissesIdxsAndNoRestInSpec { missed_idxs: HashSet<usize> },
}
