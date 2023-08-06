use circuit_base::{circuit_utils::count_nodes, CircuitRc, ModuleNode};
#[pyfunction]
pub fn elim_empty_module(circuit: &ModuleNode) -> Option<CircuitRc> {
    if count_nodes(circuit.spec.spec_circuit.clone()) == 1 {
        return Some(circuit.nodes[0].clone());
    }
    return None;
}
use pyo3::prelude::*;
