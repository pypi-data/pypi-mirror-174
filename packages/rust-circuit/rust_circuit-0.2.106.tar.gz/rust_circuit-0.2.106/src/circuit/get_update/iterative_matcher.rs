use std::{
    collections::HashSet,
    fmt::{self, Debug},
    ops,
    sync::Arc,
    vec,
};

use anyhow::{bail, Result};
use macro_rules_attribute::apply;
use pyo3::{types::PyTuple, AsPyPointer};
use uuid::uuid;

use super::{
    BoundGetter, BoundUpdater, Getter, Matcher, MatcherData, MatcherFromPyBase, MatcherRc,
    Transform, TransformRc, Updater,
};
use crate::{
    circuit::{CircuitRc, HashBytes},
    eq_by_big_hash::EqByBigHash,
    impl_both_by_big_hash,
    pyo3_prelude::*,
    setup_callable, simple_default, simple_from,
    tensor_util::Slice,
    util::{
        arc_ref_clone, arc_unwrap_or_clone, as_sorted, flip_op_result, split_first_take,
        EmptySingleMany as ESM,
    },
};

#[derive(Clone, FromPyObject)]
pub enum IterativeMatcherFromPy {
    BaseMatch(MatcherFromPyBase),
    IterativeMatcher(IterativeMatcher),
    #[pyo3(transparent)]
    PyFunc(PyObject),
}

#[derive(Clone, Debug)]
pub enum IterativeMatcherData {
    Match(Matcher),
    Filter(FilterIterativeMatcher),
    Chains(HashSet<ChainItem>),
    Raw(RawIterativeMatcher),
    PyFunc(PyObject),
}

setup_callable!(IterativeMatcher, IterativeMatcherData, IterativeMatcherFromPy, match_iterate(circuit : CircuitRc) -> IterateMatchResults);

