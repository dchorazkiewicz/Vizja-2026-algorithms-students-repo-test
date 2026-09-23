"""Small AST helpers for methodological tests.

AST = Abstract Syntax Tree. We parse the student's source code and inspect the
structure Python itself sees, rather than searching source text with regexes.
"""

from __future__ import annotations

import ast
from pathlib import Path


def parse_file(path: str | Path) -> ast.Module:
    return ast.parse(Path(path).read_text(encoding="utf-8"))


def function_node(tree: ast.Module, function_name: str) -> ast.FunctionDef:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return node
    raise AssertionError(f"Function {function_name!r} not found")


def has_node(function: ast.FunctionDef, *node_types: type[ast.AST]) -> bool:
    return any(isinstance(node, node_types) for node in ast.walk(function))


def called_names(function: ast.FunctionDef) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            names.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            names.add(node.func.attr)
    return names


def has_slice(function: ast.FunctionDef) -> bool:
    for node in ast.walk(function):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice):
            return True
    return False


def loop_count(function: ast.FunctionDef) -> int:
    return sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(function))


def has_imports(tree: ast.Module) -> bool:
    return any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))


def has_list_comprehension(function: ast.FunctionDef) -> bool:
    return has_node(function, ast.ListComp)


def recursive_calls(function: ast.FunctionDef) -> int:
    count = 0
    for node in ast.walk(function):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == function.name:
                count += 1
    return count
