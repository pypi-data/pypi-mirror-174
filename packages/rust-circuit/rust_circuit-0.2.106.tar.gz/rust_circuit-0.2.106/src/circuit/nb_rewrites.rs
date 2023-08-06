use rustc_hash::{FxHashMap as HashMap, FxHashSet as HashSet};

use super::{algebraic_rewrite::remove_axes, CircuitNode};
use crate::{
    circuit::{Add, Einsum},
    pyo3_prelude::*,
    util::filter_out_idx,
};

#[pyfunction]
pub fn einsum_elim_removable_axes_weak(einsum: &Einsum) -> Option<Einsum> {
    let mut int_to_input: HashMap<u8, HashSet<usize>> = HashMap::default();
    for (i, ints) in einsum.input_axes().enumerate() {
        for j in ints {
            int_to_input
                .entry(*j)
                .or_insert(HashSet::default())
                .insert(i);
        }
    }
    let mut int_to_input_removable: HashMap<u8, HashSet<usize>> = HashMap::default();
    for (i, (node, ints)) in einsum.args.iter().enumerate() {
        if let Some(_sc) = node.as_scalar_constant() {
            for j in ints {
                int_to_input_removable
                    .entry(*j)
                    .or_insert(HashSet::default())
                    .insert(i);
            }
        }
    }
    for (k, v) in int_to_input_removable.clone() {
        if v.len() == int_to_input[&k].len() {
            int_to_input_removable.remove(&k);
        }
    }
    if int_to_input_removable.len() == 0 {
        return None;
    }
    return Some(Einsum::new(
        einsum
            .args
            .iter()
            .enumerate()
            .map(|(i, (node, ints))| {
                let removable_axes: HashSet<usize> = ints
                    .iter()
                    .enumerate()
                    .filter_map(|(j, int)| {
                        if int_to_input_removable
                            .get(int)
                            .map(|z| z.contains(&i))
                            .unwrap_or(false)
                        {
                            Some(j)
                        } else {
                            None
                        }
                    })
                    .collect();
                if removable_axes.len() == 0 {
                    (node.clone(), ints.clone())
                } else {
                    (
                        remove_axes(node, &removable_axes).unwrap(),
                        filter_out_idx(ints, &removable_axes).into_iter().collect(),
                    )
                }
            })
            .collect(),
        einsum.out_axes.clone(),
        einsum.name_cloned(),
    ));
}

#[pyfunction]
pub fn add_elim_removable_axes_weak(add: &Add) -> Option<Add> {
    let axis_map = add.child_axis_map();
    let mut axis_to_inputs: HashMap<usize, HashSet<usize>> = HashMap::default();
    let mut axis_to_inputs_removable: HashMap<usize, HashSet<usize>> = HashMap::default();
    for (i, v) in axis_map.iter().enumerate() {
        for (oj, j) in v
            .iter()
            .enumerate()
            .filter_map(|z| z.1.as_ref().map(|y| (z.0, y)))
        {
            if add.nodes[i].info().shape[oj] != 1 {
                axis_to_inputs
                    .entry(*j)
                    .or_insert(HashSet::default())
                    .insert(i);
                if let Some(_scalar) = add.nodes[i].as_scalar_constant() {
                    axis_to_inputs_removable
                        .entry(*j)
                        .or_insert(HashSet::default())
                        .insert(i);
                }
            }
        }
    }
    for (k, v) in axis_to_inputs_removable.clone() {
        if axis_to_inputs[&k].len() == v.len() {
            axis_to_inputs_removable.remove(&k);
        }
    }
    if axis_to_inputs_removable.len() == 0 {
        return None;
    }
    Some(Add::new(
        add.nodes_and_rank_differences()
            .iter()
            .enumerate()
            .map(|(i, (node, rank_dif))| {
                let removable_axes: HashSet<usize> = (*rank_dif..add.info().rank())
                    .enumerate()
                    .filter_map(|(j, int)| {
                        if axis_to_inputs_removable
                            .get(&int)
                            .map(|z| z.contains(&i))
                            .unwrap_or(false)
                        {
                            Some(j)
                        } else {
                            None
                        }
                    })
                    .collect();
                if removable_axes.len() == 0 {
                    node.clone()
                } else {
                    remove_axes(node, &removable_axes)
                        .unwrap()
                        .unsqueeze(removable_axes.into_iter().collect(), None)
                        .unwrap()
                        .rc()
                }
            })
            .collect(),
        add.name_cloned(),
    ))
}
