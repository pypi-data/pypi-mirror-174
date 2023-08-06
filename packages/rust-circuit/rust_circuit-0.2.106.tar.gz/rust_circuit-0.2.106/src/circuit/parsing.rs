use std::{iter::zip, str::FromStr};

use anyhow::{bail, Context, Result};
use macro_rules_attribute::apply;
use once_cell::sync::Lazy;
use pyo3::exceptions::PyValueError;
use regex::Regex;
use rustc_hash::FxHashMap as HashMap;
use thiserror::Error;
use uuid::Uuid;

use super::{
    Add, ArrayConstant, AutoTag, CircuitNode, CircuitRc, Concat, Cumulant, DiscreteVar, Einsum,
    GeneralFunction, Index, ModuleNode, ModuleNodeSpec, Rearrange, ScalarConstant, Scatter,
    StoredCumulantVar, Symbol,
};
use crate::{
    all_imports::{Shape, Sv, TensorIndex},
    lru_cache::TensorCacheRrfs,
    pyo3_prelude::*,
    python_error_exception,
    tensor_util::TorchDeviceDtypeOp,
};

#[pyfunction(
    string,
    module_spec_map = "HashMap::default()",
    reference_circuits = "HashMap::default()",
    tensors_as_random = "false",
    tensors_as_random_device_dtype = "TorchDeviceDtypeOp{device:None,dtype:None}",
    tensor_getter = "None"
)]
#[pyo3(name = "parse_compiler_repr_bijection")]
pub fn parse_compiler_repr_bijection_py(
    string: &str,
    module_spec_map: HashMap<String, ModuleNodeSpec>,
    reference_circuits: HashMap<String, CircuitRc>,
    tensors_as_random: bool,
    tensors_as_random_device_dtype: TorchDeviceDtypeOp,
    tensor_cache: Option<TensorCacheRrfs>,
) -> Result<CircuitRc> {
    let mut tensor_cache = tensor_cache;
    parse_compiler_repr_bijection(
        string,
        module_spec_map,
        reference_circuits,
        tensors_as_random,
        tensors_as_random_device_dtype,
        &mut tensor_cache,
    )
}

