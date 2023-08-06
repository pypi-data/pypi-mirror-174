#![allow(clippy::borrow_deref_ref)]
use std::{
    collections::BTreeMap,
    fmt::Debug,
    hash::Hash,
    iter::zip,
    ops::{Deref, DerefMut},
    sync::Arc,
};

use anyhow::{Context, Result};
pub use computational_node::{
    flat_concat, flat_concat_back, Add, Concat, Conv, Einsum, EinsumAxes, Index, Rearrange, Scatter,
};
pub use constant::{ArrayConstant, ScalarConstant, Symbol};
pub use cumulant::Cumulant;
pub use generalfunction::{GeneralFunction, GeneralFunctionSpec, PyGFSpecShapeGetter};
pub use generalfunction_rewrite::{
    generalfunction_merge_inverses, generalfunction_special_case_simplification,
};
use macro_rules_attribute::apply;
pub use module_nodes::{ModuleNode, ModuleNodeArgSpec, ModuleNodeSpec};
use num_bigint::BigUint;
pub use parsing::{parse_compiler_repr_bijection, parse_compiler_repr_bijection_py, ParseError};
use py_circuit_items::circuit_rust_to_py;
use pyo3::{
    exceptions::{self, PyValueError},
    pyclass::CompareOp,
    types::PyBytes,
    PyTypeInfo,
};
use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};
use thiserror::Error;
use uuid::uuid;
pub use variable_nodes::{AutoTag, DiscreteVar, StoredCumulantVar};

use crate::{
    all_imports::{PyCountsAtAxes, RInnerInts},
    cached_lambda,
    circuit::circuit_utils::toposort_circuit,
    eq_by_big_hash::EqByBigHash,
    py_types::{reduction_to_ints, use_rust_comp, PyOpAtAxes, PyShape, Tensor},
    pycall, pycallable,
    pyo3_prelude::*,
    python_error_exception,
    rearrange_spec::{OpSize, RearrangeSpec},
    simple_from, sv,
    tensor_util::{
        check_canon_idxs, Shape, TensorAxisIndex, TensorIndex, TorchDeviceDtype, TorchDeviceDtypeOp,
    },
    util::{arc_ref_clone, arc_unwrap_or_clone, AsOp, AxisInt},
};

pub mod algebraic_rewrite;
pub mod batching;
pub mod canonicalize;
pub mod circuit_manipulation;
pub mod circuit_optimizer;
pub mod circuit_utils;
pub mod compiler_heuristics;
pub mod compiler_strip;
mod computational_node;
pub mod concat_rewrite;
mod constant;
pub mod cumulant;
pub mod debugging;
pub mod deep_rewrite;
pub mod diag_rewrite;
pub mod expand_node;
pub mod generalfunction;
pub mod generalfunction_rewrite;
pub mod get_update;
pub mod module_nodes;
pub mod module_rewrite;
pub mod named_axes;
pub mod nb_rewrites;
pub mod nrc;
mod parsing;
pub mod print;
pub mod py_circuit_items;
mod repr;
pub mod sample_transform;
pub mod sampling;
pub mod scatter_rewrite;
pub mod schedule_send;
pub mod scheduled_execution;
pub mod scheduling_z3;
pub mod variable_nodes;

mod circuit_node_private {
    use super::{CachedCircuitInfo, Result};
    pub trait CircuitNodePrivate {
        fn info_mut(&mut self) -> &mut CachedCircuitInfo;
        fn name_mut(&mut self) -> &mut Option<String>;
    }

    pub trait CircuitNodeInit {
        fn init_info_impl(self) -> Result<Self>
        where
            Self: Sized;

        fn rename_impl(self, new_name: Option<String>) -> Self
        where
            Self: Sized;

        fn update_info_impl<F>(self, f: F) -> Result<Self>
        where
            Self: Sized,
            F: FnOnce(&mut CachedCircuitInfo);
    }
}
use circuit_node_private::*;

use self::circuit_utils::total_arrayconstant_size;

impl<T: CircuitNodePrivate + CircuitNode> CircuitNodeInit for T {
    fn init_info_impl(mut self) -> Result<Self>
    where
        Self: Sized,
    {
        self.info_mut().shape = self.compute_shape(); // set shape so methods to compute other info can use it

        let mut hasher = self.compute_hash();
        self.info_mut().named_axes = self.compute_named_axes();
        hasher.update(self.name().unwrap_or("").as_bytes());
        hasher.update(&self.node_type_uuid());
        hasher.update(uuid!("025e9af4-1366-4211-aa5f-7c28fc6cdf9f").as_bytes());
        for (axis, name) in &self.info().named_axes {
            if *axis as usize >= self.info().shape.len() {
                return Err(ConstructError::NamedAxisAboveRank {}.into());
            }
            hasher.update(&[*axis]);
            hasher.update(name.as_bytes());
        }
        self.info_mut().is_constant = self.compute_is_constant();
        self.info_mut().is_explicitly_computable = self.compute_is_explicitly_computable();
        self.info_mut().can_be_sampled = self.compute_can_be_sampled();
        self.info_mut().hash = hasher.finalize().into();
        self.info_mut().max_non_input_size = self.max_non_input_size();
        self.info_mut().device_dtype = self.compute_device_dtype()?;
        Ok(self)
    }

    fn rename_impl(mut self, new_name: Option<String>) -> Self
    where
        Self: Sized,
    {
        *self.name_mut() = new_name;
        self.init_info_impl().unwrap() // we could avoid recomputing some stuff if we wanted
    }

    fn update_info_impl<F>(mut self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnOnce(&mut CachedCircuitInfo),
    {
        f(self.info_mut());
        self.init_info_impl()
    }
}

use self::{
    circuit_utils::total_flops,
    print::{print_circuit_stats, repr_circuit_deep_compiler},
};

fn check_canon_axes(rank: usize, axes: &[i64]) -> Result<Vec<usize>> {
    check_canon_idxs(rank, axes).context("axis out of bounds")
}
fn check_canon_axes_as(rank: usize, axes: &[i64]) -> Result<RInnerInts> {
    Ok(check_canon_axes(rank, axes)?
        .into_iter()
        .map(|x| x as u8)
        .collect())
}

pub type NamedAxes = BTreeMap<AxisInt, String>;
pub trait CircuitNode: CircuitNodeInit {
    // ==== implementable section ===
    //
    // NOTE: ALL FNS IN THIS SECTION *MUST* BE COPIED TO THE CIRCUIT NODE UNION IMPL!
    // If you add something here with a default impl, write a new impl for circuit node union!
    // (up until default section)
    //
    // we could enforce this sort of stuff with some proc macros, but seems like overkill atm.

    fn info(&self) -> &CachedCircuitInfo;
    fn name(&self) -> Option<&str>;

    fn compute_shape(&self) -> Shape;
    fn compute_hash(&self) -> blake3::Hasher; // shouldn't hash name
    fn compute_is_constant(&self) -> bool {
        self.children().all(|c| c.info().is_constant)
    }
    fn compute_is_explicitly_computable(&self) -> bool {
        self.children().all(|c| c.info().is_explicitly_computable)
    }
    fn compute_can_be_sampled(&self) -> bool {
        self.children().all(|c| c.info().can_be_sampled)
    }

    fn device_dtype_extra<'a>(&'a self) -> Box<dyn Iterator<Item = TorchDeviceDtypeOp> + 'a> {
        Box::new(std::iter::empty())
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>>;

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a>;

    fn map_children_enumerate<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>;

