// temporary schedule sending setup
use anyhow::Result;
use miniserde::{json, Deserialize, Serialize};
use pyo3::types::PyByteArray;
use rustc_hash::FxHashMap as HashMap;

use super::{
    parse_compiler_repr_bijection,
    print::repr_circuit_line_compiler,
    scheduled_execution::{get_children_keys, Instruction, Schedule},
    IrreducibleNode, ScalarConstant,
};
use crate::{
    all_imports::{Shape, TorchDeviceDtype},
    circuit::CircuitNode,
    lru_cache::TensorCacheRrfs,
    py_types::{un_flat_concat, Tensor, PY_UTILS},
    pycall,
    pyo3_prelude::*,
    sv,
};

#[pyclass]
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct InstructionToSend {
    variant: String,
    key: usize,
    info: String,
    children: Vec<usize>,
}
#[pyclass]
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ScheduleToSend {
    pub instructions: Vec<InstructionToSend>,
    pub constants: ::std::collections::HashMap<usize, String>,
    pub scalar_constants: ::std::collections::HashMap<usize, String>,
    pub dtype: String,
    pub output_circuit: (usize, Vec<usize>),
    pub split_shapes: Option<Vec<Vec<usize>>>,
}

#[pymethods]
impl ScheduleToSend {
    pub fn evaluate_remote(&self, remote_url: String, device: String) -> Option<Tensor> {
        let self_string = json::to_string(&self);
        let response = ureq::post(&remote_url).send_string(&self_string).unwrap();
        let mut body: Vec<u8> = vec![];
        dbg!(&response);
        response.into_reader().read_to_end(&mut body).unwrap();
        let body_pybytes: PyObject =
            Python::with_gil(|py| PyByteArray::new(py, &body).clone().into());
        let out_shape = self.output_circuit.1.clone();
        let count: usize = out_shape.iter().product();
        pycall!(
            PY_UTILS.tensor_from_bytes,
            (
                TorchDeviceDtype {
                    dtype: self.dtype.clone(),
                    device
                },
                out_shape,
                body_pybytes,
                count,
            )
        )
    }
    pub fn evaluate_remote_many(&self, remote_url: String, device: String) -> Option<Vec<Tensor>> {
        self.evaluate_remote(remote_url, device).map(|tensor| {
            un_flat_concat(
                &tensor,
                self.split_shapes
                    .clone()
                    .unwrap()
                    .iter()
                    .map(|y| y.iter().cloned().collect())
                    .collect(),
            )
            .unwrap()
        })
    }
}

impl ScheduleToSend {
    pub fn load(self, device: String, cache: &mut Option<TensorCacheRrfs>) -> Result<Schedule> {
        let mut result = Schedule {
            instructions: vec![],
            constants: Default::default(),
            scalar_constants: Default::default(),
            device_dtype: TorchDeviceDtype {
                device,
                dtype: self.dtype,
            },
            output_circuit: Some((self.output_circuit.0, ScalarConstant::nrc(0.0, sv![], None))),
            split_shapes: self
                .split_shapes
                .map(|z| z.iter().map(|z| z.iter().cloned().collect()).collect()),
        };

        let mut shapes: HashMap<usize, Shape> = <HashMap<usize, Shape> as Default>::default();
        result.constants = self
            .constants
            .iter()
            .map(|(k, v)| {
                let parsed = parse_compiler_repr_bijection(
                    &("0".to_owned() + v),
                    Default::default(),
                    Default::default(),
                    false,
                    result.device_dtype.clone().into(),
                    cache,
                )?;
                shapes.insert(*k, parsed.info().shape.clone());
                let irreducible: Option<IrreducibleNode> = (**parsed).clone().into();
                Ok((*k, irreducible.unwrap()))
            })
            .collect::<Result<_>>()?;
        result.scalar_constants = self
            .scalar_constants
            .iter()
            .map(|(k, v)| {
                Ok((*k, {
                    let resulty = parse_compiler_repr_bijection(
                        &("0".to_owned() + v),
                        Default::default(),
                        Default::default(),
                        false,
                        result.device_dtype.clone().into(),
                        cache,
                    )?
                    .as_scalar_constant()
                    .unwrap()
                    .clone();
                    shapes.insert(*k, resulty.info().shape.clone());
                    resulty
                }))
            })
            .collect::<Result<_>>()?;
        result.instructions = self
            .instructions
            .iter()
            .map(|ins| {
                let v: &str = &ins.variant;
                match v {
                    "Drop" => Ok(Instruction::Drop(ins.key)),
                    "Compute" => Ok(Instruction::Compute(ins.key, {
                        let result = parse_compiler_repr_bijection(
                            &std::iter::once("0".to_owned() + &ins.info)
                                .chain(ins.children.iter().map(|i| {
                                    format!("  {} '{}' {:?} Symbol", *i + 1, i, shapes[i])
                                }))
                                .collect::<Vec<String>>()
                                .join("\n"),
                            Default::default(),
                            Default::default(),
                            false,
                            Default::default(),
                            cache,
                        )?;
                        shapes.insert(ins.key, result.info().shape.clone());
                        result
                    })),
                    _ => {
                        panic!()
                    }
                }
            })
            .collect::<Result<Vec<Instruction>>>()?;
        Ok(result)
    }
}

impl Into<ScheduleToSend> for &Schedule {
    fn into(self) -> ScheduleToSend {
        ScheduleToSend {
            instructions: self
                .instructions
                .iter()
                .map(|i| match i {
                    Instruction::Compute(key, circ) => InstructionToSend {
                        key: *key,
                        variant: "Compute".to_owned(),

                        info: repr_circuit_line_compiler(&**circ, true, false),
                        children: get_children_keys(circ.clone()),
                    },
                    Instruction::Drop(key) => InstructionToSend {
                        key: *key,
                        variant: "Drop".to_owned(),
                        info: "".to_owned(),
                        children: vec![],
                    },
                })
                .collect(),
            constants: self
                .constants
                .iter()
                .map(|(k, v)| {
                    (
                        *k,
                        repr_circuit_line_compiler(&v.clone().into(), true, false),
                    )
                })
                .collect(),
            scalar_constants: self
                .scalar_constants
                .iter()
                .map(|(k, v)| {
                    (
                        *k,
                        repr_circuit_line_compiler(&v.clone().into(), true, false),
                    )
                })
                .collect(),
            dtype: self.device_dtype.dtype.clone(),
            output_circuit: (
                self.output_circuit.clone().unwrap().0,
                self.output_circuit
                    .clone()
                    .unwrap()
                    .1
                    .info()
                    .shape
                    .iter()
                    .cloned()
                    .collect(),
            ),
            split_shapes: self
                .split_shapes
                .clone()
                .map(|z| z.iter().map(|y| y.iter().cloned().collect()).collect()),
        }
    }
}
