#![feature(core_intrinsics)]
// Personally, I like or_fun_call as a lint. But currently code fails...
#![allow(clippy::too_many_arguments, clippy::or_fun_call)]
#![feature(map_try_insert)]
use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;

use pyo3::{types::PyModule, wrap_pyfunction, PyResult, Python};
/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[macro_use]
pub mod error;
#[pyo3::pymodule]
fn rust_circuit(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    pyo3::anyhow::set_get_exception(std::sync::Arc::new(error::get_exception));

    use circuit_base::{
        circuit_utils::{
            cast_circuit, count_nodes, toposort_circuit, total_arrayconstant_size, total_flops,
        },
        flat_concat,
        named_axes::{propagate_named_axes, set_named_axes_py},
    };
    use circuit_rewrites::{
        algebraic_rewrite::{
            add_collapse_scalar_inputs, add_deduplicate, add_elim_zeros, add_flatten_once,
            add_fuse_scalar_multiples, add_make_broadcasts_explicit, add_pull_removable_axes,
            concat_elim_identity, concat_merge_uniform, concat_pull_removable_axes,
            concat_repeat_to_rearrange, distribute, distribute_all, einsum_concat_to_add,
            einsum_elim_identity, einsum_elim_zero, einsum_flatten_once, einsum_merge_scalars,
            einsum_nest_path, einsum_of_permute_merge, einsum_pull_removable_axes, extract_add,
            generalfunction_pull_removable_axes, index_elim_identity, index_fuse,
            index_merge_scalar, index_split_axes, permute_of_einsum_merge, push_down_index,
            rearrange_elim_identity, rearrange_fuse, rearrange_merge_scalar, remove_add_few_input,
        },
        canonicalize::{canonicalize_node_py, deep_canonicalize_py},
        circuit_manipulation::{
            filter_nodes_py, path_get, replace_nodes_py, update_nodes_py, update_path_py,
        },
        circuit_optimizer::{optimize_and_evaluate, optimize_and_evaluate_many},
        compiler_heuristics::deep_maybe_distribute_py,
        concat_rewrite::{
            add_pull_concat, concat_drop_size_zero, concat_fuse, einsum_pull_concat,
            generalfunction_pull_concat, index_concat_drop_unreached, split_to_concat,
        },
        deep_rewrite::{
            compiler_simp_py, compiler_simp_step_py, compiler_simp_until_same,
            deep_heuristic_nest_adds, deep_pull_concat, deep_pull_concat_messy,
            deep_push_down_index,
        },
        diag_rewrite::{add_pull_diags, einsum_push_down_trace},
        scatter_rewrite::{
            add_pull_scatter, einsum_pull_scatter, index_einsum_to_scatter, scatter_elim_identity,
            scatter_pull_removable_axes, scatter_to_concat,
        },
        scheduled_execution::scheduled_evaluate,
    };
    use pyo3::{exceptions::PyValueError, types::PyTuple, PyTypeInfo};
    use rr_util::opt_einsum::optimize_einsum_spec_cached;

    // we assume throughout the codebase that usize is 8 bytes, and otherwise error here
    if !core::mem::size_of::<usize>() == 8 {
        return PyResult::Err(PyValueError::new_err("Only supports x64"));
    }

    m.add_class::<circuit_base::PyCircuitBase>()?;

    m.add_class::<rr_util::rearrange_spec::RearrangeSpec>()?;
    m.add_class::<circuit_base::GeneralFunctionSpec>()?;
    m.add_class::<rr_util::opt_einsum::EinsumSpec>()?;
    m.add_class::<circuit_base::Einsum>()?;
    m.add_class::<circuit_base::ArrayConstant>()?;
    m.add_class::<circuit_base::Symbol>()?;
    m.add_class::<circuit_base::ScalarConstant>()?;
    m.add_class::<circuit_base::Add>()?;
    m.add_class::<circuit_base::Rearrange>()?;
    m.add_class::<circuit_base::Index>()?;
    m.add_class::<circuit_base::GeneralFunction>()?;
    m.add_class::<circuit_base::Concat>()?;
    m.add_class::<circuit_base::Scatter>()?;
    m.add_class::<circuit_base::Conv>()?;
    m.add_class::<circuit_rewrites::circuit_optimizer::OptimizationSettings>()?;
    m.add_class::<circuit_rewrites::circuit_optimizer::OptimizationContext>()?;

    m.add_class::<rr_util::tensor_util::TorchDeviceDtype>()?;
    m.add_class::<rr_util::tensor_util::TorchDeviceDtypeOp>()?;

    m.add_class::<circuit_base::PyGFSpecShapeGetter>()?;

    m.add_class::<circuit_rewrites::scheduled_execution::Schedule>()?;
    m.add_class::<circuit_rewrites::scheduled_execution::ScheduleStats>()?;
    m.add_class::<circuit_rewrites::schedule_send::ScheduleToSend>()?;

    m.add_class::<circuit_base::module_nodes::ModuleNode>()?;
    m.add_class::<circuit_base::module_nodes::ModuleNodeSpec>()?;
    m.add_class::<circuit_base::module_nodes::ModuleNodeArgSpec>()?;
    m.add_class::<circuit_base::module_nodes::ModuleNodeArgSpec>()?;
    m.add_class::<circuit_base::AutoTag>()?;
    m.add_class::<circuit_base::DiscreteVar>()?;
    m.add_class::<circuit_base::StoredCumulantVar>()?;
    m.add_class::<circuit_base::Cumulant>()?;
    m.add_class::<get_update_node::Matcher>()?;
    m.add_class::<get_update_node::matcher::RegexWrap>()?;
    m.add_class::<get_update_node::IterativeMatcher>()?;
    m.add_class::<get_update_node::IterateMatchResults>()?;
    m.add_class::<get_update_node::Transform>()?;
    m.add_class::<get_update_node::Updater>()?;
    m.add_class::<get_update_node::BoundUpdater>()?;
    m.add_class::<get_update_node::Getter>()?;
    m.add_class::<get_update_node::BoundGetter>()?;
    m.add_class::<get_update_node::Batcher>()?;

    m.add_class::<rr_util::lru_cache::TensorCacheRrfs>()?;

    m.add_function(wrap_pyfunction!(circuit_base::circuit_is_leaf_py, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_base::circuit_is_irreducible_node_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_base::circuit_is_leaf_constant_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(circuit_base::circuit_is_var_py, m)?)?;

    m.add_function(wrap_pyfunction!(add_collapse_scalar_inputs, m)?)?;
    m.add_function(wrap_pyfunction!(add_deduplicate, m)?)?;
    m.add_function(wrap_pyfunction!(remove_add_few_input, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_flatten_once, m)?)?;
    m.add_function(wrap_pyfunction!(add_flatten_once, m)?)?;

    m.add_function(wrap_pyfunction!(einsum_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(index_merge_scalar, m)?)?;
    m.add_function(wrap_pyfunction!(index_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(index_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_merge_scalar, m)?)?;
    m.add_function(wrap_pyfunction!(rearrange_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(concat_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(concat_merge_uniform, m)?)?;
    m.add_function(wrap_pyfunction!(generalfunction_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::generalfunction_rewrite::generalfunction_merge_inverses,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::generalfunction_rewrite::generalfunction_special_case_simplification,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::generalfunction_rewrite::generalfunction_evaluate_simple,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(concat_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_pull_removable_axes, m)?)?;
    m.add_function(wrap_pyfunction!(add_make_broadcasts_explicit, m)?)?;
    m.add_function(wrap_pyfunction!(distribute, m)?)?;
    m.add_function(wrap_pyfunction!(distribute_all, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_of_permute_merge, m)?)?;
    m.add_function(wrap_pyfunction!(permute_of_einsum_merge, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_elim_zero, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_merge_scalars, m)?)?;
    m.add_function(wrap_pyfunction!(push_down_index, m)?)?;
    m.add_function(wrap_pyfunction!(index_split_axes, m)?)?;
    m.add_function(wrap_pyfunction!(add_elim_zeros, m)?)?;

    m.add_function(wrap_pyfunction!(compiler_simp_py, m)?)?;
    m.add_function(wrap_pyfunction!(compiler_simp_step_py, m)?)?;
    m.add_function(wrap_pyfunction!(compiler_simp_until_same, m)?)?;
    m.add_function(wrap_pyfunction!(deep_canonicalize_py, m)?)?;
    m.add_function(wrap_pyfunction!(canonicalize_node_py, m)?)?;

    m.add_function(wrap_pyfunction!(
        circuit_rewrites::batching::batch_to_concat,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::batching::batch_einsum_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::compiler_strip::strip_names_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(deep_maybe_distribute_py, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::compiler_heuristics::maybe_distribute_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(einsum_nest_path, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::algebraic_rewrite::einsum_nest_optimize_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::deep_rewrite::deep_optimize_einsums_py,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(index_einsum_to_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(scatter_elim_identity, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_pull_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_scatter, m)?)?;
    m.add_function(wrap_pyfunction!(scatter_pull_removable_axes, m)?)?;

    m.add_function(wrap_pyfunction!(cast_circuit, m)?)?;
    m.add_function(wrap_pyfunction!(count_nodes, m)?)?;
    m.add_function(wrap_pyfunction!(total_flops, m)?)?;
    m.add_function(wrap_pyfunction!(total_arrayconstant_size, m)?)?;

    m.add_function(wrap_pyfunction!(
        circuit_rewrites::circuit_optimizer::optimize_circuit_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(optimize_einsum_spec_cached, m)?)?;
    m.add_function(wrap_pyfunction!(scatter_to_concat, m)?)?;
    m.add_function(wrap_pyfunction!(scheduled_evaluate, m)?)?;
    m.add_function(wrap_pyfunction!(optimize_and_evaluate, m)?)?;
    m.add_function(wrap_pyfunction!(optimize_and_evaluate_many, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::circuit_optimizer::optimize_to_schedule,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::circuit_optimizer::optimize_to_schedule_many,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(flat_concat, m)?)?;
    m.add_function(wrap_pyfunction!(circuit_base::flat_concat_back, m)?)?;
    m.add_function(wrap_pyfunction!(deep_heuristic_nest_adds, m)?)?;
    m.add_function(wrap_pyfunction!(concat_fuse, m)?)?;
    m.add_function(wrap_pyfunction!(generalfunction_pull_concat, m)?)?;
    m.add_function(wrap_pyfunction!(index_concat_drop_unreached, m)?)?;
    m.add_function(wrap_pyfunction!(concat_drop_size_zero, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_pull_concat, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_concat, m)?)?;
    m.add_function(wrap_pyfunction!(split_to_concat, m)?)?;
    m.add_function(wrap_pyfunction!(deep_push_down_index, m)?)?;
    m.add_function(wrap_pyfunction!(deep_pull_concat_messy, m)?)?;
    m.add_function(wrap_pyfunction!(deep_pull_concat, m)?)?;
    m.add_function(wrap_pyfunction!(set_named_axes_py, m)?)?;
    m.add_function(wrap_pyfunction!(propagate_named_axes, m)?)?;
    m.add_function(wrap_pyfunction!(toposort_circuit, m)?)?;
    m.add_function(wrap_pyfunction!(add_pull_diags, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_push_down_trace, m)?)?;
    m.add_function(wrap_pyfunction!(einsum_concat_to_add, m)?)?;
    m.add_function(wrap_pyfunction!(concat_repeat_to_rearrange, m)?)?;
    m.add_function(wrap_pyfunction!(extract_add, m)?)?;
    m.add_function(wrap_pyfunction!(add_fuse_scalar_multiples, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::scatter_rewrite::concat_to_scatter,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::debugging::opt_eval_each_subcircuit_until_fail,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::algebraic_rewrite::add_outer_product_broadcasts_on_top,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_base::circuit_utils::replace_all_randn_seeded,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(
        circuit_rewrites::deep_rewrite::basic_simp,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(circuit_base::deep_map_preorder_py, m)?)?;
    m.add_function(wrap_pyfunction!(circuit_base::deep_map_py, m)?)?;

    m.add_function(wrap_pyfunction!(circuit_base::visit_circuit_py, m)?)?;

    m.add_function(wrap_pyfunction!(filter_nodes_py, m)?)?;
    m.add_function(wrap_pyfunction!(replace_nodes_py, m)?)?;
    m.add_function(wrap_pyfunction!(update_nodes_py, m)?)?;
    m.add_function(wrap_pyfunction!(path_get, m)?)?;
    m.add_function(wrap_pyfunction!(update_path_py, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_base::expand_node::expand_node_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(rr_util::rrfs::save_tensor_rrfs, m)?)?;
    m.add_function(wrap_pyfunction!(rr_util::rrfs::tensor_from_hash, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::algebraic_rewrite::einsum_permute_to_rearrange,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::nb_rewrites::add_elim_removable_axes_weak,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_rewrites::nb_rewrites::einsum_elim_removable_axes_weak,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(rr_util::rrfs::tensor_from_hash, m)?)?;
    m.add_function(wrap_pyfunction!(
        circuit_base::module_nodes::inline_all_modules,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_base::expand_node::replace_expand_bottom_up_dict_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_base::expand_node::replace_expand_bottom_up_py,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        get_update_node::sample_transform::default_var_matcher,
        m
    )?)?;
    m.add_class::<get_update_node::sample_transform::RandomSampleSpec>()?;
    m.add_class::<get_update_node::sample_transform::RunDiscreteVarAllSpec>()?;
    m.add_class::<get_update_node::sample_transform::SampleTransform>()?;
    m.add_function(wrap_pyfunction!(
        get_update_node::sample_transform::factored_cumulant_expectation_rewrite,
        m
    )?)?;

    // add more py function as desired or whatever...

    m.add_function(wrap_pyfunction!(
        circuit_rewrites::server::circuit_server_serve,
        m
    )?)?;
    m.add_function(wrap_pyfunction!(
        circuit_base::parsing::parse_compiler_repr_bijection_py,
        m
    )?)?;

    m.add_function(wrap_pyfunction!(circuit_base::print_circuit_type_check, m)?)?;
    m.add_function(wrap_pyfunction!(rr_util::py_types::hash_tensor, m)?)?;

    // create dummy object for all the type aliases we use in the stub file
    // TODO: maybe these should somehow be the actual types we use in the stub file
    // (this is kinda annoying)
    m.add("Shape", PyTuple::type_object(py))?;
    m.add("Axis", py.None())?;
    m.add("IrreducibleNode", py.None())?;
    m.add("Leaf", py.None())?;
    m.add("LeafConstant", py.None())?;
    m.add("Var", py.None())?;
    m.add("MatcherIn", py.None())?;
    m.add("IterativeMatcherIn", py.None())?;
    m.add("TransformIn", py.None())?;
    m.add("SampleSpecIn", py.None())?;
    m.add("TorchAxisIndex", py.None())?;

    error::register_exceptions(py, m)?;

    Ok(())
}
