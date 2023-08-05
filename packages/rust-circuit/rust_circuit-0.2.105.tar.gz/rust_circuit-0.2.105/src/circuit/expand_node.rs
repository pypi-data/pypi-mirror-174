use std::iter::zip;

use anyhow::{bail, Context, Result};
use macro_rules_attribute::apply;
use pyo3::exceptions::PyValueError;
use rustc_hash::FxHashMap as HashMap;
use thiserror::Error;

use super::{prelude::*, Add, Concat, GeneralFunction, Index, ModuleNode, Rearrange, Scatter};
use crate::{
    all_imports::{TensorAxisIndex, TensorIndex},
    circuit::{deep_map_fallible_pre_new_children, Einsum},
    pycall,
    pyo3_prelude::*,
    python_error_exception, sv,
    tensor_util::Shape,
};

#[pyfunction]
#[pyo3(name = "expand_node")]
pub fn expand_node_py(circuit: CircuitRc, inputs: Vec<CircuitRc>) -> Result<CircuitRc> {
    expand_node(circuit, &inputs)
}

pub fn expand_node(circuit: CircuitRc, inputs: &Vec<CircuitRc>) -> Result<CircuitRc> {
    if inputs.len() != circuit.children().count() {
        bail!(ExpandError::WrongNumChildren {
            expected: circuit.children().count(),
            got: inputs.len(),
        });
    }
    let batch_ranks: Vec<usize> = zip(circuit.children(), inputs)
        .filter_map(|(old, new)| new.info().rank().checked_sub(old.info().rank()))
        .collect();
    if batch_ranks.len() != inputs.len() {
        bail!(ExpandError::BatchingRankTooLow {
            default: circuit.children().map(|x| x.info().rank()).collect(),
            got: inputs.iter().map(|x| x.info().rank()).collect(),
        });
    }
    let batch_shapes: Vec<&[usize]> = zip(&batch_ranks, inputs)
        .map(|(br, new)| &new.info().shape[0..*br])
        .collect();
    match &**circuit {
        Circuit::Symbol(_) | Circuit::ScalarConstant(_) => Ok(circuit.clone()),
        Circuit::Rearrange(node) => {
            let input_shape_non_batch = inputs[0].info().shape[batch_ranks[0]..]
                .iter()
                .cloned()
                .collect();
            let new_spec = node
                .spec
                .conform_to_input_shape(&input_shape_non_batch, true)
                .context("failed to conform rearrange to input shape in expand")?
                .add_batch_dims(batch_ranks[0]);
            Ok(Rearrange::nrc(
                inputs[0].clone(),
                new_spec,
                circuit.name_cloned(),
            ))
        }
        Circuit::Index(node) => {
            // for now non-batch non-identity dims can't change
            for i in 0..node.node.info().rank() {
                if node.node.info().shape[i] != inputs[0].info().shape[i + batch_ranks[0]]
                    && node.index.0[i] != TensorAxisIndex::IDENT
                {
                    bail!(ExpandError::FixedIndex {
                        index: node.index.clone(),
                        old_shape: node.node.info().shape.clone(),
                        new_shape: inputs[0].info().shape.clone(),
                    });
                }
            }
            Ok(Index::nrc(
                inputs[0].clone(),
                TensorIndex(
                    vec![TensorAxisIndex::IDENT; batch_ranks[0]]
                        .into_iter()
                        .chain(node.index.0.iter().cloned())
                        .collect(),
                ),
                node.name_cloned(),
            ))
        }
        Circuit::Scatter(node) => {
            // for now non-batch non-identity dims can't change
            for i in 0..node.node.info().rank() {
                if node.node.info().shape[i] != inputs[0].info().shape[i + batch_ranks[0]]
                    && node.index.0[i] != TensorAxisIndex::IDENT
                {
                    bail!(ExpandError::FixedIndex {
                        index: node.index.clone(),
                        old_shape: node.node.info().shape.clone(),
                        new_shape: inputs[0].info().shape.clone(),
                    });
                }
            }
            Ok(Scatter::nrc(
                inputs[0].clone(),
                TensorIndex(
                    vec![TensorAxisIndex::IDENT; batch_ranks[0]]
                        .into_iter()
                        .chain(node.index.0.iter().cloned())
                        .collect(),
                ),
                inputs[0].info().shape[0..batch_ranks[0]]
                    .iter()
                    .cloned()
                    .chain(node.info().shape.iter().cloned())
                    .collect(),
                node.name_cloned(),
            ))
        }
        Circuit::Concat(node) => {
            if !batch_shapes.iter().all(|x| x == &batch_shapes[0]) {
                bail!(ExpandError::InconsistentBatches {
                    batch_shapes: batch_shapes
                        .iter()
                        .map(|x| x.iter().cloned().collect())
                        .collect(),
                    circuit: circuit.clone(),
                });
            }
            if !zip(&node.nodes, zip(inputs, &batch_ranks)).all(|(old, (new, br))| {
                old.info().shape[node.axis] == new.info().shape[node.axis + br]
            }) {
                bail!(ExpandError::ConcatAxis {
                    axis: node.axis,
                    old_shape: sv![],
                    new_shape: sv![],
                });
            }
            Concat::try_new(
                inputs.clone(),
                node.axis + batch_ranks[0],
                node.name_cloned(),
            )
            .map(|x| x.rc())
        }
        Circuit::Add(node) => Add::try_new(inputs.clone(), node.name_cloned()).map(|x| x.rc()),
        Circuit::GeneralFunction(node) => {
            GeneralFunction::try_new(inputs.clone(), node.spec.clone(), node.name_cloned())
                .map(|x| x.rc())
        }
        Circuit::Einsum(node) => {
            let mut batch_shape: Option<&[usize]> = None;
            for bs in &batch_shapes {
                if !bs.is_empty() {
                    if let Some(existing) = batch_shape {
                        if *bs != existing {
                            bail!(ExpandError::InconsistentBatches {
                                batch_shapes: batch_shapes
                                    .iter()
                                    .map(|x| x.iter().cloned().collect())
                                    .collect(),
                                circuit: circuit.clone(),
                            });
                        }
                    } else {
                        batch_shape = Some(bs.clone());
                    }
                }
            }
            let next_axis = node.next_axis();
            let newies = || (next_axis as u8..next_axis + batch_shape.unwrap().len() as u8);
            let out_axes = if let Some(_bs) = batch_shape {
                newies().chain(node.out_axes.iter().cloned()).collect()
            } else {
                node.out_axes.clone()
            };
            Einsum::try_new(
                node.args
                    .iter()
                    .enumerate()
                    .map(|(i, (_child, ints))| {
                        (inputs[i].clone(), {
                            if !batch_shapes[i].is_empty() {
                                newies().chain(ints.iter().cloned()).collect()
                            } else {
                                ints.clone()
                            }
                        })
                    })
                    .collect(),
                out_axes,
                node.name_cloned(),
            )
            .map(|x| x.rc())
        }
        Circuit::ModuleNode(node) => {
            ModuleNode::try_new(inputs.clone(), node.spec.clone(), node.name_cloned())
                .map(|z| z.rc())
        }
        _ => {
            if inputs[..] == circuit.children().collect::<Vec<_>>()[..] {
                Ok(circuit.clone())
            } else {
                bail!(ExpandError::NodeUnhandledVariant {
                    variant: circuit.variant_string(),
                })
            }
        }
    }
}

