import ast

from playground.list_01_foundations.grader.ast_checks import (
    called_names,
    function_node,
    has_imports,
    has_node,
    has_slice,
    loop_count,
    parse_file,
)


def test_no_import_shortcuts(source_path):
    tree = parse_file(source_path)
    assert not has_imports(tree)


def test_clamp_structure(source_path):
    tree = parse_file(source_path)
    fn = function_node(tree, "clamp")
    assert has_node(fn, ast.If)
    assert called_names(fn).isdisjoint({"min", "max", "sorted"})


def test_first_index_structure(source_path):
    tree = parse_file(source_path)
    fn = function_node(tree, "first_index")
    assert has_node(fn, ast.For, ast.While)
    assert called_names(fn).isdisjoint({"index", "next"})


def test_min_max_structure(source_path):
    tree = parse_file(source_path)
    fn = function_node(tree, "min_max")
    assert has_node(fn, ast.For, ast.While)
    assert called_names(fn).isdisjoint({"min", "max", "sorted", "sort"})
    assert not has_slice(fn)


def test_reverse_structure(source_path):
    tree = parse_file(source_path)
    fn = function_node(tree, "reverse_in_place")
    assert has_node(fn, ast.For, ast.While)
    assert "reversed" not in called_names(fn)
    assert not has_slice(fn)


def test_running_sum_structure(source_path):
    tree = parse_file(source_path)
    fn = function_node(tree, "first_negative_running_sum")
    assert has_node(fn, ast.For, ast.While)
    assert "sum" not in called_names(fn)
    assert not has_slice(fn)


def test_analyse_scores_structure(source_path):
    tree = parse_file(source_path)
    fn = function_node(tree, "analyse_scores")
    assert called_names(fn).isdisjoint({"sum", "min", "max", "sorted", "sort"})
    assert loop_count(fn) == 1