    fn node_type_uuid(&self) -> [u8; 16];

    fn self_flops(&self) -> BigUint {
        BigUint::from(0usize)
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor>;

    /// At most how many elements will evaluating this circuit require allocating
    /// new memory (that we are allowed to free ourselves) for? Used to improve scheduling.
    fn intermediate_cost_bound(&self) -> usize {
        self.info().numel_usize()
    }

    fn c(self) -> Circuit;
    fn rc(self) -> CircuitRc;
    fn init_info(self) -> Result<Self>
    where
        Self: Sized,
    {
        self.init_info_impl()
    }
    fn rename(self, new_name: Option<String>) -> Self
    where
        Self: Sized,
    {
        self.rename_impl(new_name)
    }
    fn update_info<F>(self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnOnce(&mut CachedCircuitInfo),
    {
        self.update_info_impl(f)
    }

    // ==== default section ===
    // FUNCTIONS BELOW HERE *shouldn't* be overridden by implementors!
    // (if you do implement, this won't be picked up on by union types!)

    fn crc(&self) -> CircuitRc
    where
        Self: Clone,
    {
        self.clone().rc()
    }
    fn name_cloned(&self) -> Option<String> {
        self.name().map(|x| x.to_owned())
    }

    fn compute_device_dtype(&self) -> Result<TorchDeviceDtypeOp> {
        self.children()
            .map(|c| c.info().device_dtype.clone())
            .chain(self.device_dtype_extra())
            .fold(Ok(TorchDeviceDtypeOp::NONE), |acc, new| {
                acc.map(|old| TorchDeviceDtypeOp::combine(old, new))?
            })
    }

    fn compute_named_axes(&self) -> NamedAxes {
        if !self.info().named_axes.is_empty() {
            return self.info().named_axes.clone();
        }
        if !self.children().any(|x| !x.info().named_axes.is_empty()) {
            return BTreeMap::new();
        }
        let child_axis_map = self.child_axis_map();
        let mut result: NamedAxes = BTreeMap::new();
        for (mp, child) in zip(child_axis_map, self.children()) {
            for (ax, name) in &child.info().named_axes {
                if let Some(top_ax) = mp[(*ax) as usize] {
                    result.insert(top_ax as u8, name.clone());
                }
            }
        }
        result
    }

    fn map_children<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> Result<CircuitRc>,
    {
        self.map_children_enumerate(|_i, x| f(x))
    }

    fn map_children_idxs<F>(&self, mut f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize) -> Result<CircuitRc>,
    {
        self.map_children_enumerate(|i, _x| f(i))
    }

    fn map_children_unwrap<F>(&self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> CircuitRc,
    {
        self.map_children(|x| Ok(f(x))).unwrap()
    }

    fn map_children_unwrap_enumerate<F>(&self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> CircuitRc,
    {
        self.map_children_enumerate(|i, x| Ok(f(i, x))).unwrap()
    }

    fn map_children_unwrap_idxs<F>(&self, mut f: F) -> Self
    where
        Self: Sized,
        F: FnMut(usize) -> CircuitRc,
    {
        self.map_children_enumerate(|i, _x| Ok(f(i))).unwrap()
    }

    /// if any return Some, return child mapped, otherwise None
    fn map_children_op<F>(&self, mut f: F) -> Option<Self>
    where
        Self: Sized,
        F: FnMut(CircuitRc) -> Option<CircuitRc>,
    {
        let mut any_modified = false;
        let out = self.map_children_unwrap(|x| {
            if let Some(new) = f(x.clone()) {
                any_modified = true;
                new
            } else {
                x
            }
        });
        if any_modified {
            Some(out)
        } else {
            None
        }
    }

    fn max_non_input_size(&self) -> BigUint {
        self.children()
            .map(|x| x.info().max_non_input_size.clone())
            .chain(std::iter::once(self.info().numel()))
            .max()
            .unwrap_or(0usize.into())
    }

    fn compiler_repr(&self) -> String
    where
        Self: Clone,
    {
        repr_circuit_deep_compiler(&self.clone().c(), false, false)
    }

    fn compiler_print(&self)
    where
        Self: Clone,
    {
        crate::python_println!("{}", self.compiler_repr())
    }

    fn get_hash(&self) -> HashBytes {
        self.info().hash
    }

    fn rank(&self) -> usize {
        self.info().rank()
    }
    fn ndim(&self) -> usize {
        self.info().rank()
    }
    fn shape(&self) -> &Shape {
        &self.info().shape
    }
    fn numel(&self) -> usize {
        self.info().numel_usize()
    }

    fn sum(&self, axes: &[i64], name: Option<String>) -> Result<Einsum>
    where
        Self: Clone,
    {
        let axes = check_canon_axes_as(self.info().rank(), axes)?;
        Ok(Einsum::new(
            vec![(self.crc(), (0u8..self.info().rank() as u8).collect())],
            (0u8..self.info().rank() as u8)
                .filter(|i| !axes.contains(&i))
                .collect(),
            name,
        ))
    }

    fn mean(&self, axes: &[i64], name: Option<String>) -> Result<Einsum>
    where
        Self: Clone,
    {
        let total_size: usize = check_canon_axes_as(self.info().rank(), axes)?
            .into_iter()
            .map(|i| self.info().shape[i as usize])
            .product();
        self.sum(axes, name)?.mul(
            ScalarConstant::nrc(1. / (total_size as f64), sv![], None),
            None,
        )
    }

    fn reduce(&self, op_name: String, axes: &[i64], name: Option<String>) -> Result<Circuit>
    where
        Self: Clone,
    {
        match op_name.as_str() {
            "mean" => return self.mean(axes, name).map(CircuitNode::c),
            "sum" => return self.sum(axes, name).map(CircuitNode::c),
            _ => (),
        }

        let axes = check_canon_axes_as(self.info().rank(), axes)?;

        Ok(GeneralFunction::new_by_name(
            vec![Rearrange::nrc(
                self.crc(),
                RearrangeSpec::combine_axes_at_end(self.info().rank().try_into()?, axes).unwrap(),
                None,
            )],
            op_name,
            name,
        )
        .unwrap()
        .c())
    }
    fn min_(&self, axes: &[i64], name: Option<String>) -> Result<Circuit>
    where
        Self: Clone,
    {
        self.reduce("min".to_owned(), axes, name)
    }
    fn max_(&self, axes: &[i64], name: Option<String>) -> Result<Circuit>
    where
        Self: Clone,
    {
        self.reduce("max".to_owned(), axes, name)
    }
    fn add(&self, other: CircuitRc, name: Option<String>) -> Result<Add>
    where
        Self: Clone,
    {
        Add::try_new(vec![self.crc(), other], name)
    }
    fn sub(&self, other: CircuitRc, name: Option<String>) -> Result<Add>
    where
        Self: Clone,
    {
        self.add(Einsum::scalar_mul(other, -1.0, None).rc(), name)
    }
    fn mul(&self, other: CircuitRc, name: Option<String>) -> Result<Einsum>
    where
        Self: Clone,
    {
        Einsum::elementwise_broadcasted(vec![self.crc(), other], name)
    }
    fn mul_scalar(
        &self,
        scalar: f64,
        name: Option<String>,
        scalar_name: Option<String>,
    ) -> Result<Einsum>
    where
        Self: Clone,
    {
        self.mul(ScalarConstant::nrc(scalar, sv![], scalar_name), name)
    }
    fn index(&self, index: TensorIndex, name: Option<String>) -> Result<Index>
    where
        Self: Clone,
    {
        Index::try_new(self.crc(), index, name)
    }
    fn expand_at_axes(
        &self,
        axes: Vec<usize>,
        counts: Vec<usize>,
        name: Option<String>,
    ) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::expand_at_axes(self.info().rank(), axes, counts)?,
            name,
        ))
    }
    fn unsqueeze(&self, axes: Vec<usize>, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unsqueeze(self.info().rank(), axes)?,
            name,
        ))
    }
    fn flatten(&self, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::flatten_usize(self.ndim())?,
            name,
        ))
    }
    fn unflatten(&self, shape: Shape, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Rearrange::unflatten(self.crc(), shape, name)
    }
    fn unflatten_axis(&self, axis: i64, shape: Shape, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unflatten_axis(self.ndim(), axis, shape)?,
            name,
        ))
    }
    fn unflatten_axis_usize(
        &self,
        axis: usize,
        shape: Shape,
        name: Option<String>,
    ) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Ok(Rearrange::new(
            self.crc(),
            RearrangeSpec::unflatten_axis_usize(self.ndim(), axis, shape)?,
            name,
        ))
    }
    fn rearrange(&self, spec: RearrangeSpec, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Rearrange::try_new(self.crc(), spec, name)
    }
    fn rearrange_str(&self, string: &str, name: Option<String>) -> Result<Rearrange>
    where
        Self: Clone,
    {
        Rearrange::from_einops_string(self.crc(), string, name)
    }
    fn add_suffix(self, suffix: Option<&str>) -> Self
    where
        Self: Sized,
    {
        match suffix {
            Some(suffix) => {
                let name = self.name().map(|x| format!("{}_{}", x, suffix));
                self.rename_impl(name)
            }
            None => self,
        }
    }
}

