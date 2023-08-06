use circuit_base::{expand_node::ExpandError, ConstructError, TensorEvalError};
use circuit_rewrites::{
    batching::BatchError,
    scheduled_execution::{SchedulingError, SchedulingOOMError},
};
use get_update_node::sample_transform::SampleError;
use pyo3::{
    types::{PyModule, PyType},
    Py, PyResult, Python,
};
use rr_util::{
    errors_util::HasPythonException,
    rearrange_spec::{PermError, RearrangeParseError, RearrangeSpecError},
    tensor_util::{IndexError, MiscInputError, ParseError},
};
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
