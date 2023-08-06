use std::collections::BTreeMap;

use anyhow::{bail, Result};
use macro_rules_attribute::apply;
use pyo3::exceptions::PyValueError;
use thiserror::Error;

use super::{
    circuit_optimizer::OptimizationContext, named_axes::get_axis_leaves, prelude::*, Einsum, Index,
    ModuleNodeArgSpec, ModuleNodeSpec, Symbol,
};
use crate::{
    all_imports::TensorIndex,
    circuit::{
        algebraic_rewrite::einsum_nest_optimize,
        circuit_optimizer::OptimizationSettings,
        deep_map_op, deep_map_unwrap,
        named_axes::{axis_of_name, set_named_axes},
        visit_circuit_unwrap, visit_circuit_with_parents, Concat, EinsumAxes, ModuleNode,
    },
    pyo3_prelude::*,
    python_error_exception,
    set_cover::set_cover,
    tensor_util::TensorAxisIndex,
};

#[pyfunction]
pub fn batch_to_concat(circuit: CircuitRc, axis: usize, num_batches: usize) -> Result<CircuitRc> {
    let l = circuit.info().shape[axis];
    if l % num_batches != 0 {
        bail!(BatchError::NumberDoesntDivide { l, num_batches });
    }
    let batch_size = l / num_batches;
    let circuit = deep_map_unwrap(circuit, |x| {
        x.as_index()
            .map(|x| Index::slice_edges_to_none(x).rc())
            .unwrap_or(x.clone())
    });

    let (name, circuit, leaves_axis, leaves_non_axis) = get_axis_leaves(circuit, axis, true)?;
    // println!("leaves axis");
    // for (k, v) in &leaves_axis {
    //     println!("{}", v);
    //     k.compiler_print();
    // }
    // println!("leaves non axis");
    // for k in &leaves_non_axis {
    //     k.compiler_print();
    // }
    let input_specs_axis: Vec<(CircuitRc, ModuleNodeArgSpec)> = leaves_axis
        .iter()
        .map(|(sub, i)| {
            (
                sub.clone(),
                ModuleNodeArgSpec {
                    symbol: set_named_axes(
                        Symbol::new_with_random_uuid(sub.info().shape.clone(), None),
                        BTreeMap::from([(*i as u8, name.clone())]),
                    ),
                    batchable: true,
                    expandable: true,
                },
            )
        })
        .collect();
    let input_specs: Vec<(CircuitRc, ModuleNodeArgSpec)> = input_specs_axis
        .iter()
        .cloned()
        .chain(leaves_non_axis.iter().map(|sub| {
            (
                sub.clone(),
                ModuleNodeArgSpec {
                    symbol: Symbol::new_with_random_uuid(sub.info().shape.clone(), None),
                    batchable: true,
                    expandable: true,
                },
            )
        }))
        .collect();
    // println!("input_specs");
    // for is in &input_specs {
    //     is.0.compiler_print();
    // }
    if input_specs.is_empty() {
        bail!(BatchError::AxisOriginatesTooHigh {});
    }
    let module_spec =
        ModuleNodeSpec::new_extract(circuit.clone(), input_specs.clone(), None, false)
            .ok_or(BatchError::AxisOriginatesTooHigh {})?;
    // println!("module spec");
    // module_spec.spec_circuit.compiler_print();
    let module_spec = module_spec.resize(
        module_spec
            .input_specs
            .iter()
            .map(|inp_spec| {
                if let Some((c, _is)) = input_specs_axis
                    .iter()
                    .find(|(_c, spec)| spec.symbol.uuid == inp_spec.symbol.uuid)
                {
                    let mut result = c.info().shape.clone();
                    result[leaves_axis[c]] = batch_size;
                    return result;
                }
                inp_spec.symbol.info().shape.clone()
            })
            .collect(),
    )?;
    // println!("module spec after resize");
    // module_spec.spec_circuit.compiler_print();
    let concattands: Vec<CircuitRc> = (0..num_batches)
        .map(|i| {
            let new_nodes: Vec<CircuitRc> = module_spec
                .input_specs
                .iter()
                .map(|inp_spec| {
                    if let Some((c, _is)) = input_specs_axis
                        .iter()
                        .find(|z| z.1.symbol.uuid == inp_spec.symbol.uuid)
                    {
                        return Index::nrc(
                            c.clone(),
                            TensorIndex::new_single(
                                TensorAxisIndex::new_plain_slice(
                                    i * batch_size,
                                    (i + 1) * batch_size,
                                ),
                                leaves_axis[c],
                                c.info().rank(),
                            ),
                            None,
                        );
                    }
                    input_specs
                        .iter()
                        .find(|(_c, s)| s.symbol.uuid == inp_spec.symbol.uuid)
                        .unwrap()
                        .0
                        .clone()
                })
                .collect();

            // println!("module args");
            // for c in new_nodes.iter() {
            //     c.compiler_print();
            // }
            ModuleNode::nrc(new_nodes, module_spec.clone(), None)
        })
        .collect();
    let result = Concat::nrc(concattands, axis, None);
    if result.info().shape != circuit.info().shape {
        println!(
            "shapes not equal {:?} {:?}",
            result.info().shape,
            circuit.info().shape
        );
        println!("old");
        circuit.compiler_print();
        println!("new");
        result.compiler_print();
        panic!();
    }
    Ok(result)
}