pub trait CircuitNodeAutoName: CircuitNode {
    fn auto_name(&self, name: Option<String>) -> Option<String>;
}

impl<T: CircuitNode> EqByBigHash for T {
    fn hash(&self) -> HashBytes {
        self.info().hash
    }
}

pub trait CircuitNodeDefer: CircuitNodeInit {
    fn as_trait_obj(&self) -> &dyn CircuitNode;
    fn map_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>;
    fn custom_c(self) -> Circuit;
    fn custom_rc(self) -> CircuitRc;
}

pub trait CircuitNodeUnion {
    type TypeTag;
    fn variant_string(&self) -> String;
    fn type_tag(&self) -> Self::TypeTag;
}

// not really needed to be so pedantic with ::std::...
#[macro_export]
macro_rules! circuit_node_eq_ord {
    ($type_name:ty) => {
        $crate::impl_eq_by_big_hash!($type_name);

        impl ::std::cmp::Ord for $type_name {
            fn cmp(&self, other: &Self) -> ::std::cmp::Ordering {
                use $crate::circuit::prelude::*;
                // name and then
                (self.name(), self.info().hash).cmp(&(other.name(), other.info().hash))
            }
        }

        impl ::std::cmp::PartialOrd for $type_name {
            fn partial_cmp(&self, other: &Self) -> ::std::option::Option<::std::cmp::Ordering> {
                Some(::std::cmp::Ord::cmp(self, other))
            }
        }
    };
}

// this is what peak rust development looks like
#[doc(hidden)]
#[macro_export]
macro_rules! define_circuit_union_impl {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        #[derive(::std::fmt::Debug, ::std::clone::Clone)]
        #[cfg_attr(feature = "real-pyo3", derive($crate::pyo3::FromPyObject))]
        pub enum $name {
            $(
                $x($x),
            )*
        }

        #[cfg(not(feature = "real-pyo3"))]
        impl<'source> $crate::pyo3::FromPyObject<'source> for $name {
            fn extract(_: &'source $crate::pyo3::PyAny) -> $crate::pyo3::PyResult<Self> {
                unimplemented!()
            }
        }

        paste::paste! {
            #[derive(Debug, Clone, Copy, Eq, PartialEq, Hash, PartialOrd, Ord)]
            pub enum [<$name Type>] {
                $(
                    $x,
                )*
            }


            impl<'source> $crate::pyo3::FromPyObject<'source> for [<$name Type>] {
                fn extract(inp: &'source $crate::pyo3::PyAny) -> $crate::pyo3::PyResult<Self> {
                    use $crate::pyo3::{ types::PyType};

                    let pairings: Vec<(Py<PyType>, [<$name Type>])> =
                        Python::with_gil(|py| vec![
                        $(
                            ($x::type_object(py).into(), [<$name Type>]::$x),
                        )*
                        ]);

                    for (t, out) in pairings {
                        if t.is(inp) {
                            return Ok(out);
                        }
                    }

                    Err(PyErr::new::<exceptions::PyTypeError, _>(format!(
                        "Expected one of the {} types",
                        stringify!($name)
                    )))
                }
            }

            impl $crate::pyo3::IntoPy<$crate::pyo3::PyObject> for [<$name Type>] {
                fn into_py(self, py: $crate::pyo3::Python<'_>) -> $crate::pyo3::PyObject {
                    match self {
                        $(
                            Self::$x => $x::type_object(py).into(),
                        )*
                    }
                }
            }

        }


        $crate::circuit_node_eq_ord!($name);

        paste::paste! {
            $(
                impl $name {
                    pub fn [<into_ $x:snake>](self) -> Option<$crate::circuit::$x> {
                        self.into_op()
                    }
                    pub fn [<as_ $x:snake>](&self) -> Option<&$crate::circuit::$x> {
                        self.as_op()
                    }
                    pub fn [<as_mut_ $x:snake>](&mut self) -> Option<&mut $crate::circuit::$x> {
                        self.as_mut_op()
                    }

                    pub fn [<into_ $x:snake _unwrap>](self) -> $crate::circuit::$x {
                        self.into_unwrap()
                    }
                    pub fn [<as_ $x:snake _unwrap>](&self) -> &$crate::circuit::$x {
                        self.as_unwrap()
                    }
                    pub fn [<as_mut_ $x:snake _unwrap>](&mut self) -> &mut $crate::circuit::$x {
                        self.as_mut_unwrap()
                    }

                    pub fn [<is_ $x:snake>](&self) -> bool {
                        self.[<as_ $x:snake>]().is_some()
                    }
                }
                impl AsOp<$crate::circuit::$x> for $name {
                    fn into_op(self) -> Option<$crate::circuit::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                    fn as_op(&self) -> Option<&$crate::circuit::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                    fn as_mut_op(&mut self) -> Option<&mut $crate::circuit::$x> {
                        if let Self::$x(node) = self {
                            Some(node)
                        } else {
                            None
                        }
                    }
                }
            )*
        }

        impl $crate::circuit::CircuitNodeInit for $name {
            fn init_info_impl(self) -> Result<Self> {
                match self {
                    $(
                        Self::$x(node) => Ok(Self::$x(node.init_info()?)),
                    )*
                }
            }

            fn rename_impl(self, new_name: Option<String>) -> Self {
                match self {
                    $(
                        Self::$x(node) => Self::$x(node.rename(new_name)),
                    )*
                }
            }

            fn update_info_impl<F>(self, f: F) -> Result<Self>
            where
                F: FnOnce(&mut $crate::circuit::CachedCircuitInfo),
            {
                match self {
                    $(
                        Self::$x(node) => Ok(Self::$x(node.update_info(f)?)),
                    )*
                }
            }
        }

        impl $crate::circuit::CircuitNodeDefer for $name {
            #[inline] // hopefully inlined away?
            fn as_trait_obj(&self) -> &dyn $crate::circuit::CircuitNode {
                match self {
                    $(
                        Self::$x(node) => node,
                    )*
                }
            }

            fn map_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
            where
                F: FnMut(usize,$crate::circuit::CircuitRc) -> Result<$crate::circuit::CircuitRc>,
            {
                match self {
                    $(
                        Self::$x(node) => $crate::circuit::CircuitNode::map_children_enumerate(node, f).map(|v| Self::$x(v)),
                    )*
                }
            }

            fn custom_c(self) -> $crate::circuit::Circuit {
                match self {
                    $(
                        Self::$x(node) => node.c(),
                    )*
                }
            }

            fn custom_rc(self) -> $crate::circuit::CircuitRc {
                match self {
                    $(
                        Self::$x(node) => node.rc(),
                    )*
                }
            }
        }

        paste::paste! {
            impl $crate::circuit::CircuitNodeUnion for $name {
                type TypeTag = [<$name Type>];

                fn variant_string(&self) -> String {
                    match self {
                        $(
                            Self::$x(_) => stringify!($x).to_owned(),
                        )*
                    }
                }

                fn type_tag(&self) -> Self::TypeTag {
                    match self {
                        $(
                            Self::$x(_) => Self::TypeTag::$x,
                        )*
                    }
                }
            }
        }

        $(
            impl From<$x> for $name {
                fn from(item: $x) -> Self {
                    Self::$x(item)
                }
            }
        )*

        impl $crate::pyo3::IntoPy<$crate::pyo3::PyObject> for $name {
            fn into_py(self, py: $crate::pyo3::Python<'_>) -> $crate::pyo3::PyObject {
                #[cfg(feature = "real-pyo3")]
                match self {
                    $(
                        Self::$x(node) => $crate::pyo3::IntoPy::into_py(node, py),
                    )*
                }

                #[cfg(not(feature = "real-pyo3"))]
                unimplemented!()
            }
        }
    }
}

