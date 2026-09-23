"""Evaluate a List 01 implementation from several independent perspectives."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import math
import sys
import tracemalloc
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from demo.list_01.private_grader.instrumentation import InstrumentedSequence, unwrap


FUNCTIONS = (
    "clamp",
    "first_index",
    "min_max",
    "reverse_in_place",
    "first_negative_running_sum",
    "analyse_scores",
)


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("student_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load solution from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_functions(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    return tree, functions


def called_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
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
    def walk(current: ast.AST, depth: int) -> int:
        next_depth = depth + 1 if isinstance(current, (ast.For, ast.While)) else depth
        best = next_depth
        for child in ast.iter_child_nodes(current):
            best = max(best, walk(child, next_depth))
        return best
    return walk(node, 0)


def static_observations(functions):
    observations = {}
    for name in FUNCTIONS:
        node = functions.get(name)
        if node is None:
            observations[name] = {"missing": True}
            continue
        calls = sorted(called_names(node))
        observations[name] = {
            "missing": False,
            "loops": loop_count(node),
            "max_loop_depth": max_loop_depth(node),
            "ifs": sum(isinstance(item, ast.If) for item in ast.walk(node)),
            "returns": sum(isinstance(item, ast.Return) for item in ast.walk(node)),
            "assignments": sum(
                isinstance(item, (ast.Assign, ast.AnnAssign, ast.AugAssign))
                for item in ast.walk(node)
            ),
            "calls": calls,
            "slice": has_slice(node),
            "list_comprehension": any(isinstance(item, ast.ListComp) for item in ast.walk(node)),
            "recursion": name in calls,
            "print": "print" in calls,
            "global": any(isinstance(item, ast.Global) for item in ast.walk(node)),
        }
    return observations


def functional_checks(module):
    results = {}

    def run(name, checks):
        passed = 0
        details = []
        for label, callback in checks:
            try:
                ok = bool(callback())
                passed += int(ok)
                details.append({"case": label, "pass": ok, "error": None})
            except Exception as exc:
                details.append({
                    "case": label,
                    "pass": False,
                    "error": f"{type(exc).__name__}: {exc}",
                })
        results[name] = {
            "passed": passed,
            "total": len(checks),
            "cases": details,
        }

    run("clamp", [
        ("inside", lambda: module.clamp(5, 0, 10) == 5),
        ("below", lambda: module.clamp(-4, 0, 10) == 0),
        ("above", lambda: module.clamp(14, 0, 10) == 10),
        ("negative interval", lambda: module.clamp(-5, -10, -1) == -5),
    ])

    run("first_index", [
        ("empty", lambda: module.first_index([], 3) == -1),
        ("first", lambda: module.first_index([3, 8, 3], 3) == 0),
        ("duplicate-first", lambda: module.first_index([8, 3, 5, 3], 3) == 1),
        ("absent", lambda: module.first_index([1, 2, 3], 9) == -1),
    ])

    def minmax_empty():
        try:
            module.min_max([])
        except ValueError:
            return True
        return False

    run("min_max", [
        ("single", lambda: unwrap(module.min_max([7])) == (7, 7)),
        ("mixed", lambda: unwrap(module.min_max([3, 1, 7, 2])) == (1, 7)),
        ("all-negative", lambda: unwrap(module.min_max([-5, -10, -2])) == (-10, -2)),
        ("empty-rejected", minmax_empty),
    ])

    def reverse_case(values):
        original = values
        expected = list(reversed(values))
        result = module.reverse_in_place(values)
        return result is None and values is original and values == expected

    run("reverse_in_place", [
        ("empty", lambda: reverse_case([])),
        ("odd", lambda: reverse_case([1, 2, 3, 4, 5])),
        ("even", lambda: reverse_case([1, 2, 3, 4])),
    ])

    run("first_negative_running_sum", [
        ("empty", lambda: module.first_negative_running_sum([]) == -1),
        ("immediate", lambda: module.first_negative_running_sum([-1, 10, 10]) == 0),
        ("later", lambda: module.first_negative_running_sum([4, -1, -2, -5, 8]) == 3),
        ("never", lambda: module.first_negative_running_sum([1, 2, 3]) == -1),
    ])

    def scores_invalid_empty():
        try:
            module.analyse_scores([], 50)
        except ValueError:
            return True
        return False

    def scores_invalid_value():
        try:
            module.analyse_scores([10, 101], 50)
        except ValueError:
            return True
        return False

    run("analyse_scores", [
        ("aggregate", lambda: module.analyse_scores([50, 80, 20, 100], 50) == (62.5, 20, 100, 3)),
        ("single", lambda: module.analyse_scores([40], 50) == (40.0, 40, 40, 0)),
        ("empty-rejected", scores_invalid_empty),
        ("invalid-score-rejected", scores_invalid_value),
    ])

    return results


def methodological_findings(static):
    rules = {
        "clamp": {
            "require_loop": False,
            "require_if": True,
            "banned_calls": {"min", "max", "sorted"},
            "ban_slice": False,
            "max_loops": 0,
        },
        "first_index": {
            "require_loop": True,
            "require_if": True,
            "banned_calls": {"index", "next"},
            "ban_slice": True,
            "max_loops": 1,
        },
        "min_max": {
            "require_loop": True,
            "require_if": True,
            "banned_calls": {"min", "max", "sorted", "sort"},
            "ban_slice": True,
            "max_loops": 1,
        },
        "reverse_in_place": {
            "require_loop": True,
            "require_if": False,
            "banned_calls": {"reversed", "list", "copy"},
            "ban_slice": True,
            "max_loops": 1,
        },
        "first_negative_running_sum": {
            "require_loop": True,
            "require_if": True,
            "banned_calls": {"sum"},
            "ban_slice": True,
            "max_loops": 1,
        },
        "analyse_scores": {
            "require_loop": True,
            "require_if": True,
            "banned_calls": {"sum", "min", "max", "sorted", "sort"},
            "ban_slice": True,
            "max_loops": 1,
        },
    }

    findings = {}
    for name, rule in rules.items():
        item = static.get(name, {"missing": True})
        issues = []
        if item.get("missing"):
            issues.append("function missing")
        else:
            if rule["require_loop"] and item["loops"] == 0:
                issues.append("no explicit loop")
            if rule["require_if"] and item["ifs"] == 0:
                issues.append("no explicit selection")
            banned = sorted(set(item["calls"]) & rule["banned_calls"])
            if banned:
                issues.append("banned shortcut calls: " + ", ".join(banned))
            if rule["ban_slice"] and item["slice"]:
                issues.append("slicing detected")
            if item["loops"] > rule["max_loops"]:
                issues.append(f"too many loops for this exercise: {item['loops']}")
            if item["max_loop_depth"] > 1:
                issues.append(f"nested loop depth {item['max_loop_depth']}")
            if item["print"]:
                issues.append("print detected")
            if item["global"]:
                issues.append("global state detected")
        findings[name] = issues
    return findings


def runtime_observations(module):
    out = {}

    def safe(name, callback):
        try:
            out[name] = {"ok": True, **callback()}
        except Exception as exc:
            out[name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    def first_index_probe():
        values = InstrumentedSequence([8, 3, 5, 3, 9, 10])
        result = module.first_index(values, 3)
        return {
            "result": unwrap(result),
            "reads": values.count("read"),
            "writes": values.count("write"),
            "iterations": values.count("iteration_start"),
            "visited_indices": values.visited_indices(),
            "early_exit": values.count("read") <= 2,
        }
    safe("first_index", first_index_probe)

    def minmax_probe():
        values = InstrumentedSequence(range(100), track_numbers=True)
        result = module.min_max(values)
        return {
            "result": unwrap(result),
            "reads": values.count("read"),
            "writes": values.count("write"),
            "iterations": values.count("iteration_start"),
            "slices": values.count("slice_read"),
            "comparisons": values.count("comparison"),
        }
    safe("min_max", minmax_probe)

    def reverse_probe():
        values = InstrumentedSequence(range(20))
        result = module.reverse_in_place(values)
        return {
            "result": unwrap(result),
            "correct_final_state": values.snapshot() == list(reversed(range(20))),
            "reads": values.count("read"),
            "writes": values.count("write"),
            "slice_reads": values.count("slice_read"),
            "slice_writes": values.count("slice_write"),
        }
    safe("reverse_in_place", reverse_probe)

    def running_probe():
        values = InstrumentedSequence([-1] + [10] * 1000)
        result = module.first_negative_running_sum(values)
        return {
            "result": unwrap(result),
            "reads": values.count("read"),
            "iterations": values.count("iteration_start"),
            "slices": values.count("slice_read"),
            "early_exit": values.count("read") == 1,
        }
    safe("first_negative_running_sum", running_probe)

    def scores_probe():
        values = InstrumentedSequence([10, 50, 70, 100, 0, 90])
        result = module.analyse_scores(values, 50)
        return {
            "result": unwrap(result),
            "reads": values.count("read"),
            "writes": values.count("write"),
            "iterations": values.count("iteration_start"),
            "slices": values.count("slice_read"),
        }
    safe("analyse_scores", scores_probe)

    return out


def growth_exponent(cost_n, cost_2n):
    if cost_n <= 0 or cost_2n <= 0:
        return None
    return math.log(cost_2n / cost_n, 2)


def complexity_observations(module):
    results = {}

    probes = {
        "first_index": lambda n: (InstrumentedSequence(range(n)), (10**9,)),
        "min_max": lambda n: (InstrumentedSequence(range(n)), ()),
        "first_negative_running_sum": lambda n: (InstrumentedSequence([1] * n), ()),
        "analyse_scores": lambda n: (InstrumentedSequence([50] * n), (50,)),
    }

    for name, maker in probes.items():
        function = getattr(module, name)
        measurements = []
        error = None
        for n in (64, 128, 256, 512):
            try:
                values, extra = maker(n)
                function(values, *extra)
                cost = values.count("read")
                measurements.append((n, cost))
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                break

        exponents = []
        if not error and len(measurements) >= 2:
            for left, right in zip(measurements, measurements[1:]):
                exponent = growth_exponent(left[1], right[1])
                if exponent is not None:
                    exponents.append(exponent)

        median = None
        if exponents:
            ordered = sorted(exponents)
            median = ordered[len(ordered) // 2]

        results[name] = {
            "measurements": measurements,
            "doubling_exponents": exponents,
            "median_exponent": median,
            "error": error,
        }

    return results


def trace_function(function, *args):
    filename = function.__code__.co_filename
    line_counts = Counter()
    call_counts = Counter()
    stdout = StringIO()
    stderr = StringIO()

    def tracer(frame, event, arg):
        if frame.f_code.co_filename == filename:
            if event == "line":
                line_counts[frame.f_lineno] += 1
            elif event == "call":
                call_counts[frame.f_code.co_name] += 1
        return tracer

    old_trace = sys.gettrace()
    try:
        sys.settrace(tracer)
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = function(*args)
    finally:
        sys.settrace(old_trace)

    return {
        "result": unwrap(result),
        "line_counts": dict(sorted(line_counts.items())),
        "call_counts": dict(sorted(call_counts.items())),
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
    }


def memory_probe(function, *args):
    tracemalloc.start()
    try:
        function(*args)
        current, peak = tracemalloc.get_traced_memory()
        return {"current_bytes": current, "peak_bytes": peak}
    finally:
        tracemalloc.stop()


def evaluate(path: Path):
    module = load_module(path)
    tree, functions = parse_functions(path)
    static = static_observations(functions)
    functional = functional_checks(module)
    methods = methodological_findings(static)
    runtime = runtime_observations(module)
    complexity = complexity_observations(module)

    try:
        trace = trace_function(module.min_max, [7, 2, 9, 4])
    except Exception as exc:
        trace = {"error": f"{type(exc).__name__}: {exc}"}

    memory = {}
    for name, args in {
        "min_max": (list(range(10000)),),
        "first_negative_running_sum": ([1] * 10000,),
        "analyse_scores": ([50] * 10000, 50),
    }.items():
        try:
            memory[name] = memory_probe(getattr(module, name), *args)
        except Exception as exc:
            memory[name] = {"error": f"{type(exc).__name__}: {exc}"}

    functional_passed = sum(item["passed"] for item in functional.values())
    functional_total = sum(item["total"] for item in functional.values())
    method_issue_count = sum(len(items) for items in methods.values())

    return {
        "solution": str(path),
        "summary": {
            "functional_passed": functional_passed,
            "functional_total": functional_total,
            "method_issue_count": method_issue_count,
        },
        "functional": functional,
        "static": static,
        "method_findings": methods,
        "runtime": runtime,
        "complexity": complexity,
        "trace": trace,
        "memory": memory,
    }


def to_markdown(data):
    lines = [
        "# List 01 implementation report",
        "",
        f"Solution: {data['solution']}",
        "",
        "## Summary",
        "",
        f"- Functional checks: {data['summary']['functional_passed']}/{data['summary']['functional_total']}",
        f"- Methodological findings: {data['summary']['method_issue_count']}",
        "",
        "## Functional correctness",
        "",
        "| Function | Passed | Total |",
        "|---|---:|---:|",
    ]
    for name, item in data["functional"].items():
        lines.append(f"| {name} | {item['passed']} | {item['total']} |")

    lines += ["", "## Methodological findings", ""]
    for name, issues in data["method_findings"].items():
        if issues:
            lines.append(f"- {name}: " + "; ".join(issues))
        else:
            lines.append(f"- {name}: none")

    lines += ["", "## Runtime observations", ""]
    for name, item in data["runtime"].items():
        lines.append(f"### {name}")
        lines.append("")
        for key, value in item.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    lines += ["## Empirical growth", ""]
    for name, item in data["complexity"].items():
        lines.append(f"### {name}")
        lines.append("")
        if item["error"]:
            lines.append(f"- error: {item['error']}")
        else:
            lines.append(f"- measurements: {item['measurements']}")
            lines.append(f"- doubling exponents: {[round(x, 3) for x in item['doubling_exponents']]}")
            median = item["median_exponent"]
            lines.append(f"- median exponent: {None if median is None else round(median, 3)}")
        lines.append("")

    lines += ["## Control-flow trace", ""]
    for key, value in data["trace"].items():
        lines.append(f"- {key}: {value}")

    lines += ["", "## Memory diagnostics", ""]
    for name, item in data["memory"].items():
        lines.append(f"- {name}: {item}")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", required=True, type=Path)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    data = evaluate(args.solution)
    markdown = to_markdown(data)

    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown, encoding="utf-8")
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(markdown)


if __name__ == "__main__":
    main()
