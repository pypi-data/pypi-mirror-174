use std::collections::HashSet;

use anyhow::{anyhow, bail, Result};
use macro_rules_attribute::apply;

use super::{IterateMatchResults, IterativeMatcherRc, Transform, TransformData, TransformRc};
use crate::{
    cached_method,
    circuit::{expand_node::expand_node, CircuitNode, CircuitRc, HashBytes},
    pyo3_prelude::*,
};

#[pyclass]
#[derive(Debug, Clone)]
pub struct Updater {
    #[pyo3(get)]
    pub(super) transform: TransformRc,
    #[pyo3(get)]
    pub(super) transform_along_modified_path: TransformRc,
    #[pyo3(get)]
    pub(super) cache_transform: bool,
    #[pyo3(get)]
    pub(super) cache_transform_along_modified_path: bool,
    #[pyo3(get)]
    pub(super) cache_update: bool,
    #[pyo3(get, set)]
    pub(super) default_fancy_validate: bool,
    pub(super) transform_cache: cached::UnboundCache<HashBytes, CircuitRc>,
    pub(super) transform_along_modified_path_cache: cached::UnboundCache<HashBytes, CircuitRc>,
    pub(super) updated_cache: cached::UnboundCache<(HashBytes, IterativeMatcherRc), CircuitRc>,
    pub(super) validation_getter: Getter,
}

impl Default for Updater {
    fn default() -> Self {
        Self {
            transform: Transform::ident().into(),
            transform_along_modified_path: Transform::ident().into(),
            cache_transform: true,
            cache_transform_along_modified_path: true,
            cache_update: true,
            default_fancy_validate: false,
            transform_cache: cached::UnboundCache::new(),
            transform_along_modified_path_cache: cached::UnboundCache::new(),
            updated_cache: cached::UnboundCache::new(),
            validation_getter: Default::default(),
        }
    }
}

#[pymethods]
impl Updater {
    #[new]
    #[args(
        transform_along_modified_path = "Transform::ident().into()",
        cache_transform = "Updater::default().cache_transform",
        cache_transform_along_modified_path = "Updater::default().cache_transform_along_modified_path",
        cache_update = "Updater::default().cache_update",
        default_fancy_validate = "Updater::default().default_fancy_validate"
    )]
    pub fn new(
        transform: TransformRc,
        transform_along_modified_path: TransformRc,
        cache_transform: bool,
        cache_transform_along_modified_path: bool,
        cache_update: bool,
        default_fancy_validate: bool,
    ) -> Self {
        Self {
            transform,
            transform_along_modified_path,
            cache_transform,
            cache_transform_along_modified_path,
            cache_update,
            default_fancy_validate,
            ..Default::default()
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.update(circuit, matcher, fancy_validate)
    }

    pub fn update(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        if fancy_validate.unwrap_or(self.default_fancy_validate) {
            self.validation_getter
                .validate(circuit.clone(), matcher.clone())?;
        }
        self.update_impl(circuit, matcher)
    }

    pub fn bind(&self, matcher: IterativeMatcherRc) -> BoundUpdater {
        BoundUpdater {
            updater: self.clone(),
            matcher,
        }
    }
}