#[apply(python_error_exception)]
#[base_error_name(Expand)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ExpandError {
    #[error("expand wrong number of children, expected {expected} got {got}")]
    WrongNumChildren { expected: usize, got: usize },

    #[error("Batching Rank Too Low")]
    BatchingRankTooLow {
        default: Vec<usize>,
        got: Vec<usize>,
    },

    #[error("Trying to expand fixed index, index {index:?} old shape{old_shape:?} new shape {new_shape:?}")]
    FixedIndex {
        index: TensorIndex,
        old_shape: Shape,
        new_shape: Shape,
    },

    #[error(
        "Trying to expand concat axis, index {axis} old shape{old_shape:?} new shape {new_shape:?}"
    )]
    ConcatAxis {
        axis: usize,
        old_shape: Shape,
        new_shape: Shape,
    },

    #[error("Inputs that should have same batching have different batchings, {batch_shapes:?} {circuit:?}")]
    InconsistentBatches {
        batch_shapes: Vec<Shape>,
        circuit: CircuitRc,
    },

    #[error("trying to expand node, unknown variant {variant}")]
    NodeUnhandledVariant { variant: String },
}

#[pyfunction]
#[pyo3(name = "replace_expand_bottom_up_dict")]
pub fn replace_expand_bottom_up_dict_py(
    circuit: CircuitRc,
    dict: HashMap<CircuitRc, CircuitRc>,
) -> Result<CircuitRc> {
    replace_expand_bottom_up(circuit, |x| dict.get(&x).cloned())
}

#[pyfunction]
#[pyo3(name = "replace_expand_bottom_up")]
pub fn replace_expand_bottom_up_py(circuit: CircuitRc, f: PyObject) -> Result<CircuitRc> {
    replace_expand_bottom_up(circuit, |x| pycall!(f, (x.clone(),)))
}

pub fn replace_expand_bottom_up<F>(circuit: CircuitRc, replacer: F) -> Result<CircuitRc>
where
    F: Fn(CircuitRc) -> Option<CircuitRc>,
{
    let recursor = |circuit: CircuitRc, new_children: &Vec<CircuitRc>| -> Result<CircuitRc> {
        if let Some(replaced) = replacer(circuit.clone()) {
            return Ok(replaced);
        }
        expand_node(circuit, new_children)
    };
    deep_map_fallible_pre_new_children(circuit, recursor)
}
