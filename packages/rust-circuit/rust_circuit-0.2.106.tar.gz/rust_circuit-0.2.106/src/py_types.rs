use anyhow::{Context, Result};
use macro_rules_attribute::apply;
use pyo3::{
    once_cell::GILLazyPy,
    pyclass::CompareOp,
    types::{IntoPyDict, PyTuple},
};

use crate::{
    all_imports::TorchDeviceDtype,
    circuit::{EinsumAxes, HashBytes, HashBytesToPy},
    pyo3_prelude::*,
    tensor_util::Shape,
};

pub struct PyUtils {
    pub torch: PyObject,
    get_tensor_shape: PyObject,
    id: PyObject,
    pub cast_int: PyObject,
    scalar_to_tensor: PyObject,
    pub cast_tensor: PyObject,
    un_flat_concat: PyObject,
    tensor_scale: PyObject,
    pub generalfunctions: std::collections::HashMap<String, PyObject>,
    pub none: PyObject,
    einsum: PyObject,
    make_diagonal: PyObject,
    pub print: PyObject,
    pub random_indices: PyObject,
    pub conv: PyObject,
    pub tensor_to_bytes: PyObject,
    pub tensor_from_bytes: PyObject,
}

/// misc python utilities
pub static PY_UTILS: GILLazyPy<PyUtils> = GILLazyPy::new_py(|py| {
    let utils = PyModule::from_code(
        py,
        include_str!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/rust_circuit_type_utils.py"
        )),
        concat!(env!("CARGO_MANIFEST_DIR"), "/rust_circuit_type_utils.py"),
        "rust_circuit_type_utils",
    )
    .unwrap();

    let get = |s: &str| utils.getattr(s).unwrap().into();

    PyUtils {
        torch: get("torch"),
        get_tensor_shape: get("get_tensor_shape"),
        id: get("get_id"),
        cast_int: get("cast_int"),
        scalar_to_tensor: get("scalar_to_tensor"),
        cast_tensor: get("cast_tensor"),
        un_flat_concat: get("un_flat_concat"),
        tensor_scale: get("tensor_scale"),
        generalfunctions: utils
            .getattr("generalfunctions")
            .unwrap()
            .extract()
            .unwrap(),
        none: get("none"),
        einsum: get("einsum"),
        make_diagonal: get("make_diagonal"),
        print: get("print"),
        random_indices: get("random_indices"),
        conv: get("conv"),
        tensor_to_bytes: get("tensor_to_bytes"),
        tensor_from_bytes: get("tensor_from_bytes"),
    }
});

pub fn py_address(x: &PyObject) -> usize {
    Python::with_gil(|py| {
        PY_UTILS
            .id
            .call(py, (x,), None)
            .unwrap()
            .extract(py)
            .unwrap()
    })
}