macro_rules! define_circuit {
    [$($x:ident),+ $(,)?] => {
        define_circuit_union_impl!(Circuit {$($x,)*});

        // you have to wrap pymethods in the paste for this to work due to how
        // pymethods proc macro works
        paste::paste! {
            #[pymethods]
            impl PyCircuitBase {
            $(
                pub fn [<as_ $x:snake>](&self) -> Option<$crate::circuit::$x> {
                    arc_ref_clone(&self).into_op()
                }

                pub fn [<as_ $x:snake _unwrap>](&self) -> $crate::circuit::$x {
                    arc_ref_clone(&self).into_unwrap()
                }

                pub fn [<is_ $x:snake>](&self) -> bool {
                    self.0.[<is_ $x:snake>]()
                }
            )*
            }
        }

    }
}

define_circuit!(
    Einsum,
    ArrayConstant,
    Symbol,
    ScalarConstant,
    Add,
    Rearrange,
    Index,
    GeneralFunction,
    Concat,
    Scatter,
    Conv,
    ModuleNode,
    AutoTag,
    DiscreteVar,
    StoredCumulantVar,
    Cumulant,
);

#[pyfunction]
pub fn print_circuit_type_check(x: CircuitType) -> CircuitType {
    dbg!(x);
    x
}

/// Define adhoc unions of different circuit types
#[macro_export]
macro_rules! define_circuit_union {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        $crate::define_circuit_union_impl!($name {$($x,)*});

        impl ::std::convert::From<$name> for $crate::circuit::Circuit {
            fn from(item: $name) -> Self {
                match item {
                    $(
                        $name::$x(node) => node.into(),
                    )*
                }
            }
        }
        impl ::std::convert::From<$crate::circuit::Circuit> for ::std::option::Option<$name> {
            fn from(item: $crate::circuit::Circuit) -> ::std::option::Option<$name> {
                match item {
                    $(
                        $crate::circuit::Circuit::$x(node) => Some(node.into()),
                    )*
                    _=>None
                }
            }
        }
        impl $name{
            pub fn matches(circuit:&$crate::circuit::Circuit)->bool{
                let op: ::std::option::Option<$name>=circuit.clone().into();
                op.is_some()
            }
        }
        paste::paste! {
            fn [<circuit_is_ $name:snake>](circuit: &$crate::circuit::Circuit) -> bool {
                match circuit {
                    $(
                        $crate::circuit::Circuit::$x(_) => true,
                    )*
                    _ => false
                }
            }

            #[pyfunction]
            #[pyo3(name="circuit_is_" $name:snake)]
            pub fn [<circuit_is_ $name:snake _py>](circuit: $crate::circuit::CircuitRc) -> bool {
                [<circuit_is_ $name:snake>](&circuit)
            }
        }
    }
}

macro_rules! define_circuit_union_special {
    [$name:ident {$($x:ident),+ $(,)?}] => {
        define_circuit_union!($name {$($x,)*});
        paste::paste! {
            impl Circuit {
                pub fn [<is_ $name:snake>](&self) -> bool {
                    [<circuit_is_ $name:snake>](self)
                }
                pub fn [<into_ $name:snake>](self) -> Option<$name> {
                    self.into()
                }
            }
        }
    }
}

// These nodes are uneffected by rewrites, and satisfy
// AlgebraicRewrite(Replace(X, IrreducibleNode->Y)) == Replace(AlgebraicRewrite(IrreducibleNode), IrreducibleNode->Y)
// except for hashmap iteration order or other unfortunate nondeterminism
define_circuit_union_special!(IrreducibleNode {
    ArrayConstant,
    Symbol,
});

define_circuit_union_special!(Leaf {
    ArrayConstant,
    Symbol,
    ScalarConstant,
});

define_circuit_union_special!(LeafConstant {
    ArrayConstant,
    ScalarConstant,
});

define_circuit_union_special!(Var {
    StoredCumulantVar,
    DiscreteVar,
});