impl Updater {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matcher.clone()))]
    #[use_try]
    #[cache_expr(updated_cache)]
    fn update_impl(
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
            let new_matcher = updated.unwrap_or(matcher);
            new_circuit = circuit.map_children(|c| self_.update_impl(c, new_matcher.clone()))?;
        }
        if found {
            if !matches!(self_.transform.data(), TransformData::Ident) {
                new_circuit = self_.run_transform(new_circuit)?;
            }
        } else if !matches!(
            self_.transform_along_modified_path.data(),
            TransformData::Ident
        ) && new_circuit != circuit
        {
            new_circuit = self_.run_transform_along_modified_path(new_circuit)?;
        }

        Ok(new_circuit)
    }

    #[apply(cached_method)]
    #[self_id(self_)]
    #[key(circuit.info().hash)]
    #[use_try]
    #[cache_expr(transform_cache)]
    fn run_transform(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        self_.transform.run(circuit)
    }

    // macro to dedup as desired
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key(circuit.info().hash)]
    #[use_try]
    #[cache_expr(transform_along_modified_path_cache)]
    fn run_transform_along_modified_path(&mut self, circuit: CircuitRc) -> Result<CircuitRc> {
        self_.transform_along_modified_path.run(circuit)
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct BoundUpdater {
    #[pyo3(get, set)]
    pub updater: Updater,
    #[pyo3(get, set)]
    pub matcher: IterativeMatcherRc,
}

#[pymethods]
impl BoundUpdater {
    #[new]
    pub fn new(updater: Updater, matcher: IterativeMatcherRc) -> Self {
        Self { updater, matcher }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.update(circuit, fancy_validate)
    }

    pub fn update(
        &mut self,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.updater
            .update(circuit, self.matcher.clone(), fancy_validate)
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Getter {
    #[pyo3(get, set)]
    pub(super) default_fancy_validate: bool,
    pub(super) cache: cached::UnboundCache<(HashBytes, IterativeMatcherRc), HashSet<CircuitRc>>,
}

impl Default for Getter {
    fn default() -> Self {
        Self {
            default_fancy_validate: false,
            cache: cached::UnboundCache::new(),
        }
    }
}

#[pymethods]
impl Getter {
    #[new]
    #[args(default_fancy_validate = "Getter::default().default_fancy_validate")]
    pub fn new(default_fancy_validate: bool) -> Self {
        Self {
            default_fancy_validate,
            ..Default::default()
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<HashSet<CircuitRc>> {
        self.get(circuit, matcher, fancy_validate)
    }

    pub fn get(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<HashSet<CircuitRc>> {
        let out = self.get_impl(circuit, matcher.clone())?;
        if fancy_validate.unwrap_or(self.default_fancy_validate) {
            matcher.validate_matched(&out)?;
        }
        Ok(out)
    }

    pub fn get_unique_op(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<Option<CircuitRc>> {
        let out = self.get(circuit, matcher, fancy_validate)?;
        if out.len() > 1 {
            bail!("found {} matches which is > 1", out.len());
        }
        Ok(out.into_iter().next())
    }

    pub fn get_unique(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.get_unique_op(circuit, matcher, fancy_validate)?
            .ok_or_else(|| anyhow!("found no matches!"))
    }

    pub fn validate(&mut self, circuit: CircuitRc, matcher: IterativeMatcherRc) -> Result<()> {
        self.get(circuit, matcher, Some(true))?;
        Ok(())
    }

    pub fn bind(&self, matcher: IterativeMatcherRc) -> BoundGetter {
        BoundGetter {
            getter: self.clone(),
            matcher,
        }
    }

    // TODO: add support for paths as needed!
}

impl Getter {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matcher.clone()))]
    #[use_try]
    #[cache_expr(cache)]
    fn get_impl(
        &mut self,
        circuit: CircuitRc,
        matcher: IterativeMatcherRc,
    ) -> Result<HashSet<CircuitRc>> {
        let IterateMatchResults {
            updated,
            finished,
            found,
        } = matcher.match_iterate(circuit.clone())?;

        let mut out = HashSet::new();
        if found {
            out.insert(circuit.clone());
        }
        if !finished {
            let new_matcher = updated.unwrap_or(matcher);
            for child in circuit.children() {
                out.extend(self_.get_impl(child, new_matcher.clone())?);
            }
        }
        Ok(out)
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct BoundGetter {
    #[pyo3(get, set)]
    pub getter: Getter,
    #[pyo3(get, set)]
    pub matcher: IterativeMatcherRc,
}

#[pymethods]
impl BoundGetter {
    #[new]
    pub fn new(getter: Getter, matcher: IterativeMatcherRc) -> Self {
        Self {
            getter,
            matcher: matcher.into(),
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<HashSet<CircuitRc>> {
        self.get(circuit, fancy_validate)
    }

    pub fn get(
        &mut self,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<HashSet<CircuitRc>> {
        self.getter
            .get(circuit, self.matcher.clone(), fancy_validate)
    }

    pub fn get_unique_op(
        &mut self,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<Option<CircuitRc>> {
        self.getter
            .get_unique_op(circuit, self.matcher.clone(), fancy_validate)
    }

    pub fn get_unique(
        &mut self,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.getter
            .get_unique(circuit, self.matcher.clone(), fancy_validate)
    }

    pub fn validate(&mut self, circuit: CircuitRc) -> Result<()> {
        self.getter.validate(circuit, self.matcher.clone())
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Batcher {
    /// Note: we don't currently cache these transforms individually. We could
    /// do this.
    #[pyo3(get)]
    pub(super) replacements: Vec<TransformRc>,
    /// Technically, having all of these matchers stored here isn't important
    /// for key functionality (like unused for caching).
    /// This is just nice for calling from python.
    ///
    /// invariant: replacements.len() == matchers.len()
    #[pyo3(get)]
    pub(super) matchers: Vec<IterativeMatcherRc>,
    #[pyo3(set, get)]
    pub ban_multiple_matches_on_node: bool,
    #[pyo3(set, get)]
    pub default_fancy_validate: bool,
    #[pyo3(get)]
    pub(super) suffix: Option<String>,
    pub(super) batch_cache: cached::UnboundCache<(HashBytes, Vec<IterativeMatcherRc>), CircuitRc>,
    pub(super) validation_getter: Getter,
}

impl Default for Batcher {
    fn default() -> Self {
        Self {
            replacements: Vec::new(),
            matchers: Vec::new(),
            ban_multiple_matches_on_node: false,
            default_fancy_validate: false,
            suffix: None,
            batch_cache: cached::UnboundCache::new(),
            validation_getter: Default::default(),
        }
    }
}

#[pymethods]
impl Batcher {
    #[new]
    #[args(
        batchers = "*",
        ban_multiple_matches_on_node = "Batcher::default().ban_multiple_matches_on_node",
        default_fancy_validate = "Batcher::default().default_fancy_validate",
        suffix = "None"
    )]
    pub fn new(
        batchers: Vec<(IterativeMatcherRc, TransformRc)>,
        ban_multiple_matches_on_node: bool,
        default_fancy_validate: bool,
        suffix: Option<String>,
    ) -> Self {
        let (matchers, replacements) = batchers
            .into_iter()
            .map(|(a, b)| (a.into(), b.into()))
            .unzip();
        Self {
            replacements,
            matchers,
            ban_multiple_matches_on_node,
            default_fancy_validate,
            suffix,
            ..Default::default()
        }
    }

    fn __call__(
        &mut self,
        _py: Python<'_>,
        circuit: CircuitRc,
        fancy_validate: Option<bool>,
    ) -> Result<CircuitRc> {
        self.batch(circuit, fancy_validate)
    }

    pub fn batch(&mut self, circuit: CircuitRc, fancy_validate: Option<bool>) -> Result<CircuitRc> {
        if fancy_validate.unwrap_or(self.default_fancy_validate) {
            for m in &self.matchers {
                self.validation_getter
                    .validate(circuit.clone(), m.clone())?;
            }
        }
        self.batch_impl(circuit, self.matchers.clone())
    }
}

impl Batcher {
    #[apply(cached_method)]
    #[self_id(self_)]
    #[key((circuit.info().hash, matchers.clone()))]
    #[use_try]
    #[cache_expr(batch_cache)]
    fn batch_impl(
        &mut self,
        circuit: CircuitRc,
        matchers: Vec<IterativeMatcherRc>,
    ) -> Result<CircuitRc> {
        let results = matchers
            .iter()
            .map(|m| m.match_iterate(circuit.clone()))
            .collect::<Result<Vec<_>>>()?;

        let filtered = results.iter().enumerate().filter(|(_, res)| res.found);

        if let Some((idx, _)) = filtered.clone().next() {
            if self_.ban_multiple_matches_on_node {
                let n_matches = filtered.count();
                if n_matches != 1 {
                    bail!("multiple matches! got {} != 1", n_matches);
                }
            }

            return self_.replacements[idx].run(circuit);
        }

        if results.iter().all(|x| x.finished) {
            return Ok(circuit);
        }

        let new_matchers: Vec<_> = results
            .into_iter()
            .zip(matchers)
            .map(|(res, matcher)| res.updated.unwrap_or(matcher))
            .collect();

        let new_children = circuit
            .children()
            .map(|c| self_.batch_impl(c, new_matchers.clone()))
            .collect::<Result<_>>()?;

        Ok(expand_node(circuit, &new_children)?.add_suffix(self_.suffix.as_ref().map(|x| &**x)))
    }

    pub fn suffix(&self) -> Option<&str> {
        self.suffix.as_ref().map(|x| &**x)
    }
}