pub fn parse_compiler_repr_bijection(
    string: &str,
    module_spec_map: HashMap<String, ModuleNodeSpec>,
    reference_circuits: HashMap<String, CircuitRc>,
    tensors_as_random: bool,
    tensors_as_random_device_dtype: TorchDeviceDtypeOp,
    tensor_cache: &mut Option<TensorCacheRrfs>,
) -> Result<CircuitRc> {
    let string = string.trim();
    let lines: Vec<_> = string.lines().collect();
    // make seperate struct that can deeply mutate, can't use immutable Circuit bc see children later
    #[derive(Debug, Clone)]
    struct PartialCirc {
        pub variant: String, // copying bc refs annoying / don't care
        pub extra: String,
        pub shape: Option<Shape>,
        pub name: Option<String>,
        pub children: Vec<usize>,
    }
    let tab_width: usize = 2;
    let mut partial_circuits: Vec<Option<PartialCirc>> = vec![None; lines.len()];
    let mut stack: Vec<usize> = vec![];
    static RE: Lazy<Regex> = Lazy::new(|| {
        Regex::new(r"^( *)(\d+)(?: '((?:(?:\\')?[^']*)*)')?(?: \[([\d, ]*)\])?(?: ([a-zA-Z]+))?(?: (.*))?\s*$").unwrap()
    });
    for line in lines {
        let rf = || ParseError::NoRegexMatch {
            line: line.to_owned(),
        };
        let re_captures = RE.captures(line).ok_or_else(rf)?;
        let num_spaces = re_captures.get(1).ok_or_else(rf)?.as_str().len();
        if num_spaces % tab_width != 0 {
            bail!(ParseError::InvalidIndentation {
                tab_width,
                spaces: num_spaces,
                stack_indentation: stack.len(),
                stack_top: stack.last().map(|z| partial_circuits[*z]
                    .clone()
                    .unwrap()
                    .variant
                    .clone()),
            });
        }
        let indentation_level = num_spaces / tab_width;
        if indentation_level > stack.len() {
            bail!(ParseError::InvalidIndentation {
                tab_width,
                spaces: num_spaces,
                stack_indentation: stack.len(),
                stack_top: stack.last().map(|z| partial_circuits[*z]
                    .clone()
                    .unwrap()
                    .variant
                    .clone()),
            });
        }
        stack.truncate(indentation_level);
        let serial_number = re_captures
            .get(2)
            .ok_or_else(rf)?
            .as_str()
            .parse::<usize>()
            .unwrap();

        if serial_number > partial_circuits.len() - 1 {
            partial_circuits.resize(serial_number + 1, None)
        }
        let is_new_node = partial_circuits[serial_number].is_none();
        if is_new_node {
            partial_circuits[serial_number] = Some(PartialCirc {
                name: re_captures
                    .get(3)
                    .map(|x| x.as_str().replace(r"\'", "'").replace(r"\\", r"\")),
                shape: if re_captures.get(4).is_some() {
                    Some(
                        re_captures
                            .get(4)
                            .ok_or_else(rf)?
                            .as_str()
                            .split(',')
                            .map(|z| z.trim())
                            .filter(|z| !z.is_empty())
                            .map(|x| x.parse::<usize>())
                            .collect::<Result<Sv<_>, _>>()
                            .map_err(|e| ParseError::NumberFail {
                                string: format!("{}", e),
                            })?,
                    )
                } else {
                    None
                },
                variant: re_captures.get(5).ok_or_else(rf)?.as_str().to_owned(),
                extra: re_captures
                    .get(6)
                    .map(|z| z.as_str())
                    .unwrap_or("")
                    .trim()
                    .to_owned(),
                children: vec![],
            });
        }
        if let Some(l) = stack.last() {
            partial_circuits[*l]
                .as_mut()
                .unwrap()
                .children
                .push(serial_number);
        }
        if is_new_node {
            stack.push(serial_number);
        }
    }

    fn deep_convert_partial_circ(
        serial_number: usize,
        partial_circuits: &Vec<Option<PartialCirc>>,
        context: &mut HashMap<usize, CircuitRc>,
        module_spec_map: &HashMap<String, ModuleNodeSpec>,
        reference_circuits: &HashMap<String, CircuitRc>,
        tensors_as_random: bool,
        tensors_as_random_device_dtype: TorchDeviceDtypeOp,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<CircuitRc> {
        if let Some(already) = context.get(&serial_number) {
            return Ok(already.clone());
        }
        if serial_number > partial_circuits.len() - 1 {
            bail!(ParseError::InvalidSerialNumber { serial_number });
        }
        let ps = partial_circuits[serial_number]
            .as_ref()
            .ok_or(ParseError::InvalidSerialNumber { serial_number })?;
        let children: Vec<CircuitRc> = ps
            .children
            .iter()
            .map(|x| {
                deep_convert_partial_circ(
                    *x,
                    partial_circuits,
                    context,
                    module_spec_map,
                    reference_circuits,
                    tensors_as_random,
                    tensors_as_random_device_dtype.clone(),
                    tensor_cache,
                )
            })
            .collect::<Result<Vec<_>, _>>()?;
        let variant: &str = &ps.variant;
        let result = match variant {
            "Array" => {
                if tensors_as_random {
                    ArrayConstant::randn_named(
                        ps.shape.clone().ok_or(ParseError::ShapeNeeded {
                            variant: variant.to_owned(),
                        })?,
                        ps.name.clone(),
                        tensors_as_random_device_dtype,
                    )
                    .rc()
                } else {
                    ArrayConstant::from_hash_prefix(ps.name.clone(), &ps.extra, tensor_cache)
                        .context("parse array constant from hash prefix")?
                        .rc()
                }
            }
            "Scalar" => ScalarConstant::nrc(
                ps.extra
                    .parse::<f64>()
                    .map_err(|e| ParseError::NumberFail {
                        string: format!("{}", e),
                    })?,
                ps.shape
                    .as_ref()
                    .ok_or(ParseError::ShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone(),
                ps.name.clone(),
            ),
            "Add" => {
                if !ps.extra.is_empty() {
                    bail!(ParseError::ExtraUnneededString {
                        string: ps.extra.to_owned(),
                    })
                } else {
                    Add::try_new(children, ps.name.clone())?.rc()
                }
            }
            "Concat" => Concat::try_new(
                children,
                ps.extra
                    .parse::<usize>()
                    .map_err(|e| ParseError::NumberFail {
                        string: format!("{}", e),
                    })?,
                ps.name.clone(),
            )?
            .rc(),
            "Einsum" => Einsum::from_einsum_string(&ps.extra, children, ps.name.clone())?.rc(),
            "Rearrange" => {
                Rearrange::from_einops_string(children[0].clone(), &ps.extra, ps.name.clone())?.rc()
            }
            "Symbol" => {
                let shape = ps
                    .shape
                    .as_ref()
                    .ok_or(ParseError::ShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone();
                if ps.extra.is_empty() {
                    Symbol::new_with_none_uuid(shape, ps.name.clone()).rc()
                } else {
                    Symbol::nrc(
                        shape,
                        Uuid::from_str(&ps.extra).map_err(|_e| ParseError::Fail {
                            string: ps.extra.to_owned(),
                        })?,
                        ps.name.clone(),
                    )
                }
            }
            "GeneralFunction" => {
                GeneralFunction::new_by_name(children, ps.extra.clone(), ps.name.clone())?.rc()
            }
            "Index" => Index::try_new(
                children[0].clone(),
                TensorIndex::from_bijection_string(&ps.extra, tensor_cache)?,
                ps.name.clone(),
            )?
            .rc(),
            "Scatter" => Scatter::try_new(
                children[0].clone(),
                TensorIndex::from_bijection_string(&ps.extra, tensor_cache)?,
                ps.shape
                    .as_ref()
                    .ok_or(ParseError::ShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone(),
                ps.name.clone(),
            )?
            .rc(),
            "ModuleNode" => ModuleNode::try_new(
                children,
                module_spec_map
                    .get(&ps.extra.clone())
                    .cloned()
                    .ok_or_else(|| ParseError::ModuleNotFound {
                        name: ps.extra.clone(),
                    })?,
                ps.name.clone(),
            )?
            .rc(),
            "Ref" => reference_circuits
                .get(&ps.extra.clone())
                .cloned()
                .ok_or_else(|| ParseError::CircuitRefNotFound {
                    name: ps.extra.clone(),
                })?,
            "AutoTag" => Uuid::from_str(&ps.extra)
                .map_err(|_| ParseError::InvalidUuid {
                    string: ps.extra.clone(),
                })
                .map(|uuid| AutoTag::nrc(children[0].clone(), uuid, ps.name.clone()))?,
            "Cumulant" => Cumulant::nrc(children, ps.name.clone()),
            "DiscreteVar" => {
                DiscreteVar::try_new(children[0].clone(), children[1].clone(), ps.name.clone())?
                    .rc()
            }
            "StoredCumulantVar" => {
                if let [cum_nums, uuid] = ps.extra.split("|").collect::<Vec<_>>()[..] {
                    let keys = cum_nums
                        .split(",")
                        .map(|s| s.trim().parse::<usize>())
                        .collect::<Result<Vec<_>, _>>()
                        .map_err(|e| ParseError::NumberFail {
                            string: format!("{}", e),
                        })?;

                    let uuid = Uuid::from_str(uuid).map_err(|_| ParseError::InvalidUuid {
                        string: ps.extra.clone(),
                    })?;
                    if keys.len() != children.len() {
                        bail!(ParseError::WrongNumberChildren {
                            expected: keys.len(),
                            found: children.len(),
                        })
                    } else {
                        StoredCumulantVar::try_new(
                            zip(keys, children).collect(),
                            uuid,
                            ps.name.clone(),
                        )?
                        .rc()
                    }
                } else {
                    bail!(ParseError::Fail {
                        string: ps.extra.clone(),
                    })
                }
            }
            _ => bail!(ParseError::InvalidVariant {
                v: variant.to_owned(),
            }),
        };
        context.insert(serial_number, result.clone());
        Ok(result)
    }
    let mut context: HashMap<usize, CircuitRc> = HashMap::default();
    deep_convert_partial_circ(
        stack[0],
        &partial_circuits,
        &mut context,
        &module_spec_map,
        &reference_circuits,
        tensors_as_random,
        tensors_as_random_device_dtype,
        tensor_cache,
    )
}

#[apply(python_error_exception)]
#[base_error_name(Parse)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ParseError {
    #[error("Parsing no regex match '{line}'")]
    NoRegexMatch { line: String },

    #[error("Parsing number failed {string}")]
    NumberFail { string: String },

    #[error("Parsing failed {string}")]
    Fail { string: String },

    #[error("Expected UUID string, found  {string}")]
    InvalidUuid { string: String },

    #[error("Parsing wrong number of children, expected {expected} found {found}")]
    WrongNumberChildren { expected: usize, found: usize },

    #[error("Parsing invalid indentation, tab width {tab_width} num spaces {spaces} stack indentation {stack_indentation} stack top {stack_top:?}")]
    InvalidIndentation {
        spaces: usize,
        tab_width: usize,
        stack_indentation: usize,
        stack_top: Option<String>,
    },

    #[error("Parsing invalid circuit variant {v}")]
    InvalidVariant { v: String },

    #[error("Parsing invalid serial number {serial_number}")]
    InvalidSerialNumber { serial_number: usize },

    #[error("Parsing Extra Unneeded String '{string}'")]
    ExtraUnneededString { string: String },

    #[error("Parsing shape needed but not provided on {variant}")]
    ShapeNeeded { variant: String },

    #[error("Parsing found multiple circuits in sequence, instead of one circuit (aka last node wasn't child of anything)")]
    GotMultipleCircuits {},

    #[error("Circuit by name not found: {name}")]
    CircuitRefNotFound { name: String },

    #[error("Module by name not found: {name}")]
    ModuleNotFound { name: String },
}