// work around for fact that we can't implement foreign trait on constrained type
#[macro_export]
macro_rules! circuit_node_extra_impl {
    ($type_name:ident) => {
        $crate::circuit_node_eq_ord!($type_name);

        impl $crate::circuit::CircuitNodePrivate for $type_name {
            fn info_mut(&mut self) -> &mut $crate::circuit::CachedCircuitInfo {
                &mut self.info
            }
            fn name_mut(&mut self) -> &mut Option<String> {
                &mut self.name
            }
        }

        #[cfg(feature = "real-pyo3")]
        impl $type_name {
            fn into_init(self) -> PyClassInitializer<Self> {
                // kinda awkward clone... (but probably basically free)
                (self.clone(), $crate::circuit::PyCircuitBase(self.rc())).into()
            }
        }

        impl IntoPy<PyObject> for $type_name {
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

#[macro_export]
macro_rules! circuit_node_auto_impl {
    ($the_uuid:literal) => {
        fn info(&self) -> &$crate::circuit::CachedCircuitInfo {
            &self.info
        }
        fn name(&self) -> Option<&str> {
            self.name.as_deref()
        }
        fn node_type_uuid(&self) -> [u8; 16] {
            *uuid::uuid!($the_uuid).as_bytes()
        }
        fn c(self) -> $crate::circuit::Circuit {
            self.into()
        }
        fn rc(self) -> $crate::circuit::CircuitRc {
            $crate::circuit::CircuitRc(std::sync::Arc::new(self.c()))
        }
    };
}

// UPDATE ME WHEN YOU CHANGE CircuitNode Trait!!!
impl<T: CircuitNodeDefer> CircuitNode for T {
    fn info(&self) -> &CachedCircuitInfo {
        self.as_trait_obj().info()
    }

    fn name(&self) -> Option<&str> {
        self.as_trait_obj().name()
    }

    fn compute_shape(&self) -> Shape {
        self.as_trait_obj().compute_shape()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let hasher = self.as_trait_obj().compute_hash();
        hasher
    }

    fn compute_is_constant(&self) -> bool {
        self.as_trait_obj().compute_is_constant()
    }

    fn compute_is_explicitly_computable(&self) -> bool {
        self.as_trait_obj().compute_is_explicitly_computable()
    }

    fn compute_can_be_sampled(&self) -> bool {
        self.as_trait_obj().compute_can_be_sampled()
    }

    fn device_dtype_extra<'a>(&'a self) -> Box<dyn Iterator<Item = TorchDeviceDtypeOp> + 'a> {
        self.as_trait_obj().device_dtype_extra()
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        self.as_trait_obj().child_axis_map()
    }

    fn children<'a>(&'a self) -> Box<dyn Iterator<Item = CircuitRc> + 'a> {
        self.as_trait_obj().children()
    }

    fn map_children_enumerate<F>(&self, f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        self.map_children_enumerate_impl(f)
    }

    fn node_type_uuid(&self) -> [u8; 16] {
        self.as_trait_obj().node_type_uuid()
    }

    fn self_flops(&self) -> BigUint {
        self.as_trait_obj().self_flops()
    }

    fn eval_tensors(&self, tensors: &[Tensor], device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
        self.as_trait_obj().eval_tensors(tensors, device_dtype)
    }

    fn intermediate_cost_bound(&self) -> usize {
        self.as_trait_obj().intermediate_cost_bound()
    }

    fn c(self) -> Circuit {
        self.custom_c()
    }

    fn rc(self) -> CircuitRc {
        self.custom_rc()
    }
}

pub type HashBytes = [u8; 32];

#[derive(FromPyObject, Copy, Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct HashBytesToPy(pub HashBytes);

simple_from!(|b: HashBytes| -> HashBytesToPy { Self(b) });
impl IntoPy<PyObject> for HashBytesToPy {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PyBytes::new(py, &self.0).into()
    }
}

#[derive(Clone, Default)]
pub struct CachedCircuitInfo {
    pub shape: Shape,
    pub is_constant: bool,
    pub is_explicitly_computable: bool,
    pub can_be_sampled: bool,
    pub hash: HashBytes,
    pub max_non_input_size: BigUint,
    pub device_dtype: TorchDeviceDtypeOp,
    pub named_axes: NamedAxes,
}

/// don't want to print hash with Debug, for now just print shape
impl Debug for CachedCircuitInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self.shape)
    }
}

impl CachedCircuitInfo {
    pub fn numel(&self) -> BigUint {
        self.shape.iter().map(|x| BigUint::from(*x)).product()
    }
    /// Saturating element count
    pub fn numel_usize(&self) -> usize {
        let numel_digits = self.numel().to_u64_digits();
        if numel_digits.len() == 1 {
            numel_digits[0] as usize
        } else {
            usize::MAX
        }
    }
    pub fn rank(&self) -> usize {
        self.shape.len()
    }
    pub fn hash_usize(&self) -> usize {
        let mut hash_prefix: [u8; 8] = Default::default();
        hash_prefix.copy_from_slice(&self.hash[..8]);
        usize::from_le_bytes(hash_prefix)
    }
}

#[apply(python_error_exception)]
#[base_error_name(Construct)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ConstructError {
    #[error("{string}")]
    NotSupportedYet { string: String },

    #[error("Conv requires stride and padding to be full size, got stride len {stride} padding len {padding}")]
    ConvStridePaddingNotFull { stride: usize, padding: usize },

    #[error("Conv input wrong shape")]
    ConvInputWrongShape {},

    #[error("Conv input wrong shape")]
    ConvFilterWrongShape {},

    #[error("Conv kernel shape must be all odd, got")]
    ConvFilterMustBeOddLength { shape: Shape },

    #[error("Conv stride must evenly divide")]
    ConvStrideMustDivide { shape: Shape, stride: Vec<usize> },

    #[error("Conv groups ({groups}) must divide input channels ({in_channels}) and output channels ({out_channels})")]
    ConvGroupsMustDivide {
        groups: usize,
        in_channels: usize,
        out_channels: usize,
    },

    #[error(
        "Conv input and filter must have same number of input channels, got {input} and {filter}"
    )]
    ConvInputFilterDifferentNumInputChannels { input: usize, filter: usize },
    #[error("DiscreteVar doesn't have leading 'samples' dim")]
    DiscreteVarNoSamplesDim {},

    #[error("DiscreteVar samples dim doesn't match probs, {node} vs {probs}")]
    DiscreteVarWrongSamplesDim { node: usize, probs: usize },

    #[error("DiscreteVar probs must be 1d with length matching samples axis 0, got probs of shape {shape:?}")]
    DiscreteVarProbsMustBe1d { shape: Shape },

    #[error("StoredCumulantVar needs first 2 cumulants specified")]
    StoredCumulantVarNeedsMeanVariance {},

    #[error("StoredCumulantVar invalid cumulant number {number}")]
    StoredCumulantVarInvalidCumulantNumber { number: usize },

    #[error("StoredCumulantVar cumulant number {cumulant_number} needs to be base shape, {base_shape:?} times cumulant number, got {cumulant_shape:?}")]
    StoredCumulantVarCumulantWrongShape {
        base_shape: Shape,
        cumulant_shape: Shape,
        cumulant_number: usize,
    },

    #[error("len shape different from len axes (len axes: {len_axes}, len shape: {circuit_len_shape}, circuit name: {circuit_name:?})")]
    EinsumLenShapeDifferentFromAxes {
        circuit_name: Option<String>,
        circuit_len_shape: usize,
        len_axes: usize,
    },
    #[error("shape different for axis (axis: {axis}, shape: {circuit_shape}, existing_shape: {existing_shape} circuit name: {circuit_name:?})")]
    EinsumShapeDifferent {
        circuit_name: Option<String>,
        circuit_shape: usize,
        axis: usize,
        existing_shape: usize,
    },
    #[error("output not subset, TODO error")]
    EinsumOutputNotSubset {
        // TODO: args
    },
    #[error("Einsum string invalid {string} {substring}")]
    EinsumStringInvalid { string: String, substring: String },

    #[error("Rearrange takes different input shape, shape: {shape:?} spec: {spec:?}")]
    RearrangeWrongInputShape { spec: RearrangeSpec, shape: Shape },

    #[error("Wrong input shapes for GeneralFunction {input_shapes:?} {gf_spec:?}")]
    GeneralFunctionWrongInputShape {
        gf_spec: GeneralFunctionSpec,
        input_shapes: Vec<Shape>,
    },

    #[error("Concat requires at least one node")]
    ConcatZeroNodes {},

    #[error("Concat nodes have different shapes {shapes:?}")]
    ConcatShapeDifferent { shapes: Vec<Shape> },

    #[error("index rank too high: {index_rank} vs {node_rank}")]
    IndexRankTooHigh { index_rank: usize, node_rank: usize },

    #[error("axis out of bounds: {axis} vs {node_rank}")]
    AxisOutOfBounds { axis: i64, node_rank: usize },

    #[error("Index {axis:?} out of bounds, index: {index:?} shape: {shape:?}. NB: Rust circuit slices don't saturate like Python ones do.")]
    IndexOutOfBounds {
        index: TensorIndex,
        shape: Shape,
        at: usize,
        axis: TensorAxisIndex,
        l: usize,
    },

    #[error("Scatter shape wrong, index: {index_shape:?} child: {shape:?} {index:?}")]
    ScatterShapeWrong {
        index: TensorIndex,
        shape: Shape,
        index_shape: Shape,
    },

    #[error("This scatter index not supported yet, {index:?}")]
    ScatterIndexTypeUnimplemented { index: TensorIndex },

    #[error("Children multiple dtypes {a:?} {b:?}")]
    ChildrenMultipleDtypes {
        a: Option<String>,
        b: Option<String>,
    },

    #[error("Children multiple dtypes {a:?} {b:?}")]
    ChildrenMultipleDevices {
        a: Option<String>,
        b: Option<String>,
    },

    #[error("Unknown GeneralFunction name {spec_name}")]
    UnknownGeneralFunction { spec_name: String },

    #[error("ModuleNode wrong number of children, expected {expected} got {got}")]
    ModuleNodeWrongNumberChildren { expected: usize, got: usize },

    #[error("ModuleNode got unknown keyword argument, {argument}")]
    ModuleNodeUnknownArgument { argument: String },

    #[error("Named axis higher than rank")]
    NamedAxisAboveRank {},

    #[error("Failed to construct equivalent explicitly computable circuit")]
    NoEquivalentExplicitlyComputable {},

    #[error("ndim={ndim}")]
    UnflattenButNDimNot1 { ndim: usize },
}

