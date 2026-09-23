"""Render student-facing GitHub Issue feedback from a List 02 report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def render_feedback(data: dict, profile: str, source_sha: str) -> str:
    summary = data["summary"]
    lines = [
        "# List 02 — automated technical feedback",
        "",
        f"Analysed revision: `{source_sha}`",
        f"Demonstration profile: **{profile}**",
        "",
        "## Summary",
        "",
        f"- functional checks: **{summary['functional_passed']}/{summary['functional_total']}**",
        f"- methodological findings: **{summary['method_issue_count']}**",
        "",
    ]

    failures = []
    for name, result in data["functional"].items():
        if result["passed"] != result["total"]:
            failed_cases = [
                case["case"]
                for case in result["cases"]
                if not case["pass"]
            ]
            failures.append((name, result["passed"], result["total"], failed_cases))

    if failures:
        lines += ["## Correctness issues", ""]
        for name, passed, total, cases in failures:
            lines.append(
                f"- `{name}`: {passed}/{total} checks passed; "
                f"failing cases: {', '.join(cases)}."
            )
        lines.append("")
    else:
        lines += [
            "## Correctness",
            "",
            "All functional checks in this demonstration pass.",
            "",
        ]

    method_items = [
        (name, issues)
        for name, issues in data["method_findings"].items()
        if issues
    ]
    if method_items:
        lines += ["## Implementation observations", ""]
        for name, issues in method_items:
            lines.append(f"- `{name}`: " + "; ".join(issues) + ".")
        lines.append("")

    runtime = data["runtime"]
    complexity = data["complexity"]

    binary = runtime.get("binary_search", {})
    binary_growth = complexity.get("binary_search", {})
    if binary.get("ok") and (
        not binary.get("logarithmic_probe", True)
        or binary_growth.get("max_reads", 0) > 32
    ):
        lines += [
            "## Binary-search access pattern",
            "",
            f"The large absent-target probe performed **{binary.get('reads')}** reads.",
            "",
            "The task expects interval halving. Keep low/high bounds and inspect only the midpoint of the current search interval.",
            "",
        ]

    insertion = runtime.get("insertion_sort_in_place", {})
    if insertion.get("ok") and not insertion.get("stable", True):
        lines += [
            "## Stability",
            "",
            "The insertion-sort probe changes the relative order of equal keys.",
            "",
            "Insertion sort in this task must be stable. Shift only elements that are strictly greater than the key.",
            "",
        ]

    selection = runtime.get("selection_sort_in_place", {})
    if selection.get("ok") and not selection.get("limited_data_movement", True):
        lines += [
            "## Selection-sort data movement",
            "",
            f"The probe observed **{selection.get('writes')}** writes for 64 elements.",
            "",
            "Canonical selection sort searches for the minimum first and performs at most one swap per outer iteration.",
            "",
        ]

    merge = runtime.get("merge_sorted", {})
    if merge.get("ok") and not merge.get("stable", True):
        lines += [
            "## Merge stability",
            "",
            "The merge probe does not preserve the original order of equal keys.",
            "",
            "When keys compare equal, emit the item from the left input first.",
            "",
        ]

    merge_linear_growth = complexity.get("merge_sorted", {})
    merge_linear_exp = merge_linear_growth.get("median_exponent")
    if merge_linear_exp is not None and merge_linear_exp > 1.5:
        lines += [
            "## Merge complexity signal",
            "",
            f"For `merge_sorted`, the measured comparison-growth exponent is approximately **{merge_linear_exp:.3f}**.",
            "",
            "The merge step should be linear in the combined input size. Advance one of the two input cursors after each comparison instead of re-sorting the combined data.",
            "",
        ]

    merge_growth = complexity.get("merge_sort", {})
    merge_exp = merge_growth.get("median_exponent")
    if merge_exp is not None and merge_exp > 1.5:
        lines += [
            "## Merge-sort complexity signal",
            "",
            f"The measured comparison-growth exponent is approximately **{merge_exp:.3f}**.",
            "",
            "This is substantially above the expected n log n pattern. Use recursive splitting and linear merging rather than a quadratic sorting method.",
            "",
        ]

    quick_growth = complexity.get("quick_sort", {})
    quick_exp = quick_growth.get("median_exponent")
    if quick_exp is not None and quick_exp > 1.5:
        lines += [
            "## Quicksort complexity signal",
            "",
            f"The measured comparison-growth exponent is approximately **{quick_exp:.3f}** on deterministic shuffled inputs.",
            "",
            "The implementation is sorting correctly, but its measured growth is closer to a quadratic method than to quicksort's expected average behaviour.",
            "",
        ]

    if not failures and not method_items:
        lines += [
            "## Result",
            "",
            "No technical correction is suggested by the current automated checks.",
            "",
        ]

    lines += [
        "---",
        "",
        "This feedback is generated from versioned technical evidence. "
        "It is intended to support revision of the implementation and is not a standalone final grade.",
    ]

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-json", required=True, type=Path)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    data = json.loads(args.report_json.read_text(encoding="utf-8"))
    feedback = render_feedback(data, args.profile, args.source_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(feedback, encoding="utf-8")
    print(feedback)


if __name__ == "__main__":
    main()