#[apply(python_error_exception)]
#[base_error_name(Batch)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum BatchError {
    #[error("num_batches {num_batches} doesn't divide length {l}")]
    NumberDoesntDivide { l: usize, num_batches: usize },

    #[error("Would need to batch multiple axes, only supports one")]
    RequiresMultipleAxes {},

    #[error("Batching axis originates too high")]
    AxisOriginatesTooHigh {},
}

#[pyfunction]
#[pyo3(name = "batch_einsum")]
pub fn batch_einsum_py(einsum: Einsum, settings: OptimizationSettings) -> Result<CircuitRc> {
    batch_einsum(
        &einsum,
        &mut OptimizationContext::new_settings_circuit(settings, einsum.crc()),
    )
}

pub fn batch_einsum(einsum: &Einsum, context: &mut OptimizationContext) -> Result<CircuitRc> {
    let max_single_mem = context.cache.max_single_tensor_numel;
    assert!(einsum.info().numel_usize() <= max_single_mem);

    let mut no_memory_limit_context: OptimizationContext = Default::default();
    no_memory_limit_context.cache.max_single_tensor_numel = usize::MAX;
    // use named axes to record the ints used in intermediate einsums
    let einsum_args_named_axes: Vec<(CircuitRc, EinsumAxes)> = einsum
        .args
        .iter()
        .enumerate()
        .map(|(i, (c, ints))| {
            (
                set_named_axes(
                    Symbol::new_with_random_uuid(c.info().shape.clone(), Some(i.to_string())),
                    ints.iter()
                        .enumerate()
                        .map(|(i, int)| (i as u8, int.to_string()))
                        .collect(),
                )
                .rc(),
                ints.clone(),
            )
        })
        .collect();
    let einsum_named_axes = Einsum::try_new(
        einsum_args_named_axes.clone(),
        einsum.out_axes.clone(),
        einsum.name_cloned(),
    )
    .unwrap();
    let nested_big =
        einsum_nest_optimize(&einsum_named_axes, &mut no_memory_limit_context).unwrap();

    nested_big.compiler_print();
    let mut intermediates_above_mem = vec![];
    visit_circuit_unwrap(nested_big.crc(), |c| {
        if c.info().numel_usize() > max_single_mem {
            intermediates_above_mem.push(c);
        }
    });
    assert!(!intermediates_above_mem.is_empty());
    // get the set cover of axes to batch
    let mut covers: Vec<u128> = vec![0; 64];
    for (i, intermediate) in intermediates_above_mem.iter().enumerate() {
        for (_, v) in &intermediate.info().named_axes {
            let int = v.parse::<usize>().unwrap();
            let v = covers[int] | 1 << i;
            covers[int] = v
        }
    }
    let ints_needed = set_cover(&covers);
    if ints_needed.len() != 1 {
        bail!(BatchError::RequiresMultipleAxes {});
    }

    let batch_int = ints_needed[0];
    let batch_str = batch_int.to_string();

    let batch_int_len = einsum.shape_map().unwrap()[&(batch_int as u8)];
    let max_interm_mem = intermediates_above_mem
        .iter()
        .map(|x| x.info().numel_usize())
        .max()
        .unwrap();
    let mut num_batches = ((max_interm_mem as f64) / (max_single_mem as f64)) as usize;
    while batch_int_len % num_batches != 0 {
        num_batches += 1;
    }

    let mut batchheads: Vec<CircuitRc> = vec![];
    visit_circuit_with_parents(nested_big.crc(), |x, parents| {
        if x.info().named_axes.values().any(|n| n == &batch_str)
            && !parents
                .iter()
                .any(|p| p.info().named_axes.values().any(|n| n == &batch_str))
        {
            batchheads.push(x);
        }
    });
    let batchheads_from: Vec<CircuitRc> = batchheads
        .iter()
        .map(|c| {
            batch_to_concat(c.clone(), axis_of_name(c, &batch_str).unwrap(), num_batches).unwrap()
        })
        .collect();
    let out_still_symbols = deep_map_op(nested_big.crc(), |c| {
        if let Some(p) = batchheads
            .iter()
            .position(|bh| c.info().hash == bh.info().hash)
        {
            return Some(batchheads_from[p].clone());
        }
        None
    })
    .unwrap();
    let out = deep_map_op(out_still_symbols, |c| {
        if let Some(sym) = c.as_symbol() && let Some(p) = einsum_args_named_axes
            .iter()
            .position(|(s, _ints)| sym.uuid==s.as_symbol().unwrap().uuid)
        {
            return Some(einsum.args[p].0.clone());
        }
        None
    })
    .unwrap();
    Ok(out)
}