pub type CircResult = Result<CircuitRc>;

#[apply(python_error_exception)]
#[base_error_name(TensorEval)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum TensorEvalError {
    #[error("not explicitly computable: {circuit:?})")]
    NotExplicitlyComputable { circuit: CircuitRc },
    #[error("incompatible dtype circ:{circ:?} passed:{passed:?}")]
    DeviceDtypeError {
        circ: TorchDeviceDtypeOp,
        passed: TorchDeviceDtypeOp,
    },
}

#[derive(Clone, Debug, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct CircuitRc(Arc<Circuit>);

pub fn make_children_zero<T: CircuitNode>(circuit: &T) -> T {
    circuit.map_children_unwrap(&mut |child: CircuitRc| {
        ScalarConstant::new(0.0, child.info().shape.clone(), child.name_cloned()).rc()
    })
}

pub fn evaluate_fn(circ: CircuitRc) -> Result<Tensor> {
    evaluate_fn_dtype_device(circ, Default::default())
}

pub fn evaluate_fn_dtype_device(
    circ: CircuitRc,
    dtype_device: TorchDeviceDtypeOp,
) -> Result<Tensor> {
    let device_dtype = dtype_device
        .clone()
        .combine(circ.info().device_dtype.clone())
        .map_err(|_err| TensorEvalError::DeviceDtypeError {
            circ: circ.info().device_dtype.clone(),
            passed: dtype_device.clone(),
        })?
        .unwrap_or_defaults();
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<Tensor> {
        let child_tensors: Result<Vec<Tensor>> = circ.children().map(recurse).collect();
        let child_tensors = child_tensors?;

        circ.eval_tensors(&child_tensors, &device_dtype)
    }

    recurse(circ)
}

#[apply(pycallable)]
#[pyo3(name = "deep_map")]
pub fn deep_map<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn((circuit, CircuitRc)) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        let inner_mapped = circ.map_children(&mut recurse)?.rc();
        f(inner_mapped)
    }
    recurse(circuit)
}

#[apply(pycallable)]
#[pyo3(name = "deep_map_preorder")]
pub fn deep_map_preorder<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn((circuit, CircuitRc)) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        f(circ)?.map_children(&mut recurse).map(|z| z.rc())
    }
    recurse(circuit)
}

pub fn visit_circuit_with_parents<F>(circuit: CircuitRc, mut f: F)
where
    F: FnMut(CircuitRc, &Vec<CircuitRc>),
{
    let mut toposorted = toposort_circuit(circuit);
    toposorted.reverse(); // its children first by default

    let mut parents: HashMap<CircuitRc, Vec<CircuitRc>> = HashMap::default();
    for (_i, sub) in toposorted.into_iter().enumerate() {
        f(sub.clone(), parents.get(&sub).unwrap_or(&vec![]));
        for child in sub.children() {
            parents.entry(child).or_insert(vec![]).push(sub.clone());
        }
    }
}

pub fn visit_circuit_with_parents_fallible<F>(circuit: CircuitRc, mut f: F) -> Result<()>
where
    F: FnMut(CircuitRc, &Vec<CircuitRc>) -> Result<()>,
{
    let mut toposorted = toposort_circuit(circuit);
    toposorted.reverse(); // its children first by default

    let mut parents: HashMap<CircuitRc, Vec<CircuitRc>> = HashMap::default();
    for (_i, sub) in toposorted.into_iter().enumerate() {
        f(sub.clone(), parents.get(&sub).unwrap_or(&vec![]))?;
        for child in sub.children() {
            parents.entry(child).or_insert(vec![]).push(sub.clone());
        }
    }
    Ok(())
}

/// does not visit children of circuits where f fails. It does visit all children even if one fails
/// even though this is more work than stopping on the first child that fails
/// because it's semantically cleaner to not have to think about which children are first
#[apply(pycallable)]
#[pyo3(name = "visit_circuit")]
pub fn visit_circuit<F>(circuit: CircuitRc, mut f: F) -> Result<()>
where
    F: FnMut((circuit, CircuitRc)) -> Result<()>,
{
    let mut f = f;
    let mut seen: HashSet<HashBytes> = HashSet::default();

    fn recurse<F>(circ: CircuitRc, seen: &mut HashSet<HashBytes>, f: &mut F) -> Result<()>
    where
        F: FnMut(CircuitRc) -> Result<()>,
    {
        if !seen.contains(&circ.info().hash) {
            seen.insert(circ.info().hash);
            f(circ.clone())?;

            circ.children()
                .map(|child| recurse(child, seen, f))
                .collect::<Vec<_>>() // intermediate collect causes all recurses to happen even if one errors
                .into_iter()
                .collect::<Result<Vec<_>, _>>()?;
        }
        Ok(())
    }
    recurse(circuit, &mut seen, &mut f)
}

pub fn visit_circuit_postorder<F>(circuit: CircuitRc, mut f: F)
where
    F: FnMut(CircuitRc),
{
    let mut seen: HashSet<HashBytes> = HashSet::default();

    fn recurse<F>(circ: CircuitRc, seen: &mut HashSet<HashBytes>, f: &mut F)
    where
        F: FnMut(CircuitRc),
    {
        if !seen.contains(&circ.info().hash) {
            seen.insert(circ.info().hash);
            for child in circ.children() {
                recurse(child, seen, f)
            }
            f(circ);
        }
    }
    recurse(circuit, &mut seen, &mut f);
}

pub fn deep_map_op<F>(circuit: CircuitRc, f: F) -> Option<CircuitRc>
where
    F: Fn(CircuitRc) -> Option<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> Option<CircuitRc> {
        let inner_mapped = circ.map_children_op(&mut recurse).map(|z| z.rc());
        inner_mapped
            .map(|x| f(x.clone()).unwrap_or(x))
            .or_else(|| f(circ))
    }
    recurse(circuit)
}