#[macro_export]
macro_rules! make_py_func {
    {
        #[py_ident($py:ident)]
        $( #[$m:meta] )*
        $vi:vis fn $name:ident($($arg_name:ident : $arg_ty:ty),* $(,)?) -> $ret_ty:ty
        { $($tt:tt)* }
    } => {
        paste::paste!{
            $(#[$m])*
            $vi fn [<$name _py>]<'py>($py : Python<'py>, $($arg_name : $arg_ty,)*) -> $ret_ty {
                $($tt)*
            }
            $(#[$m])* // TODO: maybe shouldn't apply to both??
            $vi fn $name($($arg_name : $arg_ty,)*) -> $ret_ty {
                Python::with_gil(|py| [<$name _py>](py, $($arg_name,)*))
            }
        }

    };
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn scalar_to_tensor(v: f64, shape: Shape, device_dtype: TorchDeviceDtype) -> Result<Tensor> {
    PY_UTILS
        .scalar_to_tensor
        .call(py, (v, shape, device_dtype), None)
        .context("scalar to tensor")?
        .extract::<Tensor>(py)
        .context("scalar to tensor extract")
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn einsum(items: Vec<(Tensor, EinsumAxes)>, out_axes: EinsumAxes) -> PyResult<Tensor> {
    PY_UTILS
        .einsum
        .call(py, (items, out_axes), None)?
        .extract(py)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn make_diagonal(
    non_diag: &Tensor,
    out_axes_deduped: EinsumAxes,
    out_axes: EinsumAxes,
) -> PyResult<Tensor> {
    PY_UTILS
        .make_diagonal
        .call(py, (non_diag, out_axes_deduped, out_axes), None)?
        .extract(py)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn einops_repeat(
    tensor: &Tensor,
    op: String,
    sizes: impl IntoIterator<Item = (String, u64)>,
) -> Result<Tensor> {
    PY_EINOPS
        .repeat
        .call(py, (tensor, op), Some(sizes.into_py_dict(py)))
        .context("einops repeat")?
        .extract(py)
        .context("einops repeat extract")
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn un_flat_concat(tensor: &Tensor, split_shapes: Vec<Shape>) -> PyResult<Vec<Tensor>> {
    PY_UTILS
        .un_flat_concat
        .call(py, (tensor, split_shapes), None)
        .context("un flat concat")?
        .extract(py)
}

#[apply(make_py_func)]
#[py_ident(py)]
pub fn tensor_scale(tensor: &Tensor) -> PyResult<f64> {
    PY_UTILS.tensor_scale.call(py, (tensor,), None)?.extract(py)
}

pub struct PyEinops {
    pub einops: Py<PyModule>,
    pub repeat: PyObject,
}

pub static PY_EINOPS: GILLazyPy<PyEinops> = GILLazyPy::new_py(|py| {
    let einops = PyModule::import(py, "einops").unwrap();
    let get = |s: &str| einops.getattr(s).unwrap().into();

    PyEinops {
        einops: einops.into(),
        repeat: get("repeat"),
    }
});

pub static HASH_TENSOR: GILLazyPy<(PyObject, PyObject)> = GILLazyPy::new_py(|py| {
    let module = PyModule::from_code(
        py,
        include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/tensor_hash.py")),
        concat!(env!("CARGO_MANIFEST_DIR"), "/tensor_hash.py"),
        "tensor_hash",
    )
    .unwrap();
    (
        module.getattr("hash_tensor").unwrap().into(),
        module.getattr("pop_cuda_context").unwrap().into(),
    )
});

#[macro_export]
macro_rules! pycall {
    ($f:expr,$args:expr) => {
        Python::with_gil(|py| $f.call(py, $args, None).unwrap().extract(py).unwrap())
    };
    ($f:expr, $args:expr, anyhow) => {
        Python::with_gil(|py| {
            $f.call(py, $args, None)
                .map_err(|z| anyhow::Error::from(z))?
                .extract(py)
                .map_err(|z| anyhow::Error::from(z))
        })
    };
}

macro_rules! generate_extra_py_ops {
    [$($op:ident),*] => {
        paste::paste! {
            struct PyOperators {
                $($op: PyObject,)*
            }

            static PY_OPERATORS: GILLazyPy<PyOperators> = GILLazyPy::new_py(|py| {
                let operator = PyModule::import(py, "operator").unwrap();

                PyOperators {
                    $( $op : operator.getattr(stringify!($op)).unwrap().into(),)*
                }
            });


            /// Trait for python operator methods when they return the same type.
            /// Used for tensors.
            ///
            /// Not useful when an operator returns a different type: this will
            /// always raise an error (e.g. dict).
            ///
            /// # Example
            ///
            /// ```
            /// # use pyo3::prelude::*;
            /// # use rust_circuit::py_types::ExtraPySelfOps;
            ///
            /// #[derive(Clone, Debug, FromPyObject)]
            /// struct WrapInt(i64);
            ///
            /// impl IntoPy<PyObject> for WrapInt {
            ///     fn into_py(self, py: Python<'_>) -> PyObject {
            ///         self.0.into_py(py)
            ///     }
            /// }
            ///
            /// impl ExtraPySelfOps for WrapInt {}
            ///
            /// pyo3::prepare_freethreaded_python();
            ///
            /// assert_eq!(
            ///     Python::with_gil(|py| WrapInt(8).py_add(py, 7)).unwrap().0,
            ///     7 + 8
            /// );
            /// assert_eq!(
            ///     Python::with_gil(|py| WrapInt(2).py_mul(py, 3)).unwrap().0,
            ///     2 * 3
            /// );
            /// ```
            pub trait ExtraPySelfOps
            where
                Self: IntoPy<PyObject>,
                for<'a> Self: FromPyObject<'a>,
            {
                $(
                    fn [<py_ $op>]<'a>(self, py: Python<'a>, x: impl IntoPy<PyObject>) -> PyResult<Self> {
                        PY_OPERATORS.$op.call1(py, (self, x))?.extract(py)
                    }

                    // not sure if this method should exist
                    fn [<py_ $op _acquire>]<'a>(self, x: impl IntoPy<PyObject>) -> PyResult<Self> {
                        Python::with_gil(|py| self.[<py_ $op>](py, x))
                    }
                )*
            }
        }
    }
}

// add more as needed
generate_extra_py_ops!(add, getitem, mul);

#[derive(Debug, Clone)]
pub struct Tensor {
    tensor: PyObject,
    shape: Shape, /* cache shape so doesn't have to be recomputed on reconstruct etc (not uber efficient I think) */
    hash: Option<HashBytes>,
}

impl PartialEq for Tensor {
    fn eq(&self, other: &Self) -> bool {
        if let Some(a)=self.hash && let Some(b)=other.hash{
            a==b
        }else{
            false
        }
    }
}

impl Eq for Tensor {}

impl<'source> FromPyObject<'source> for Tensor {
    fn extract(tensor: &'source PyAny) -> PyResult<Self> {
        let shape =
            Python::with_gil(|py| PY_UTILS.get_tensor_shape.call1(py, (tensor,))?.extract(py))?;

        Ok(Self {
            tensor: tensor.into(),
            shape,
            hash: None,
        })
    }
}

impl IntoPy<PyObject> for &Tensor {
    fn into_py(self, _py: Python<'_>) -> PyObject {
        self.tensor.clone()
    }
}
impl IntoPy<PyObject> for Tensor {
    fn into_py(self, _py: Python<'_>) -> PyObject {
        self.tensor
    }
}

impl ExtraPySelfOps for Tensor {}

impl Tensor {
    pub fn tensor(&self) -> &PyObject {
        &self.tensor
    }

    pub fn shape(&self) -> &Shape {
        &self.shape
    }

    pub fn ndim(&self) -> usize {
        self.shape.len()
    }

    pub fn hash(&self) -> Option<&HashBytes> {
        self.hash.as_ref()
    }

    pub fn flatten(&self) -> Tensor {
        Python::with_gil(|py| {
            self.tensor
                .call_method(py, "flatten", (), None)
                .unwrap()
                .extract(py)
                .unwrap()
        })
    }

    /// DANGEROUS
    pub fn set_hash(&mut self, hash: Option<HashBytes>) {
        self.hash = hash;
    }

    pub fn hash_usize(&self) -> Option<usize> {
        self.hash.as_ref().map(|x| {
            let mut hash_prefix: [u8; 8] = Default::default();
            hash_prefix.copy_from_slice(&x[..8]);
            usize::from_le_bytes(hash_prefix)
        })
    }

    pub fn hashed(&self) -> Tensor {
        if self.hash.is_some() {
            self.clone()
        } else {
            Self {
                tensor: self.tensor.clone(),
                shape: self.shape.clone(),
                hash: Python::with_gil(|py| {
                    HASH_TENSOR
                        .0
                        .call(py, (self.tensor.clone(),), None)
                        .unwrap()
                        .extract(py)
                        .unwrap()
                }),
            }
        }
    }
}

#[pyfunction]
pub fn hash_tensor(t: Tensor) -> HashBytesToPy {
    (*t.hashed().hash().unwrap()).into()
}

#[derive(FromPyObject)]
pub struct PyShape(pub Shape);

impl IntoPy<PyObject> for PyShape {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PyTuple::new(py, self.0).into_py(py)
    }
}

#[derive(FromPyObject)]
pub struct PyEinsumAxes(pub EinsumAxes);

impl IntoPy<PyObject> for PyEinsumAxes {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PyTuple::new(py, self.0).into_py(py)
    }
}

pub fn use_rust_comp<T: PartialOrd>(l: &T, r: &T, comp_op: CompareOp) -> bool {
    match comp_op {
        CompareOp::Lt => l < r,
        CompareOp::Gt => l > r,
        CompareOp::Le => l <= r,
        CompareOp::Ge => l >= r,
        CompareOp::Eq => l == r,
        CompareOp::Ne => l != r,
    }
}

#[macro_export]
macro_rules! make_single_many {
    ($name:ident, $type:ty, $container:ident) => {
        #[derive(Clone, FromPyObject)]
        pub enum $name {
            Single($type),
            Many($container<$type>),
        }

        impl $name {
            pub fn into_many(self) -> $container<$type> {
                match self {
                    Self::Single(x) => [x].into_iter().collect(),
                    Self::Many(many) => many,
                }
            }

            pub fn len(&self) -> usize {
                match self {
                    Self::Single(_) => 1,
                    Self::Many(many) => many.len(),
                }
            }
        }
    };
}

make_single_many!(PyOpAtAxes, i64, Vec);

pub fn reduction_to_ints(x: Option<PyOpAtAxes>, ndim: usize) -> Vec<i64> {
    x.map(|x| x.into_many())
        .unwrap_or_else(|| (0..ndim as i64).collect())
}
