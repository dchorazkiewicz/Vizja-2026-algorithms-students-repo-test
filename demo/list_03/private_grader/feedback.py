"""Render student-facing GitHub Issue feedback from List 03 evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def render_feedback(data, profile, source_sha):
    summary = data["summary"]
    lines = [
        "# List 03 — automated technical feedback",
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
            failed = [case["case"] for case in result["cases"] if not case["pass"]]
            failures.append((name, result["passed"], result["total"], failed))

    if failures:
        lines += ["## Correctness issues", ""]
        for name, passed, total, failed in failures:
            lines.append(
                f"- `{name}`: {passed}/{total} checks passed; "
                f"failing cases: {', '.join(failed)}."
            )
        lines.append("")
    else:
        lines += ["## Correctness", "", "All functional checks in this demonstration pass.", ""]

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

    search = runtime.get("bst_contains", {})
    if search.get("ok") and search.get("balanced_key_reads", 0) > 64:
        lines += [
            "## BST search path",
            "",
            f"On a balanced BST with 4,095 nodes, the probe observed **{search.get('balanced_key_reads')}** key reads.",
            "",
            "A BST search should follow one root-to-leaf path. Avoid materialising a full traversal before searching.",
            "",
        ]
    elif search.get("ok"):
        lines += [
            "## Tree shape matters",
            "",
            f"Balanced-tree probe: **{search.get('balanced_key_reads')}** key reads.",
            f"Degenerate right-chain probe: **{search.get('skewed_key_reads')}** key reads.",
            "",
            "This contrast is expected: BST search is O(h), so a balanced tree and a degenerate tree with the same operation can behave very differently.",
            "",
        ]

    insert = runtime.get("bst_insert", {})
    if insert.get("ok"):
        if insert.get("node_created_for_new_key", 0) > 1 or insert.get("link_writes_for_new_key", 0) > 2:
            lines += [
                "## BST insertion locality",
                "",
                f"One new-key insertion created **{insert.get('node_created_for_new_key')}** nodes and performed **{insert.get('link_writes_for_new_key')}** link writes.",
                "",
                "The task expects a local insertion: follow one search path, allocate one node, and change one child link.",
                "",
            ]
        if insert.get("node_created_for_duplicate", 0) > 0:
            lines += [
                "## Duplicate handling",
                "",
                f"Inserting an existing key created **{insert.get('node_created_for_duplicate')}** new node(s).",
                "",
                "Duplicate keys must be ignored without changing the tree.",
                "",
            ]

    validator = runtime.get("is_valid_bst", {})
    if validator.get("ok") and validator.get("deep_invalid_result") is True:
        lines += [
            "## Global BST invariant",
            "",
            "The validator accepted a tree whose direct parent/child comparisons look valid locally but whose deeper node violates an ancestor bound.",
            "",
            "Carry lower and upper bounds through the recursion. Checking only immediate children is not sufficient.",
            "",
        ]

    avl = runtime.get("avl_insert", {})
    if avl.get("ok"):
        if not avl.get("valid_avl", True):
            lines += [
                "## AVL invariant",
                "",
                f"After inserting 64 ascending keys, the resulting tree has height **{avl.get('actual_height')}** and fails the AVL invariant.",
                "",
                "Update heights on the recursive return path and apply the appropriate LL, RR, LR or RL rotation when the balance factor leaves [-1, 1].",
                "",
            ]
        elif avl.get("nodes_created_across_64_insertions", 0) > 256:
            lines += [
                "## AVL update cost",
                "",
                f"Across 64 insertions the probe observed **{avl.get('nodes_created_across_64_insertions')}** node allocations and **{avl.get('total_rotations')}** rotation calls.",
                "",
                "The final tree is valid, but the implementation is rebuilding large parts of the tree. AVL insertion should allocate one node per new key and repair balance locally with rotations.",
                "",
            ]
        else:
            lines += [
                "## AVL structural evidence",
                "",
                f"64 ascending insertions produced height **{avl.get('actual_height')}**, "
                f"with **{avl.get('nodes_created_across_64_insertions')}** node allocations and "
                f"**{avl.get('total_rotations')}** observed rotations.",
                "",
            ]

    allocation = data["complexity"].get("avl_cumulative_node_allocations", {})
    exponent = allocation.get("median_exponent")
    if exponent is not None and exponent > 1.5:
        lines += [
            "## AVL allocation-growth signal",
            "",
            f"Cumulative node-allocation growth has an empirical exponent of approximately **{exponent:.3f}**.",
            "",
            "That is consistent with repeated whole-tree rebuilding rather than local O(log n) AVL updates.",
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