pub fn deep_map_pre_new_children<F>(circuit: CircuitRc, f: F) -> CircuitRc
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> CircuitRc,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> CircuitRc {
        let old_children: Vec<CircuitRc> = circ.children().collect();
        let new_children = old_children.into_iter().map(recurse).collect();
        f(circ, &new_children)
    }
    recurse(circuit)
}

pub fn deep_map_op_pre_new_children<F>(circuit: CircuitRc, f: F) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> Option<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    fn recurse(circ: CircuitRc) -> Option<CircuitRc> {
        let old_children: Vec<CircuitRc> = circ.children().collect();
        let new_children: Vec<Option<CircuitRc>> =
            old_children.iter().cloned().map(recurse).collect();
        if new_children.iter().all(|x| x.is_none()) {
            f(circ, &old_children)
        } else {
            let new_real_children = zip(old_children, new_children)
                .map(|(old, new)| new.unwrap_or(old))
                .collect();
            Some(f(circ.clone(), &new_real_children).unwrap_or_else(|| {
                circ.map_children_unwrap_idxs(|i| new_real_children[i].clone())
                    .rc()
            }))
        }
    }
    recurse(circuit)
}

pub fn deep_map_fallible_pre_new_children<F>(circuit: CircuitRc, f: F) -> Result<CircuitRc>
where
    F: Fn(CircuitRc, &Vec<CircuitRc>) -> Result<CircuitRc>,
{
    #[apply(cached_lambda)]
    #[key(circ.info().hash, HashBytes)]
    #[use_try]
    fn recurse(circ: CircuitRc) -> Result<CircuitRc> {
        let old_children: Vec<CircuitRc> = circ.children().collect(); // need to define this for borrow reasons
        let new_children: Result<Vec<CircuitRc>> = old_children.into_iter().map(recurse).collect();
        new_children.and_then(|a| f(circ, &a))
    }
    recurse(circuit)
}

pub fn apply_fn_cache<I, K, O, F, FK>(i: &I, f: F, c: &mut HashMap<K, O>, fk: FK) -> O
where
    F: Fn(&I) -> O,
    FK: Fn(&I) -> K,
    O: Clone,
    K: Eq + Hash,
{
    let k = fk(i);
    match c.get(&k) {
        Some(r) => r.clone(),
        None => {
            let r = f(i);
            c.insert(k, r.clone());
            r
        }
    }
}

pub fn deep_map_op_context<F, C>(
    circuit: CircuitRc,
    f: &F,
    context: &mut C,
    self_cache: &mut HashMap<HashBytes, Option<CircuitRc>>,
) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &mut C) -> Option<CircuitRc>,
{
    if let Some(z) = self_cache.get(&circuit.info().hash) {
        return z.clone();
    }
    let inner_mapped = circuit.map_children_op(|x| deep_map_op_context(x, f, context, self_cache));
    let result = match inner_mapped {
        Some(z) => f(z.crc(), context).or(Some(z.rc())),
        None => f(circuit.clone(), context),
    };
    self_cache.insert(circuit.info().hash, result.clone());
    result
}

pub fn deep_map_op_context_preorder_stoppable<F, C>(
    circuit: CircuitRc,
    f: &F,
    context: &mut C,
    self_cache: &mut HashMap<HashBytes, Option<CircuitRc>>,
) -> Option<CircuitRc>
where
    F: Fn(CircuitRc, &mut C) -> (Option<CircuitRc>, bool),
{
    if let Some(z) = self_cache.get(&circuit.info().hash) {
        return z.clone();
    }
    let (circuit_applied, stop) = f(circuit.clone(), context);
    if stop {
        return circuit_applied;
    }
    let result = if let Some(applied) = circuit_applied {
        Some(
            applied
                .map_children_op(|x| {
                    deep_map_op_context_preorder_stoppable(x, f, context, self_cache)
                })
                .map(|x| x.rc())
                .unwrap_or(applied.clone()),
        )
    } else {
        circuit
            .map_children_op(|x| deep_map_op_context_preorder_stoppable(x, f, context, self_cache))
            .map(|x| x.rc())
    };
    self_cache.insert(circuit.info().hash, result.clone());
    result
}

pub fn evaluate_fn_uncached(circ: CircuitRc, device_dtype: &TorchDeviceDtype) -> Result<Tensor> {
    let child_tensors: Result<Vec<Tensor>> = circ
        .children()
        .map(|x| evaluate_fn_uncached(x, device_dtype))
        .collect();
    let child_tensors = child_tensors?;

    circ.eval_tensors(&child_tensors, device_dtype)
}

impl IntoPy<PyObject> for CircuitRc {
    fn into_py(self, py: Python<'_>) -> PyObject {
        #[cfg(feature = "real-pyo3")]
        {
            (*self.0).clone().into_py(py)
        }

        #[cfg(not(feature = "real-pyo3"))]
        unimplemented!()
    }
}

impl<'source> FromPyObject<'source> for CircuitRc {
    fn extract(circuit_obj: &'source PyAny) -> PyResult<Self> {
        #[cfg(feature = "real-pyo3")]
        {
            let circ: Circuit = circuit_obj.extract()?;
            Ok(circ.rc())
        }

        #[cfg(not(feature = "real-pyo3"))]
        unimplemented!()
    }
}

impl<T: CircuitNode + Into<Circuit>> From<T> for CircuitRc {
    fn from(x: T) -> Self {
        x.rc()
    }
}

impl From<Arc<Circuit>> for CircuitRc {
    fn from(x: Arc<Circuit>) -> Self {
        CircuitRc(x)
    }
}

