"""Multi-layer evaluator for List 02 searching and sorting submissions."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import random
import sys
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from demo.list_02.private_grader.ast_checks import function_metrics, function_node, parse_file
from demo.list_02.private_grader.complexity import (
    adjacent_exponents,
    median,
    nlogn_ratio,
    peak_allocated_bytes,
)
from demo.list_02.private_grader.instrumentation import (
    InstrumentedSequence,
    Ledger,
    TrackedItem,
    is_stable_tagged,
    tagged_output,
    unwrap,
)


FUNCTIONS = (
    "binary_search",
    "insertion_sort_in_place",
    "selection_sort_in_place",
    "merge_sorted",
    "merge_sort",
    "quick_sort_in_place",
)


class StableProbe:
    def __init__(self, key, tag):
        self.key = key
        self.tag = tag

    @staticmethod
    def _key(other):
        return other.key if isinstance(other, StableProbe) else other

    def __lt__(self, other): return self.key < self._key(other)
    def __le__(self, other): return self.key <= self._key(other)
    def __gt__(self, other): return self.key > self._key(other)
    def __ge__(self, other): return self.key >= self._key(other)
    def __eq__(self, other): return self.key == self._key(other)

    def __repr__(self):
        return f"StableProbe({self.key!r}, {self.tag!r})"


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("list02_submission", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stable_tags(values) -> bool:
    groups = {}
    for item in values:
        groups.setdefault(item.key, []).append(item.tag)
    return all(tags == sorted(tags) for tags in groups.values())


def functional_checks(module):
    results = {}

    def run(name, cases):
        passed = 0
        details = []
        for label, callback in cases:
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
        results[name] = {"passed": passed, "total": len(cases), "cases": details}

    run("binary_search", [
        ("empty", lambda: module.binary_search([], 3) == -1),
        ("single-hit", lambda: module.binary_search([3], 3) == 0),
        ("absent", lambda: module.binary_search([1, 3, 5, 7], 4) == -1),
        ("leftmost-duplicate", lambda: module.binary_search([1, 2, 2, 2, 4], 2) == 1),
        ("boundary", lambda: module.binary_search([1, 3, 5, 7], 7) == 3),
    ])

    def sort_in_place_case(function, values):
        original = values
        expected = sorted(values)
        result = function(values)
        return result is None and values is original and values == expected

    run("insertion_sort_in_place", [
        ("empty", lambda: sort_in_place_case(module.insertion_sort_in_place, [])),
        ("single", lambda: sort_in_place_case(module.insertion_sort_in_place, [4])),
        ("mixed", lambda: sort_in_place_case(module.insertion_sort_in_place, [5, 1, 4, 2, 8])),
        ("duplicates", lambda: sort_in_place_case(module.insertion_sort_in_place, [3, 1, 3, 2, 1])),
        ("reverse", lambda: sort_in_place_case(module.insertion_sort_in_place, [5, 4, 3, 2, 1])),
        ("stable", lambda: _stable_in_place(module.insertion_sort_in_place)),
    ])

    run("selection_sort_in_place", [
        ("empty", lambda: sort_in_place_case(module.selection_sort_in_place, [])),
        ("single", lambda: sort_in_place_case(module.selection_sort_in_place, [4])),
        ("mixed", lambda: sort_in_place_case(module.selection_sort_in_place, [5, 1, 4, 2, 8])),
        ("duplicates", lambda: sort_in_place_case(module.selection_sort_in_place, [3, 1, 3, 2, 1])),
        ("reverse", lambda: sort_in_place_case(module.selection_sort_in_place, [5, 4, 3, 2, 1])),
    ])

    def merge_case(left, right):
        left_before = list(left)
        right_before = list(right)
        result = module.merge_sorted(left, right)
        return result == sorted(left + right) and left == left_before and right == right_before

    run("merge_sorted", [
        ("both-empty", lambda: merge_case([], [])),
        ("left-empty", lambda: merge_case([], [1, 2, 3])),
        ("interleaved", lambda: merge_case([1, 3, 5], [2, 4, 6])),
        ("duplicates", lambda: merge_case([1, 2, 2], [2, 2, 3])),
        ("stable", lambda: _stable_merge(module.merge_sorted)),
    ])

    def returned_sort_case(function, values):
        before = list(values)
        result = function(values)
        return result == sorted(values) and values == before and result is not values

    run("merge_sort", [
        ("empty", lambda: returned_sort_case(module.merge_sort, [])),
        ("single", lambda: returned_sort_case(module.merge_sort, [4])),
        ("mixed", lambda: returned_sort_case(module.merge_sort, [5, 1, 4, 2, 8])),
        ("duplicates", lambda: returned_sort_case(module.merge_sort, [3, 1, 3, 2, 1])),
        ("stable", lambda: _stable_returned(module.merge_sort)),
    ])

    run("quick_sort_in_place", [
        ("empty", lambda: sort_in_place_case(module.quick_sort_in_place, [])),
        ("single", lambda: sort_in_place_case(module.quick_sort_in_place, [4])),
        ("mixed", lambda: sort_in_place_case(module.quick_sort_in_place, [5, 1, 4, 2, 8])),
        ("duplicates", lambda: sort_in_place_case(module.quick_sort_in_place, [3, 1, 3, 2, 1])),
        ("reverse", lambda: sort_in_place_case(module.quick_sort_in_place, [5, 4, 3, 2, 1])),
    ])

    return results


def _stable_in_place(function):
    values = [
        StableProbe(2, 0),
        StableProbe(1, 1),
        StableProbe(2, 2),
        StableProbe(1, 3),
        StableProbe(2, 4),
    ]
    function(values)
    return [item.key for item in values] == [1, 1, 2, 2, 2] and stable_tags(values)


def _stable_merge(function):
    left = [StableProbe(1, 0), StableProbe(2, 1), StableProbe(2, 2)]
    right = [StableProbe(2, 3), StableProbe(2, 4), StableProbe(3, 5)]
    result = function(left, right)
    return [item.key for item in result] == [1, 2, 2, 2, 2, 3] and stable_tags(result)


def _stable_returned(function):
    values = [
        StableProbe(2, 0),
        StableProbe(1, 1),
        StableProbe(2, 2),
        StableProbe(1, 3),
        StableProbe(2, 4),
    ]
    result = function(values)
    return [item.key for item in result] == [1, 1, 2, 2, 2] and stable_tags(result)


def static_observations(path: Path):
    tree = parse_file(path)
    output = {}
    for name in FUNCTIONS:
        try:
            node = function_node(tree, name)
            output[name] = {"missing": False, **function_metrics(node)}
        except AssertionError:
            output[name] = {"missing": True}
    return output


def methodological_findings(static):
    rules = {
        "binary_search": {
            "min_loop_depth": 1,
            "banned": {"index", "bisect", "bisect_left", "bisect_right", "sorted", "sort"},
            "ban_slice": True,
            "ban_membership": True,
            "require_recursion": False,
        },
        "insertion_sort_in_place": {
            "min_loop_depth": 2,
            "banned": {"sorted", "sort"},
            "ban_slice": True,
            "ban_membership": False,
            "require_recursion": False,
        },
        "selection_sort_in_place": {
            "min_loop_depth": 2,
            "banned": {"sorted", "sort"},
            "ban_slice": True,
            "ban_membership": False,
            "require_recursion": False,
        },
        "merge_sorted": {
            "min_loop_depth": 1,
            "banned": {"sorted", "sort"},
            "ban_slice": False,
            "ban_membership": False,
            "require_recursion": False,
        },
        "merge_sort": {
            "min_loop_depth": 0,
            "banned": {"sorted", "sort"},
            "ban_slice": False,
            "ban_membership": False,
            "require_recursion": True,
        },
        "quick_sort_in_place": {
            "min_loop_depth": 1,
            "banned": {"sorted", "sort"},
            "ban_slice": True,
            "ban_membership": False,
            "require_recursion": True,
        },
    }

    findings = {}
    for name, rule in rules.items():
        item = static[name]
        issues = []
        if item.get("missing"):
            findings[name] = ["function missing"]
            continue

        if item["max_loop_depth"] < rule["min_loop_depth"]:
            issues.append(
                f"loop nesting too shallow for requested method: {item['max_loop_depth']}"
            )

        banned = sorted(set(item["calls"]) & rule["banned"])
        if banned:
            issues.append("banned shortcut calls: " + ", ".join(banned))

        if rule["ban_slice"] and item["slice"]:
            issues.append("slicing detected")

        if rule["ban_membership"] and item["membership"]:
            issues.append("membership search detected")

        if rule["require_recursion"] and not item["recursive_functions"]:
            issues.append("required recursive structure not detected")

        findings[name] = issues

    return findings


def runtime_observations(module):
    output = {}

    def safe(name, callback):
        try:
            output[name] = {"ok": True, **callback()}
        except Exception as exc:
            output[name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    def binary_probe():
        values = InstrumentedSequence(range(4096))
        result = module.binary_search(values, 4097)
        return {
            "result": result,
            "reads": values.count("read"),
            "writes": values.count("write"),
            "visited_indices": values.visited_indices(),
            "logarithmic_probe": values.count("read") <= 20,
        }
    safe("binary_search", binary_probe)

    def insertion_probe():
        sorted_values = InstrumentedSequence(range(64), track_items=True)
        module.insertion_sort_in_place(sorted_values)

        reverse_values = InstrumentedSequence(range(63, -1, -1), track_items=True)
        module.insertion_sort_in_place(reverse_values)

        stable_values = InstrumentedSequence([2, 1, 2, 1, 2], track_items=True)
        module.insertion_sort_in_place(stable_values)
        tagged = stable_values.tagged_snapshot()

        return {
            "sorted_input_comparisons": sorted_values.count("comparison"),
            "sorted_input_writes": sorted_values.count("write"),
            "reverse_input_comparisons": reverse_values.count("comparison"),
            "reverse_input_writes": reverse_values.count("write"),
            "stable": is_stable_tagged(tagged),
            "tagged_result": tagged,
        }
    safe("insertion_sort_in_place", insertion_probe)

    def selection_probe():
        values = InstrumentedSequence(range(63, -1, -1), track_items=True)
        module.selection_sort_in_place(values)
        n = len(values)
        expected_comparisons = n * (n - 1) // 2
        return {
            "comparisons": values.count("comparison"),
            "expected_canonical_comparisons": expected_comparisons,
            "writes": values.count("write"),
            "canonical_comparison_count": values.count("comparison") == expected_comparisons,
            "limited_data_movement": values.count("write") <= 2 * (n - 1),
        }
    safe("selection_sort_in_place", selection_probe)

    def merge_probe():
        ledger = Ledger()
        left = InstrumentedSequence([1, 2, 2, 5], track_items=True, ledger=ledger, tag_offset=0)
        right = InstrumentedSequence([2, 2, 3, 6], track_items=True, ledger=ledger, tag_offset=4)
        result = module.merge_sorted(left, right)
        tagged = tagged_output(result)
        return {
            "result": [key for key, _ in tagged],
            "comparisons": ledger.counts["comparison"],
            "reads": ledger.counts["read"],
            "input_writes": ledger.counts["write"],
            "stable": is_stable_tagged(tagged),
            "tagged_result": tagged,
        }
    safe("merge_sorted", merge_probe)

    def merge_sort_probe():
        values = InstrumentedSequence([4, 2, 4, 1, 2, 3, 1], track_items=True)
        result = module.merge_sort(values)
        tagged = tagged_output(result)
        trace = trace_calls(module.merge_sort, [5, 1, 4, 2, 8, 3, 7, 6])
        return {
            "result": [key for key, _ in tagged],
            "input_writes": values.count("write"),
            "comparisons": values.count("comparison"),
            "stable": is_stable_tagged(tagged),
            "recursive_calls": trace["total_calls"],
            "max_call_depth": trace["max_depth"],
        }
    safe("merge_sort", merge_sort_probe)

    def quick_probe():
        data = list(range(128))
        random.Random(2026).shuffle(data)
        values = InstrumentedSequence(data, track_items=True)
        trace = trace_calls(module.quick_sort_in_place, list(data))
        result = module.quick_sort_in_place(values)
        return {
            "returned": result,
            "sorted": values.snapshot() == sorted(data),
            "reads": values.count("read"),
            "writes": values.count("write"),
            "comparisons": values.count("comparison"),
            "slice_reads": values.count("slice_read"),
            "slice_writes": values.count("slice_write"),
            "recursive_calls": trace["total_calls"],
            "max_call_depth": trace["max_depth"],
        }
    safe("quick_sort_in_place", quick_probe)

    return output


def trace_calls(function, *args):
    filename = function.__code__.co_filename
    calls = Counter()
    current_depth = 0
    max_depth = 0

    def tracer(frame, event, arg):
        nonlocal current_depth, max_depth
        if frame.f_code.co_filename != filename:
            return tracer
        if event == "call":
            calls[frame.f_code.co_name] += 1
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif event == "return":
            current_depth -= 1
        return tracer

    previous = sys.gettrace()
    try:
        sys.settrace(tracer)
        function(*args)
    finally:
        sys.settrace(previous)

    return {
        "calls": dict(sorted(calls.items())),
        "total_calls": sum(calls.values()),
        "max_depth": max_depth,
    }


def complexity_observations(module):
    output = {}

    binary_measurements = []
    for n in (128, 256, 512, 1024, 2048, 4096):
        values = InstrumentedSequence(range(n))
        module.binary_search(values, n + 1)
        binary_measurements.append((n, values.count("read")))
    output["binary_search"] = {
        "measurements": binary_measurements,
        "max_reads": max(cost for _, cost in binary_measurements),
    }

    def sort_measurements(function, sizes, maker):
        measurements = []
        for n in sizes:
            values = InstrumentedSequence(maker(n), track_items=True)
            function(values)
            measurements.append((n, max(1, values.count("comparison"))))
        exponents = adjacent_exponents(measurements)
        return {
            "measurements": measurements,
            "doubling_exponents": exponents,
            "median_exponent": median(exponents),
        }

    output["insertion_reverse"] = sort_measurements(
        module.insertion_sort_in_place,
        (32, 64, 128, 256),
        lambda n: list(range(n - 1, -1, -1)),
    )
    output["insertion_sorted"] = sort_measurements(
        module.insertion_sort_in_place,
        (32, 64, 128, 256),
        lambda n: list(range(n)),
    )
    output["selection_reverse"] = sort_measurements(
        module.selection_sort_in_place,
        (32, 64, 128, 256),
        lambda n: list(range(n - 1, -1, -1)),
    )

    merge_measurements = []
    for n in (128, 256, 512, 1024):
        ledger = Ledger()
        left = InstrumentedSequence(range(0, n, 2), track_items=True, ledger=ledger, tag_offset=0)
        right = InstrumentedSequence(range(1, n, 2), track_items=True, ledger=ledger, tag_offset=n // 2)
        module.merge_sorted(left, right)
        merge_measurements.append((n, max(1, ledger.counts["comparison"])))
    merge_exponents = adjacent_exponents(merge_measurements)
    output["merge_sorted"] = {
        "measurements": merge_measurements,
        "doubling_exponents": merge_exponents,
        "median_exponent": median(merge_exponents),
    }

    def returned_sort_measurements(function, sizes):
        measurements = []
        for n in sizes:
            data = list(range(n))
            random.Random(1000 + n).shuffle(data)
            ledger = Ledger()
            tracked = [
                TrackedItem(value, index, ledger)
                for index, value in enumerate(data)
            ]
            function(tracked)
            measurements.append((n, max(1, ledger.counts["comparison"])))
        exponents = adjacent_exponents(measurements)
        return {
            "measurements": measurements,
            "doubling_exponents": exponents,
            "median_exponent": median(exponents),
            "nlogn_ratios": [
                (n, nlogn_ratio(n, cost))
                for n, cost in measurements
            ],
        }

    output["merge_sort"] = returned_sort_measurements(
        module.merge_sort, (64, 128, 256, 512)
    )

    quick_measurements = []
    for n in (64, 128, 256, 512):
        data = list(range(n))
        random.Random(2000 + n).shuffle(data)
        values = InstrumentedSequence(data, track_items=True)
        module.quick_sort_in_place(values)
        quick_measurements.append((n, max(1, values.count("comparison"))))
    quick_exponents = adjacent_exponents(quick_measurements)
    output["quick_sort"] = {
        "measurements": quick_measurements,
        "doubling_exponents": quick_exponents,
        "median_exponent": median(quick_exponents),
        "nlogn_ratios": [
            (n, nlogn_ratio(n, cost))
            for n, cost in quick_measurements
        ],
    }

    return output


def memory_observations(module):
    output = {}
    cases = {
        "insertion_sort_in_place": (module.insertion_sort_in_place, [256, 255, *range(254, -1, -1)]),
        "selection_sort_in_place": (module.selection_sort_in_place, list(range(255, -1, -1))),
        "merge_sort": (module.merge_sort, list(range(1023, -1, -1))),
        "quick_sort_in_place": (module.quick_sort_in_place, list(range(1023, -1, -1))),
    }

    for name, (function, values) in cases.items():
        try:
            _, peak = peak_allocated_bytes(function, values)
            output[name] = {"peak_bytes": peak}
        except Exception as exc:
            output[name] = {"error": f"{type(exc).__name__}: {exc}"}

    return output


def capture_output(module):
    out = StringIO()
    err = StringIO()
    try:
        with redirect_stdout(out), redirect_stderr(err):
            module.binary_search([1, 3, 5], 3)
        return {"stdout": out.getvalue(), "stderr": err.getvalue()}
    except Exception as exc:
        return {"error": f"{type(exc).__name__}: {exc}"}


def evaluate(path: Path):
    module = load_module(path)
    functional = functional_checks(module)
    static = static_observations(path)
    methods = methodological_findings(static)
    runtime = runtime_observations(module)
    complexity = complexity_observations(module)
    memory = memory_observations(module)
    output_capture = capture_output(module)

    return {
        "solution": str(path),
        "summary": {
            "functional_passed": sum(item["passed"] for item in functional.values()),
            "functional_total": sum(item["total"] for item in functional.values()),
            "method_issue_count": sum(len(items) for items in methods.values()),
        },
        "functional": functional,
        "static": static,
        "method_findings": methods,
        "runtime": runtime,
        "complexity": complexity,
        "memory": memory,
        "output_capture": output_capture,
    }


def to_markdown(data):
    lines = [
        "# List 02 implementation report",
        "",
        f"Solution: `{data['solution']}`",
        "",
        "## Summary",
        "",
        f"- functional checks: **{data['summary']['functional_passed']}/{data['summary']['functional_total']}**",
        f"- methodological findings: **{data['summary']['method_issue_count']}**",
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
        lines.append(f"- `{name}`: " + ("; ".join(issues) if issues else "none"))

    lines += ["", "## Runtime observations", ""]
    for name, values in data["runtime"].items():
        lines += [f"### {name}", ""]
        for key, value in values.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    lines += ["## Empirical complexity evidence", ""]
    for name, values in data["complexity"].items():
        lines += [f"### {name}", ""]
        for key, value in values.items():
            if key == "doubling_exponents":
                value = [round(item, 3) for item in value]
            elif key == "median_exponent" and value is not None:
                value = round(value, 3)
            lines.append(f"- {key}: {value}")
        lines.append("")

    lines += ["## Memory diagnostics", ""]
    for name, values in data["memory"].items():
        lines.append(f"- {name}: {values}")

    lines += ["", "## Output capture", ""]
    lines.append(f"- stdout: `{data['output_capture'].get('stdout', '')}`")
    lines.append(f"- stderr: `{data['output_capture'].get('stderr', '')}`")

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
        args.json_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    print(markdown)


if __name__ == "__main__":
    main()
