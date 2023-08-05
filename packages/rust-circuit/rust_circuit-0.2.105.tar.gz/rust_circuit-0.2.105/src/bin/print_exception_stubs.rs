use pyo3::{PyResult, Python};

pub fn main() -> PyResult<()> {
    pyo3::prepare_freethreaded_python();
    println!("# to generate below exception stubs, `cargo run print_exception_stubs`");
    Python::with_gil(|py| -> PyResult<()> {
        println!("{}", rust_circuit::print_exception_stubs(py)?);
        Ok(())
    })
}