impl Deref for CircuitRc {
    type Target = Arc<Circuit>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for CircuitRc {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl CircuitNodeInit for CircuitRc {
    fn init_info_impl(self) -> Result<Self> {
        Ok(self.c().clone().init_info()?.rc())
    }

    fn rename_impl(self, new_name: Option<String>) -> Self {
        self.c().clone().rename(new_name).rc()
    }

    fn update_info_impl<F>(self, f: F) -> Result<Self>
    where
        F: FnOnce(&mut CachedCircuitInfo),
    {
        Ok(self.c().clone().update_info_impl(f)?.rc())
    }
}

impl CircuitNodeDefer for CircuitRc {
    fn as_trait_obj(&self) -> &dyn CircuitNode {
        // deref to avoid infinite recursion
        (**self).as_trait_obj()
    }
    fn map_children_enumerate_impl<F>(&self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        (**self).map_children_enumerate(f).map(CircuitNode::rc)
    }

    fn custom_c(self) -> Circuit {
        arc_unwrap_or_clone(self.0)
    }

    // fast custom impl
    fn custom_rc(self) -> CircuitRc {
        self
    }
}

#[pyclass(subclass, name = "Circuit")]
#[derive(Clone, Debug)]
pub struct PyCircuitBase(CircuitRc);

impl Deref for PyCircuitBase {
    type Target = CircuitRc;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for PyCircuitBase {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[pymethods]
impl PyCircuitBase {
    #[getter]
    fn shape(&self) -> PyShape {
        PyShape(self.info().shape.clone())
    }

    #[getter]
    fn is_constant(&self) -> bool {
        self.info().is_constant
    }

    #[getter]
    fn is_explicitly_computable(&self) -> bool {
        self.info().is_explicitly_computable
    }

    #[getter]
    fn can_be_sampled(&self) -> bool {
        self.info().can_be_sampled
    }

    #[getter]
    fn name(&self) -> &str {
        self.0.name().unwrap_or("")
    }

    #[getter]
    fn intermediate_cost_bound(&self) -> usize {
        self.0.intermediate_cost_bound()
    }

    // TODO: probably could be more efficient...
    fn children(&self) -> Vec<CircuitRc> {
        self.0.children().collect()
    }

    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self.0, &object.0, comp_op)
    }

    fn __repr__(&self) -> String {
        self.compiler_repr(true, true)
    }

    #[getter]
    fn hash(&self) -> HashBytesToPy {
        self.info().hash.into()
    }

    #[getter]
    fn hash_base16(&self) -> String {
        base16::encode_lower(&self.info().hash)
    }

    fn __hash__(&self) -> u64 {
        self.first_u64()
    }

    pub fn self_flops(&self) -> BigUint {
        self.0.self_flops()
    }

    pub fn total_flops(&self) -> BigUint {
        total_flops((*self.0).crc())
    }

    pub fn max_non_input_size(&self) -> BigUint {
        (*self.0).info().max_non_input_size.clone()
    }

    pub fn print_stats(&self) {
        print_circuit_stats(&self.0)
    }

    #[args(bijection = "true", shape_only_necessary = "false")]
    fn compiler_repr(&self, bijection: bool, shape_only_necessary: bool) -> String {
        repr_circuit_deep_compiler(self, bijection, shape_only_necessary)
    }

    #[args(bijection = "true", shape_only_necessary = "false")]
    fn compiler_print(&self, bijection: bool, shape_only_necessary: bool) {
        crate::python_println!("{}", self.compiler_repr(bijection, shape_only_necessary))
    }

    fn numel(&self) -> BigUint {
        self.0.info().numel()
    }

    fn rank(&self) -> usize {
        self.0.info().rank()
    }
    fn ndim(&self) -> usize {
        self.rank()
    }
    #[pyo3(name = "child_axis_map")]
    fn child_axis_map_py(&self) -> Vec<Vec<Option<usize>>> {
        self.child_axis_map()
    }

    fn to_py(&self) -> PyObject {
        circuit_rust_to_py(self.0.clone())
    }

    #[args(device_dtype = "Default::default()")]
    fn evaluate(&self, device_dtype: TorchDeviceDtypeOp) -> Result<Tensor> {
        evaluate_fn_dtype_device(self.0.clone(), device_dtype)
    }

    fn map_children_enumerate(&self, f: PyObject) -> Result<CircuitRc> {
        self.0
            .map_children_enumerate(|i, child| pycall!(f, (i, child), anyhow))
    }

    fn map_children(&self, f: PyObject) -> Result<CircuitRc> {
        self.0.map_children(|child| pycall!(f, (child,), anyhow))
    }

    fn total_arrayconstant_size(&self) -> BigUint {
        total_arrayconstant_size(self.0.clone())
    }

    fn get_compatible_device_dtype(&self) -> TorchDeviceDtype {
        get_compatible_dtype(&***self)
    }

    fn rename(&self, name: Option<String>) -> CircuitRc {
        self.0.clone().rename(name)
    }
    fn add_suffix(&self, suffix: Option<&str>) -> CircuitRc {
        self.0.clone().add_suffix(suffix)
    }

    fn visit(&self, f: PyObject) -> Result<()> {
        visit_circuit_py(self.0.clone(), f)
    }

    fn reduce(
        &self,
        op_name: String,
        axis: Option<PyOpAtAxes>,
        name: Option<String>,
    ) -> Result<Circuit> {
        self.0
            .reduce(op_name, &reduction_to_ints(axis, self.info().rank()), name)
    }

    fn sum(&self, axis: Option<PyOpAtAxes>, name: Option<String>) -> Result<Einsum> {
        Ok(self
            .0
            .sum(&reduction_to_ints(axis, self.info().rank()), name)?)
    }
    fn mean(&self, axis: Option<PyOpAtAxes>, name: Option<String>) -> Result<Einsum> {
        Ok(self
            .0
            .mean(&reduction_to_ints(axis, self.info().rank()), name)?)
    }
    fn min(&self, axis: Option<PyOpAtAxes>, name: Option<String>) -> Result<CircuitRc> {
        Ok(self
            .0
            .min_(&reduction_to_ints(axis, self.info().rank()), name)?
            .rc())
    }
    fn max(&self, axis: Option<PyOpAtAxes>, name: Option<String>) -> Result<CircuitRc> {
        Ok(self
            .0
            .max_(&reduction_to_ints(axis, self.info().rank()), name)?
            .rc())
    }

    fn add(&self, other: CircuitRc, name: Option<String>) -> Result<Add> {
        self.0.add(other, name)
    }
    fn sub(&self, other: CircuitRc, name: Option<String>) -> Result<Add> {
        self.0.sub(other, name)
    }
    fn mul(&self, other: CircuitRc, name: Option<String>) -> Result<Einsum> {
        self.0.mul(other, name)
    }
    fn mul_scalar(
        &self,
        scalar: f64,
        name: Option<String>,
        scalar_name: Option<String>,
    ) -> Result<Einsum> {
        self.0.mul_scalar(scalar, name, scalar_name)
    }
    fn index(&self, index: TensorIndex, name: Option<String>) -> Result<Index> {
        self.0.index(index, name)
    }
    fn expand_at_axes(
        &self,
        axes: PyOpAtAxes,
        counts: Option<PyCountsAtAxes>,
        name: Option<String>,
    ) -> Result<Rearrange> {
        Ok(Rearrange::new(
            self.0.crc(),
            RearrangeSpec::expand_at_axes_py(self.rank(), axes, counts)?,
            name,
        ))
    }
    fn unsqueeze(&self, axes: PyOpAtAxes, name: Option<String>) -> Result<Rearrange> {
        self.expand_at_axes(axes, None, name)
    }
    fn flatten(&self, name: Option<String>) -> Result<Rearrange> {
        self.0.flatten(name)
    }
    fn unflatten(&self, shape: Shape, name: Option<String>) -> Result<Rearrange> {
        self.0.unflatten(shape, name)
    }
    fn unflatten_axis(&self, axis: i64, shape: Shape, name: Option<String>) -> Result<Rearrange> {
        self.0.unflatten_axis(axis, shape, name)
    }
    fn rearrange(&self, spec: RearrangeSpec, name: Option<String>) -> Result<Rearrange> {
        self.0.rearrange(spec, name)
    }
    fn rearrange_str(&self, string: &str, name: Option<String>) -> Result<Rearrange> {
        self.0.rearrange_str(string, name)
    }
    pub fn is_irreducible_node(&self) -> bool {
        self.0.is_irreducible_node()
    }
    pub fn is_leaf(&self) -> bool {
        self.0.is_leaf()
    }
    pub fn is_leaf_constant(&self) -> bool {
        self.0.is_leaf_constant()
    }
    pub fn is_var(&self) -> bool {
        self.0.is_var()
    }
    pub fn into_irreducible_node(&self) -> Option<IrreducibleNode> {
        self.0.clone().c().into()
    }
    pub fn into_leaf(&self) -> Option<Leaf> {
        self.0.clone().c().into()
    }
    pub fn into_leaf_constant(&self) -> Option<LeafConstant> {
        self.0.clone().c().into()
    }
    pub fn into_var(&self) -> Option<Var> {
        self.0.clone().c().into()
    }
}

pub fn get_compatible_dtype(circ: &Circuit) -> TorchDeviceDtype {
    circ.info().device_dtype.clone().unwrap_or_defaults()
}

pub mod prelude {
    pub use super::{
        Circuit, CircuitNode, CircuitNodeAutoName, CircuitNodeUnion, CircuitRc, ConstructError,
    };
}
