use pyo3::{
    types::{PyModule, PyType},
    Py, PyResult, PyTypeInfo, Python,
};

use crate::{
    circuit::{
        batching::BatchError,
        expand_node::ExpandError,
        sample_transform::SampleError,
        scheduled_execution::{SchedulingError, SchedulingOOMError},
        ConstructError, ParseError, TensorEvalError,
    },
    rearrange_spec::{PermError, RearrangeParseError, RearrangeSpecError},
    tensor_util::{IndexError, MiscInputError},
};

pub fn py_get_type<T: PyTypeInfo>() -> Py<PyType> {
    Python::with_gil(|py| T::type_object(py).into())
}

pub trait HasPythonException {
    fn get_python_exception_type(&self) -> Py<PyType>;
    fn register(py: Python<'_>, m: &PyModule) -> PyResult<()>;
    fn print_stub(py: Python<'_>) -> PyResult<String>;
}

#[macro_export]
macro_rules! python_error_exception {
    (
        #[base_error_name($e_name:ident)]
        #[base_exception($base_ty:ty)]
        // #[error_py_description($desc:literal)]
        $( #[$($meta_tt:tt)*] )*
        $vis:vis enum $name:ident {
            $(
                $(#[$($meta_tt_item:tt)*])*
                $err_name:ident {
                    $($inside:tt)*
                },
            )*
        }
    ) => {
        $( #[$($meta_tt)*] )*
        $vis enum $name {
            $(
                $(#[$($meta_tt_item)*])*
                $err_name { $($inside)* },
            )*
        }

        paste::paste! {
            type [<__ $name BaseExcept>] = $base_ty;
            mod [< __ $name:snake _python_exception_stuff>] {
                $crate::python_error_exception! {
                    @in_mod $vis $name {
                        $(
                            $err_name [[<$e_name $err_name Error>]],
                        )*
                    }
                    ([<$e_name Error>] super::[<__ $name BaseExcept>]
                     // $desc
                     )
                }
            }

            #[allow(dead_code)]
            $vis type [<Py $e_name Error>] = [< __ $name:snake _python_exception_stuff>]::[<$e_name Error>];
            $(
            #[allow(dead_code)]
            $vis type  [<Py $e_name $err_name Error>] = [< __ $name:snake _python_exception_stuff>]::[<$e_name $err_name Error>];
            )*
        }
    };
    (@op_name [] $name:ident) => {
        $name
    };
    (@op_name [$e_name:ident] $name:ident) => {
        paste::paste! {
            [<$e_name Error>]
        }
    };
    (
        @in_mod $vis:vis $name:ident {
            $(
                $err_name:ident [$sub_excep_name:ident],
            )*
        }
        ($excep_name:ident $base_ty:ty
         // $desc:literal
         )
    ) => {
        use pyo3::{
            create_exception,
            types::{PyModule, PyType},
            PyTypeInfo,
            Py, PyResult, Python,
        };

        use $crate::{
            error::{py_get_type, HasPythonException},
        };

        create_exception!(
            rust_circuit,
            $excep_name,
            $base_ty
            //, $desc
        );
        $(
            create_exception!(
                rust_circuit,
                $sub_excep_name,
                $excep_name
            );
        )*

        impl HasPythonException for super::$name {
            fn get_python_exception_type(&self) -> Py<PyType> {
                use super::$name::*;
                match self {
                    $(
                        $err_name { .. } => {
                            py_get_type::<$sub_excep_name>()
                        },
                    )*
                }
            }
            fn register(py: Python<'_>, m: &PyModule) -> PyResult<()> {
                m.add(
                    stringify!($excep_name),
                    py.get_type::<$excep_name>(),
                )?;
                $(
                    m.add(
                        stringify!($sub_excep_name),
                        py.get_type::<$sub_excep_name>(),
                    )?;
                )*

                Ok(())
            }
            fn print_stub(py : Python<'_>) -> PyResult<String> {
                let out = [
                    format!("class {}({}): ...", $excep_name::NAME, <$base_ty>::type_object(py).name()?),
                    $(
                        format!("class {}({}): ...", $sub_excep_name::NAME, $excep_name::NAME),
                    )*
                ].join("\n");
                Ok(out)
            }
        }
    }
}

macro_rules! setup_errors {
    ($($t:ty),* $(,)?) => {
        pub fn get_exception(err: &anyhow::Error) -> Option<Py<PyType>> {
            if let Some(x) = pyo3::anyhow::get_exception_from_base_error(err) {
                return Some(x);
            }
            $(
                if let Some(x) = err.root_cause().downcast_ref::<$t>() {
                    return Some(x.get_python_exception_type());
                }
            )*
            None
        }
        pub fn register_exceptions(py: Python<'_>, m: &PyModule) -> PyResult<()> {
            $(
                <$t>::register(py, m)?;
            )*
            Ok(())
        }
        pub fn print_exception_stubs(py : Python<'_>) -> PyResult<String> {
            let out = [
                $(
                    <$t>::print_stub(py)?,
                )*
            ].join("\n");
            Ok(out)
        }
    };
}

setup_errors!(
    BatchError,
    ConstructError,
    ExpandError,
    MiscInputError,
    ParseError,
    RearrangeSpecError,
    PermError,
    RearrangeParseError,
    SchedulingError,
    SchedulingOOMError,
    TensorEvalError,
    SampleError,
    IndexError,
);
