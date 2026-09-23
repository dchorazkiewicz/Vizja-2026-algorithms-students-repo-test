"""AST helpers for List 03."""

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


def recursive_function_names(node: ast.AST) -> set[str]:
    result = set()
    functions = [node] + [
        item for item in ast.walk(node)
        if isinstance(item, ast.FunctionDef) and item is not node
    ]
    for function in functions:
        calls = called_names(function)
        if function.name in calls:
            result.add(function.name)
    return result


def loop_count(node: ast.AST) -> int:
    return sum(isinstance(item, (ast.For, ast.While)) for item in ast.walk(node))


def function_metrics(node: ast.FunctionDef):
    calls = sorted(called_names(node))
    return {
        "loops": loop_count(node),
        "ifs": sum(isinstance(item, ast.If) for item in ast.walk(node)),
        "returns": sum(isinstance(item, ast.Return) for item in ast.walk(node)),
        "assignments": sum(
            isinstance(item, (ast.Assign, ast.AnnAssign, ast.AugAssign))
            for item in ast.walk(node)
        ),
        "calls": calls,
        "recursive_functions": sorted(recursive_function_names(node)),
        "list_literals": sum(isinstance(item, ast.List) for item in ast.walk(node)),
        "list_comprehensions": sum(isinstance(item, ast.ListComp) for item in ast.walk(node)),
    }
