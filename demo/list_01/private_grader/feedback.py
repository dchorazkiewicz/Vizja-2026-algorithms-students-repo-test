"""Render a concise student-facing GitHub Issue draft from a technical report.

The full JSON/Markdown report remains the technical evidence.  This renderer
turns the most relevant observations into actionable feedback that could be
posted to the student's fork.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def render_feedback(data: dict, profile: str, source_sha: str) -> str:
    summary = data["summary"]
    lines = [
        "# List 01 — automated technical feedback",
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

    failed_functions = []
    for name, result in data["functional"].items():
        if result["passed"] != result["total"]:
            failed = [case["case"] for case in result["cases"] if not case["pass"]]
            failed_functions.append((name, result["passed"], result["total"], failed))

    if failed_functions:
        lines += ["## Correctness issues", ""]
        for name, passed, total, failed in failed_functions:
            lines.append(
                f"- `{name}`: {passed}/{total} checks passed; "
                f"failing cases: {', '.join(failed)}."
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

    first_index = runtime.get("first_index", {})
    if first_index.get("ok") and not first_index.get("early_exit", True):
        lines += [
            "## Early termination",
            "",
            f"`first_index` returned the correct result in the probe, but inspected "
            f"**{first_index.get('reads')}** elements and visited "
            f"`{first_index.get('visited_indices')}`.",
            "",
            "The target was available earlier. Return immediately once the first occurrence is known.",
            "",
        ]

    min_max = runtime.get("min_max", {})
    if min_max.get("ok") and min_max.get("iterations", 0) >= 2:
        lines += [
            "## Repeated traversal",
            "",
            f"`min_max` started **{min_max.get('iterations')}** full sequence iterations "
            f"and performed **{min_max.get('reads')}** reads in the runtime probe.",
            "",
            "The task asks for one pass. Keep the current minimum and maximum while traversing the data once.",
            "",
        ]

    scores = runtime.get("analyse_scores", {})
    if scores.get("ok") and scores.get("iterations", 0) > 1:
        lines += [
            "## Repeated work in score analysis",
            "",
            f"`analyse_scores` started **{scores.get('iterations')}** sequence iterations "
            f"and performed **{scores.get('reads')}** reads in the probe.",
            "",
            "Accumulate total, minimum, maximum, and passing count in the same traversal.",
            "",
        ]

    growth = data["complexity"].get("first_negative_running_sum", {})
    exponent = growth.get("median_exponent")
    if exponent is not None and exponent > 1.5:
        lines += [
            "## Complexity signal",
            "",
            f"For `first_negative_running_sum`, the measured doubling exponent is "
            f"approximately **{exponent:.3f}**.",
            "",
            f"Measured reads: `{growth.get('measurements')}`.",
            "",
            "This is consistent with substantially worse than linear growth. "
            "Maintain a running sum instead of recomputing prefixes.",
            "",
        ]

    if not failed_functions and not method_items:
        lines += [
            "## Result",
            "",
            "No technical correction is suggested by the current automated checks.",
            "",
        ]

    lines += [
        "---",
        "",
        "This message is generated from automated technical evidence. "
        "It is intended as feedback on the implementation, not as a standalone final grade.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
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