simple_from!(|x: Matcher| -> IterativeMatcher { IterativeMatcherData::Match(x).into() });
simple_from!(|x: MatcherData| -> IterativeMatcher { Matcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcher { Matcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcherFromPy {
    IterativeMatcherFromPy::BaseMatch(x.into())
});
simple_from!(|x: Matcher| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_from!(|x: MatcherData| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_from!(|x: MatcherFromPyBase| -> IterativeMatcherRc { IterativeMatcher::from(x).into() });
simple_default!(IterativeMatcherFromPy {
    MatcherFromPyBase::default().into()
});
simple_default!(IterativeMatcher {
    Matcher::default().into()
});
simple_default!(IterativeMatcherRc {
    IterativeMatcher::default().into()
});

impl From<IterativeMatcherFromPy> for IterativeMatcher {
    fn from(m: IterativeMatcherFromPy) -> Self {
        match m {
            IterativeMatcherFromPy::BaseMatch(x) => x.into(),
            IterativeMatcherFromPy::IterativeMatcher(x) => x.into(),
            // we intentionally do a matcher here as the default - if users want
            // a IterativeMatcher pyfunc, they can explicitly use IterativeMatcher
            // factory.
            IterativeMatcherFromPy::PyFunc(x) => MatcherData::PyFunc(x).into(),
        }
    }
}

#[derive(Clone)]
pub struct ChainItem {
    first: IterativeMatcherRc,
    rest: Vec<IterativeMatcherRc>,
    hash: HashBytes,
}

impl EqByBigHash for ChainItem {
    fn hash(&self) -> HashBytes {
        self.hash
    }
}

impl_both_by_big_hash!(ChainItem);

impl Debug for ChainItem {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        [self.first.clone()]
            .into_iter()
            .chain(self.rest.clone())
            .collect::<Vec<_>>()
            .fmt(f)
    }
}

impl ChainItem {
    pub fn new(first: IterativeMatcherRc, rest: Vec<IterativeMatcherRc>) -> Self {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&first.hash);
        for x in &rest {
            hasher.update(&x.hash);
        }

        Self {
            first,
            rest,
            hash: hasher.finalize().into(),
        }
    }

    pub fn last(&self) -> &IterativeMatcherRc {
        self.rest.last().unwrap_or(&self.first)
    }
}

impl IterativeMatcherData {
    fn uuid(&self) -> [u8; 16] {
        match self {
            Self::Match(_) => uuid!("f1d5e8ec-cba0-496f-883e-78dd5cdc3a49"),
            Self::Filter(_) => uuid!("bcc5ccaa-afbe-414d-88b4-b8eac8c93ece"),
            Self::Chains(_) => uuid!("958d03ed-7a1a-4ea9-8dd4-d4a8a68feecb"),
            Self::Raw(_) => uuid!("5838ac96-0f48-4cdb-874f-d4f68ce3a52b"),
            Self::PyFunc(_) => uuid!("d3afc3c0-5c86-46df-9e41-7944caedd901"),
        }
        .into_bytes()
    }

    fn item_hash(&self, hasher: &mut blake3::Hasher) {
        match self {
            Self::Match(x) => {
                hasher.update(&x.hash());
            }
            Self::Filter(FilterIterativeMatcher {
                iterative_matcher,
                term_if_matches,
                start_depth,
                end_depth,
                term_early_at,
                depth,
            }) => {
                hasher.update(&iterative_matcher.hash);
                hasher.update(&[*term_if_matches as u8]);
                hasher.update(&[start_depth.is_some() as u8]);
                hasher.update(&start_depth.unwrap_or(0).to_le_bytes());
                hasher.update(&[end_depth.is_some() as u8]);
                hasher.update(&end_depth.unwrap_or(0).to_le_bytes());
                hasher.update(&term_early_at.hash());
                hasher.update(&depth.to_le_bytes());
            }
            Self::Chains(chains) => {
                for chain in as_sorted(chains) {
                    hasher.update(&chain.hash);
                }
            }
            Self::Raw(x) => {
                hasher.update(&(Arc::as_ptr(&x.0) as *const () as usize).to_le_bytes());
            }
            Self::PyFunc(x) => {
                hasher.update(&(x.as_ptr() as usize).to_le_bytes());
            }
        }
    }
}

/// Helper with some basic rules you may want to use to control your node matching iterations.
/// TODO: include docs in py + other places as needed.
#[derive(Clone, Debug)]
pub struct FilterIterativeMatcher {
    pub iterative_matcher: IterativeMatcherRc,
    ///if true, stops once it has found a match
    pub term_if_matches: bool,
    /// depth at which we start matching
    pub start_depth: Option<u32>,
    /// depth at which we stop matching
    pub end_depth: Option<u32>,
    /// terminate iterative matching if we reach a node which matches this
    pub term_early_at: MatcherRc,
    depth: u32,
}

impl FilterIterativeMatcher {
    /// Fancy constructor which supports range
    ///
    /// TODO: add support for a builder with defaults because this is really annoying...
    /// TODO: actually test this when builder is added!
    pub fn new_range<R: ops::RangeBounds<u32>>(
        iterative_matcher: IterativeMatcherRc,
        term_if_matches: bool,
        depth_range: R,
        term_early_at: MatcherRc,
    ) -> Self {
        use ops::Bound;

        let start_depth = match depth_range.start_bound() {
            Bound::Unbounded => None,
            Bound::Included(x) => Some(*x),
            Bound::Excluded(x) => Some(*x + 1),
        };
        let end_depth = match depth_range.end_bound() {
            Bound::Unbounded => None,
            Bound::Included(x) => Some(*x + 1),
            Bound::Excluded(x) => Some(*x),
        };
        Self {
            iterative_matcher,
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
            depth: 0,
        }
    }

    pub fn new(
        iterative_matcher: IterativeMatcherRc,
        term_if_matches: bool,
        start_depth: Option<u32>,
        end_depth: Option<u32>,
        term_early_at: MatcherRc,
    ) -> Self {
        Self {
            iterative_matcher,
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
            depth: 0,
        }
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let with_dist_of_end = |offset: u32| {
            self.end_depth
                .map(|x| self.depth >= x.saturating_sub(offset))
                .unwrap_or(false)
        };

        let after_end = with_dist_of_end(0);
        if after_end {
            return Ok(IterateMatchResults {
                updated: None,
                finished: true,
                found: false,
            });
        }

        let before_start = self.start_depth.map(|x| self.depth < x).unwrap_or(false);
        if before_start {
            return Ok(IterateMatchResults {
                updated: Some(
                    IterativeMatcherData::Filter(FilterIterativeMatcher {
                        depth: self.depth + 1,
                        ..self.clone()
                    })
                    .into(),
                ),
                finished: false,
                found: false,
            });
        }

        let IterateMatchResults {
            updated,
            finished,
            found,
        } = self.iterative_matcher.match_iterate(circuit.clone())?;

        let reached_end = with_dist_of_end(1);
        if finished
            || (found && self.term_if_matches)
            || reached_end
            || self.term_early_at.call(circuit)?
        {
            return Ok(IterateMatchResults {
                updated: None,
                finished: true,
                found,
            });
        }

        let new_depth = if self.end_depth.is_some() {
            self.depth + 1
        } else {
            self.depth
        };
        let updated = (self.end_depth.is_some() || updated.is_some()).then(|| {
            let new = updated
                .map(Into::into)
                .unwrap_or(self.iterative_matcher.clone());

            IterativeMatcherData::Filter(FilterIterativeMatcher {
                iterative_matcher: new,
                depth: new_depth,
                ..self.clone()
            })
            .into()
        });

        Ok(IterateMatchResults {
            updated,
            finished,
            found,
        })
    }
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct IterateMatchResults {
    #[pyo3(set, get)]
    pub updated: Option<IterativeMatcherRc>,
    #[pyo3(set, get)]
    pub finished: bool,
    #[pyo3(set, get)]
    pub found: bool,
}

#[pymethods]
impl IterateMatchResults {
    #[new]
    #[args(updated = "None", finished = "false", found = "false")]
    fn new(updated: Option<IterativeMatcherRc>, finished: bool, found: bool) -> Self {
        Self {
            updated,
            finished,
            found,
        }
    }

    fn to_tup(&self) -> Py<PyTuple> {
        Python::with_gil(|py| {
            PyTuple::new(
                py,
                [
                    self.updated.clone().into_py(py),
                    self.finished.into_py(py),
                    self.found.into_py(py),
                ],
            )
            .into()
        })
    }
}

impl IterativeMatcher {
    pub fn or(self, other: IterativeMatcherRc) -> Self {
        Self::any(vec![self.crc(), other])
    }

    pub fn validate_matched(&self, matched: &HashSet<CircuitRc>) -> Result<()> {
        match &self.data {
            IterativeMatcherData::Match(m) => m.validate_matched(matched),
            IterativeMatcherData::Filter(m) => m.iterative_matcher.validate_matched(matched),
            IterativeMatcherData::Chains(m) => {
                for chain in m {
                    chain.last().validate_matched(matched)?;
                }
                Ok(())
            }
            IterativeMatcherData::PyFunc(_) | IterativeMatcherData::Raw(_) => Ok(()),
        }
    }
    // TODO: more rust niceness funcs like the py ones!
}

#[pymethods]
impl IterativeMatcher {
    #[new]
    #[args(inps = "*")]
    fn py_new(inps: Vec<IterativeMatcherRc>) -> Self {
        match inps.into() {
            ESM::Empty => MatcherData::Always(false).into(),
            ESM::Single(x) => arc_ref_clone(&x),
            ESM::Many(x) => Self::any(x),
        }
    }

    pub fn match_iterate(&self, circuit: CircuitRc) -> Result<IterateMatchResults> {
        let res = match &self.data {
            IterativeMatcherData::Match(m) => IterateMatchResults {
                updated: None,
                finished: false,
                found: m.call(circuit)?,
            },
            IterativeMatcherData::Filter(filter) => filter.match_iterate(circuit)?,
            IterativeMatcherData::Chains(chains) => {
                /// avoid some hashing and some copies - probably overkill
                #[derive(Clone, Copy)]
                enum MaybeChain<'a> {
                    Chain(&'a ChainItem),
                    Slices {
                        first: &'a IterativeMatcherRc,
                        rest: &'a [IterativeMatcherRc],
                    },
                }

                impl<'a> MaybeChain<'a> {
                    fn first(&'a self) -> &'a IterativeMatcherRc {
                        match self {
                            Self::Chain(x) => &x.first,
                            Self::Slices { first, .. } => first,
                        }
                    }

                    fn rest(&'a self) -> &'a [IterativeMatcherRc] {
                        match self {
                            Self::Chain(x) => &x.rest,
                            Self::Slices { rest, .. } => rest,
                        }
                    }
                }

                fn run_item(
                    chain: MaybeChain<'_>,
                    circuit: &CircuitRc,
                    new_items: &mut HashSet<ChainItem>,
                ) -> Result<bool> {
                    let IterateMatchResults {
                        updated,
                        finished,
                        found,
                    } = chain.first().match_iterate(circuit.clone())?;

                    if !finished {
                        let new_chain = match (updated, chain) {
                            (None, MaybeChain::Chain(chain)) => chain.clone(),
                            (Some(x), chain) => ChainItem::new(x, chain.rest().to_vec()),
                            (None, MaybeChain::Slices { first, .. }) => {
                                ChainItem::new(first.clone(), chain.rest().to_vec())
                            }
                        };
                        new_items.insert(new_chain);
                    }

                    if found {
                        match chain.rest() {
                            [] => Ok(true),
                            [rest_first, rest_rest @ ..] => run_item(
                                MaybeChain::Slices {
                                    first: rest_first,
                                    rest: rest_rest,
                                },
                                circuit,
                                new_items,
                            ),
                        }
                    } else {
                        Ok(false)
                    }
                }

                let mut new_items = HashSet::new();
                let mut any_chain_finished = false;
                for chain in chains {
                    any_chain_finished =
                        run_item(MaybeChain::Chain(chain), &circuit, &mut new_items)?
                            || any_chain_finished;
                }

                let finished = new_items.is_empty();

                IterateMatchResults {
                    finished,
                    updated: (!finished && &new_items != chains)
                        .then(|| IterativeMatcherData::Chains(new_items).into()),
                    found: any_chain_finished,
                }
            }
            IterativeMatcherData::Raw(f) => f.0(circuit)?,
            IterativeMatcherData::PyFunc(pyfunc) => {
                Python::with_gil(|py| pyfunc.call1(py, (circuit,)).and_then(|r| r.extract(py)))?
            }
        };

        Ok(res)
    }

    fn validate_matched_py(&self, matched: HashSet<CircuitRc>) -> Result<()> {
        self.validate_matched(&matched)
    }

    #[staticmethod]
    #[args(matchers = "*")]
    pub fn any(matchers: Vec<IterativeMatcherRc>) -> Self {
        IterativeMatcherData::Chains(
            matchers
                .into_iter()
                .map(|x| ChainItem::new(x.into(), Vec::new()))
                .collect(),
        )
        .into()
    }

    #[staticmethod]
    #[args(first, rest = "*")]
    pub fn mk_chain(first: IterativeMatcherRc, rest: Vec<IterativeMatcherRc>) -> Self {
        first.chain(rest)
    }

    #[staticmethod]
    #[args(chains = "*")]
    pub fn mk_chain_many(chains: Vec<Vec<IterativeMatcherRc>>) -> Result<Self> {
        Ok(IterativeMatcherData::Chains(
            chains
                .into_iter()
                .map(|mut chain| match split_first_take(&mut chain) {
                    None => bail!("Received empty tuple for a chain, we expect len >= 1",),
                    Some((first, rest)) => Ok(ChainItem::new(first, rest.collect())),
                })
                .collect::<Result<_>>()?,
        )
        .into())
    }

    #[staticmethod]
    #[pyo3(name = "mk_func")]
    pub(super) fn mk_func_py(f: PyObject) -> Self {
        IterativeMatcherData::PyFunc(f).into()
    }

    #[args(others = "*")]
    pub fn mk_or(&self, others: Vec<IterativeMatcherRc>) -> Self {
        Self::any([self.clone().into()].into_iter().chain(others).collect())
    }

    fn __or__(&self, other: IterativeMatcherRc) -> Self {
        self.clone().or(other)
    }
    fn __ror__(&self, other: IterativeMatcherRc) -> Self {
        arc_unwrap_or_clone(other.0).or(self.crc())
    }

    // TODO: write flatten/simplify method if we want the extra speed + niceness!
}

macro_rules! dup_functions {
    {
        #[self_id($self_ident:ident)]
        impl IterativeMatcher {
            $(
            $( #[$($meta_tt:tt)*] )*
        //  ^~~~attributes~~~~^
            $vis:vis fn $name:ident (
                &self
                $(, $arg_name:ident : $arg_ty:ty )* $(,)?
        //      ^~~~~~~~~~~~~~~argument list!~~~~~~~~~~~^
                )
                $( -> $ret_ty:ty )?
        //      ^~~~return type~~~^
                { $($tt:tt)* }
            )*

        }
    } => {
        // paste is needed due to how pymethods proc macro works
        paste::paste!{
            #[pymethods]
            impl IterativeMatcher {
                $(
                    $(#[$($meta_tt)*])*
                    $vis fn $name(&self, $($arg_name : $arg_ty,)*) $(-> $ret_ty)* {
                        let $self_ident = self;
                        $($tt)*
                    }
                )*
            }

            #[pymethods]
            impl Matcher {
                $(
                    $(#[$($meta_tt)*])*
                    $vis fn $name(&self, $($arg_name : $arg_ty,)*) $(-> $ret_ty)* {
                        self.to_iterative_matcher().$name($($arg_name,)*)
                    }
                )*
            }
        }

    };
}

#[apply(dup_functions)]
#[self_id(self_)]
impl IterativeMatcher {
    #[args(
        term_if_matches = "false",
        start_depth = "None",
        end_depth = "None",
        term_early_at = "MatcherFromPyBase::Always(false).into()"
    )]
    pub fn filter(
        &self,
        term_if_matches: bool,
        start_depth: Option<u32>,
        end_depth: Option<u32>,
        term_early_at: MatcherRc,
    ) -> IterativeMatcher {
        // TODO: flatten
        IterativeMatcherData::Filter(FilterIterativeMatcher::new(
            self_.clone().into(),
            term_if_matches,
            start_depth,
            end_depth,
            term_early_at,
        ))
        .into()
    }

    #[args(
        term_if_matches = "false",
        depth_slice = "Slice::IDENT",
        term_early_at = "MatcherFromPyBase::Always(false).into()"
    )]
    pub fn filter_sl(
        &self,
        term_if_matches: bool,
        depth_slice: Slice,
        term_early_at: MatcherRc,
    ) -> Result<IterativeMatcher> {
        Ok(self_.filter(
            term_if_matches,
            flip_op_result(depth_slice.start.map(|x| x.try_into()))?,
            flip_op_result(depth_slice.stop.map(|x| x.try_into()))?,
            term_early_at,
        ))
    }

    #[args(rest = "*")]
    pub fn chain(&self, rest: Vec<IterativeMatcherRc>) -> IterativeMatcher {
        // TODO: flatten
        IterativeMatcherData::Chains(
            [ChainItem::new(self_.clone().into(), rest)]
                .into_iter()
                .collect::<HashSet<_>>(),
        )
        .into()
    }

    #[args(rest = "*")]
    pub fn chain_many(&self, rest: Vec<Vec<IterativeMatcherRc>>) -> IterativeMatcher {
        // TODO: flatten
        IterativeMatcherData::Chains(
            rest.into_iter()
                .map(|x| ChainItem::new(self_.clone().into(), x))
                .collect(),
        )
        .into()
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get(&self, circuit: CircuitRc, fancy_validate: bool) -> Result<HashSet<CircuitRc>> {
        Getter::default().get(circuit, self_.crc(), Some(fancy_validate))
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get_unique_op(
        &self,
        circuit: CircuitRc,
        fancy_validate: bool,
    ) -> Result<Option<CircuitRc>> {
        Getter::default().get_unique_op(circuit, self_.crc(), Some(fancy_validate))
    }

    #[args(fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn get_unique(&self, circuit: CircuitRc, fancy_validate: bool) -> Result<CircuitRc> {
        Getter::default().get_unique(circuit, self_.crc(), Some(fancy_validate))
    }

    pub fn validate(&self, circuit: CircuitRc) -> Result<()> {
        Getter::default().validate(circuit, self_.crc())
    }

    #[args(default_fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn getter(&self, default_fancy_validate: bool) -> BoundGetter {
        Getter::new(default_fancy_validate).bind(self_.crc())
    }

    #[args(
        transform_along_modified_path = "Transform::ident().into()",
        cache_transform = "Updater::default().cache_transform",
        cache_transform_along_modified_path = "Updater::default().cache_transform_along_modified_path",
        cache_update = "Updater::default().cache_update",
        fancy_validate = "Updater::default().default_fancy_validate"
    )]
    pub fn update(
        &self,
        circuit: CircuitRc,
        transform: TransformRc,
        transform_along_modified_path: TransformRc,
        cache_transform: bool,
        cache_transform_along_modified_path: bool,
        cache_update: bool,
        fancy_validate: bool,
    ) -> Result<CircuitRc> {
        Updater::new(
            transform,
            transform_along_modified_path,
            cache_transform,
            cache_transform_along_modified_path,
            cache_update,
            false,
        )
        .update(circuit, self_.crc(), Some(fancy_validate))
    }

    #[args(
        transform_along_modified_path = "Transform::ident().into()",
        cache_transform = "Updater::default().cache_transform",
        cache_transform_along_modified_path = "Updater::default().cache_transform_along_modified_path",
        cache_update = "Updater::default().cache_update",
        default_fancy_validate = "Updater::default().default_fancy_validate"
    )]
    pub fn updater(
        &self,
        transform: TransformRc,
        transform_along_modified_path: TransformRc,
        cache_transform: bool,
        cache_transform_along_modified_path: bool,
        cache_update: bool,
        default_fancy_validate: bool,
    ) -> BoundUpdater {
        Updater::new(
            transform,
            transform_along_modified_path,
            cache_transform,
            cache_transform_along_modified_path,
            cache_update,
            default_fancy_validate,
        )
        .bind(self_.crc())
    }
}
