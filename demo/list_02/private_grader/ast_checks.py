"""AST helpers for List 02 methodological analysis."""

from __future__ import annotations

import ast
from pathlib import Path


def parse_file(path: str | Path) -> ast.Module:
    return ast.parse(Path(path).read_text(encoding="utf-8"))


def function_node(tree: ast.Module, name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"Function {name!r} not found")


def called_names(node: ast.AST) -> set[str]:
    names = set()
    for item in ast.walk(node):
        if isinstance(item, ast.Call):
            if isinstance(item.func, ast.Name):
                names.add(item.func.id)
            elif isinstance(item.func, ast.Attribute):
                names.add(item.func.attr)
    return names


def has_slice(node: ast.AST) -> bool:
    return any(
        isinstance(item, ast.Subscript) and isinstance(item.slice, ast.Slice)
        for item in ast.walk(node)
    )


def loop_count(node: ast.AST) -> int:
    return sum(isinstance(item, (ast.For, ast.While)) for item in ast.walk(node))


def max_loop_depth(node: ast.AST) -> int:
    def visit(current: ast.AST, depth: int) -> int:
        new_depth = depth + 1 if isinstance(current, (ast.For, ast.While)) else depth
        best = new_depth
        for child in ast.iter_child_nodes(current):
            best = max(best, visit(child, new_depth))
        return best

    return visit(node, 0)


def uses_membership(node: ast.AST) -> bool:
    for item in ast.walk(node):
        if isinstance(item, ast.Compare):
            if any(isinstance(op, (ast.In, ast.NotIn)) for op in item.ops):
                return True
    return False


def recursive_function_names(node: ast.AST) -> set[str]:
    recursive = set()
    for function in ast.walk(node):
        if not isinstance(function, ast.FunctionDef):
            continue
        calls = called_names(function)
        if function.name in calls:
            recursive.add(function.name)
    return recursive


def function_metrics(node: ast.FunctionDef) -> dict[str, object]:
    calls = sorted(called_names(node))
    return {
        "loops": loop_count(node),
        "max_loop_depth": max_loop_depth(node),
        "ifs": sum(isinstance(item, ast.If) for item in ast.walk(node)),
        "returns": sum(isinstance(item, ast.Return) for item in ast.walk(node)),
        "calls": calls,
        "slice": has_slice(node),
        "membership": uses_membership(node),
        "recursive_functions": sorted(recursive_function_names(node)),
        "list_comprehension": any(isinstance(item, ast.ListComp) for item in ast.walk(node)),
        "imports": sorted(
            alias.name
            for item in ast.walk(node)
            if isinstance(item, ast.Import)
            for alias in item.names
        ),
    }
