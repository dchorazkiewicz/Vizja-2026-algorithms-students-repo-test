"""Multi-layer evaluator for List 03 tree submissions."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from collections import Counter
from pathlib import Path

from demo.list_03.private_grader.ast_checks import function_metrics, function_node, parse_file
from demo.list_03.private_grader.complexity import adjacent_exponents, median, peak_allocated_bytes
from demo.list_03.private_grader.instrumentation import (
    Ledger,
    TrackedNode,
    actual_height,
    build_balanced,
    build_right_skewed,
    child_reads,
    count_nodes,
    generic_key,
    generic_left,
    generic_right,
    inorder_plain,
    is_valid_avl_structure,
    is_valid_bst_structure,
    link_writes,
    unwrap,
    visited_keys,
)


FUNCTIONS = (
    "inorder_keys",
    "bst_contains",
    "bst_insert",
    "bst_height",
    "is_valid_bst",
    "rotate_left",
    "rotate_right",
    "avl_insert",
)


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("list03_submission", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_tree(module, key, left=None, right=None):
    if key is None:
        return None
    node = module.Node(key)
    node.left = left
    node.right = right
    return node


def build_balanced_normal(module, keys):
    keys = list(keys)

    def build(low, high):
        if low >= high:
            return None
        middle = (low + high) // 2
        node = module.Node(keys[middle])
        node.left = build(low, middle)
        node.right = build(middle + 1, high)
        node.height = 1 + max(
            0 if node.left is None else node.left.height,
            0 if node.right is None else node.right.height,
        )
        return node

    return build(0, len(keys))


def normal_inorder(root):
    if root is None:
        return []
    return normal_inorder(root.left) + [root.key] + normal_inorder(root.right)


def normal_height(root):
    if root is None:
        return 0
    return 1 + max(normal_height(root.left), normal_height(root.right))


def normal_count(root):
    if root is None:
        return 0
    return 1 + normal_count(root.left) + normal_count(root.right)


def normal_valid_bst(root):
    def valid(node, lower, upper):
        if node is None:
            return True
        if lower is not None and node.key <= lower:
            return False
        if upper is not None and node.key >= upper:
            return False
        return valid(node.left, lower, node.key) and valid(node.right, node.key, upper)

    return valid(root, None, None)


def normal_valid_avl(root):
    def validate(node):
        if node is None:
            return True, 0, None, None

        left_ok, left_h, left_min, left_max = validate(node.left)
        right_ok, right_h, right_min, right_max = validate(node.right)
        key = node.key
        expected_h = 1 + max(left_h, right_h)

        ok = (
            left_ok
            and right_ok
            and (left_max is None or left_max < key)
            and (right_min is None or key < right_min)
            and abs(left_h - right_h) <= 1
            and node.height == expected_h
        )
        minimum = left_min if left_min is not None else key
        maximum = right_max if right_max is not None else key
        return ok, expected_h, minimum, maximum

    return validate(root)[0]


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

    def sample_tree():
        return make_tree(
            module,
            4,
            make_tree(module, 2, make_tree(module, 1), make_tree(module, 3)),
            make_tree(module, 6, make_tree(module, 5), make_tree(module, 7)),
        )

    run("inorder_keys", [
        ("empty", lambda: module.inorder_keys(None) == []),
        ("single", lambda: module.inorder_keys(module.Node(4)) == [4]),
        ("balanced", lambda: module.inorder_keys(sample_tree()) == [1, 2, 3, 4, 5, 6, 7]),
        ("unbalanced", lambda: module.inorder_keys(make_tree(module, 3, make_tree(module, 2, make_tree(module, 1)), None)) == [1, 2, 3]),
    ])

    run("bst_contains", [
        ("empty", lambda: module.bst_contains(None, 3) is False),
        ("root", lambda: module.bst_contains(sample_tree(), 4) is True),
        ("left", lambda: module.bst_contains(sample_tree(), 1) is True),
        ("right", lambda: module.bst_contains(sample_tree(), 7) is True),
        ("absent", lambda: module.bst_contains(sample_tree(), 8) is False),
    ])

    def insert_case(keys, inserted, expected):
        root = None
        for key in keys:
            root = module.bst_insert(root, key)
        before_count = normal_count(root)
        root = module.bst_insert(root, inserted)
        return (
            normal_inorder(root) == expected
            and normal_valid_bst(root)
            and normal_count(root) <= before_count + 1
        )

    run("bst_insert", [
        ("empty", lambda: insert_case([], 4, [4])),
        ("left", lambda: insert_case([4], 2, [2, 4])),
        ("right", lambda: insert_case([4], 6, [4, 6])),
        ("deep", lambda: insert_case([4, 2, 6, 1, 3], 5, [1, 2, 3, 4, 5, 6])),
        ("duplicate-ignored", lambda: insert_case([4, 2, 6], 2, [2, 4, 6])),
    ])

    run("bst_height", [
        ("empty", lambda: module.bst_height(None) == 0),
        ("leaf", lambda: module.bst_height(module.Node(1)) == 1),
        ("balanced-3", lambda: module.bst_height(sample_tree()) == 3),
        ("left-chain", lambda: module.bst_height(make_tree(module, 3, make_tree(module, 2, make_tree(module, 1)), None)) == 3),
    ])

    deep_invalid = make_tree(
        module,
        10,
        make_tree(module, 5, None, make_tree(module, 12)),
        make_tree(module, 15),
    )
    duplicate_invalid = make_tree(module, 10, make_tree(module, 10), None)

    run("is_valid_bst", [
        ("empty", lambda: module.is_valid_bst(None) is True),
        ("valid", lambda: module.is_valid_bst(sample_tree()) is True),
        ("root-violation", lambda: module.is_valid_bst(make_tree(module, 10, make_tree(module, 12), None)) is False),
        ("deep-global-violation", lambda: module.is_valid_bst(deep_invalid) is False),
        ("duplicate-invalid", lambda: module.is_valid_bst(duplicate_invalid) is False),
    ])

    def left_rotation_case():
        root = module.Node(10)
        root.right = module.Node(20)
        root.right.right = module.Node(30)
        root.height = 3
        root.right.height = 2
        new_root = module.rotate_left(root)
        return (
            new_root.key == 20
            and new_root.left.key == 10
            and new_root.right.key == 30
            and new_root.left.height == 1
            and new_root.height == 2
            and normal_valid_bst(new_root)
        )

    def right_rotation_case():
        root = module.Node(30)
        root.left = module.Node(20)
        root.left.left = module.Node(10)
        root.height = 3
        root.left.height = 2
        new_root = module.rotate_right(root)
        return (
            new_root.key == 20
            and new_root.left.key == 10
            and new_root.right.key == 30
            and new_root.right.height == 1
            and new_root.height == 2
            and normal_valid_bst(new_root)
        )

    run("rotate_left", [
        ("basic-shape-and-heights", left_rotation_case),
        ("subtree-preserved", lambda: _left_subtree_case(module)),
    ])

    run("rotate_right", [
        ("basic-shape-and-heights", right_rotation_case),
        ("subtree-preserved", lambda: _right_subtree_case(module)),
    ])

    run("avl_insert", [
        ("single", lambda: _avl_sequence(module, [10])),
        ("LL", lambda: _avl_sequence(module, [30, 20, 10])),
        ("RR", lambda: _avl_sequence(module, [10, 20, 30])),
        ("LR", lambda: _avl_sequence(module, [30, 10, 20])),
        ("RL", lambda: _avl_sequence(module, [10, 30, 20])),
        ("long-sequence", lambda: _avl_sequence(module, list(range(1, 40)))),
        ("duplicate-ignored", lambda: _avl_duplicate_case(module)),
    ])

    return results


def _left_subtree_case(module):
    root = module.Node(10)
    root.right = module.Node(30)
    root.right.left = module.Node(20)
    root.height = 3
    root.right.height = 2
    new_root = module.rotate_left(root)
    return (
        new_root.key == 30
        and new_root.left.key == 10
        and new_root.left.right.key == 20
        and normal_valid_bst(new_root)
        and new_root.height == 3
    )


def _right_subtree_case(module):
    root = module.Node(30)
    root.left = module.Node(10)
    root.left.right = module.Node(20)
    root.height = 3
    root.left.height = 2
    new_root = module.rotate_right(root)
    return (
        new_root.key == 10
        and new_root.right.key == 30
        and new_root.right.left.key == 20
        and normal_valid_bst(new_root)
        and new_root.height == 3
    )


def _avl_sequence(module, keys):
    root = None
    for key in keys:
        root = module.avl_insert(root, key)
    return normal_inorder(root) == sorted(set(keys)) and normal_valid_avl(root)


def _avl_duplicate_case(module):
    root = None
    for key in [10, 5, 15, 10, 5, 15]:
        root = module.avl_insert(root, key)
    return normal_inorder(root) == [5, 10, 15] and normal_count(root) == 3 and normal_valid_avl(root)


def static_observations(path):
    tree = parse_file(path)
    output = {}
    for name in FUNCTIONS:
        try:
            output[name] = {"missing": False, **function_metrics(function_node(tree, name))}
        except AssertionError:
            output[name] = {"missing": True}
    return output


def methodological_findings(static):
    findings = {}

    for name in FUNCTIONS:
        item = static[name]
        issues = []

        if item.get("missing"):
            findings[name] = ["function missing"]
            continue

        calls = set(item["calls"])
        recursive = bool(item["recursive_functions"])

        if name == "inorder_keys":
            if not recursive:
                issues.append("recursive traversal not detected")
            if calls & {"sorted", "sort"}:
                issues.append("sorting shortcut detected")

        elif name == "bst_contains":
            if item["loops"] == 0 and not recursive:
                issues.append("path traversal structure not detected")
            if "inorder_keys" in calls:
                issues.append("full inorder traversal used for BST search")
            if calls & {"sorted", "sort"}:
                issues.append("sorting shortcut detected")

        elif name == "bst_insert":
            if item["loops"] == 0 and not recursive:
                issues.append("tree traversal structure not detected")
            if calls & {"inorder_keys", "sorted", "sort", "list"}:
                issues.append("whole-tree materialisation/rebuild shortcut detected")

        elif name == "bst_height":
            if not recursive:
                issues.append("required recursive height computation not detected")

        elif name == "is_valid_bst":
            if not recursive:
                issues.append("required recursive global validation not detected")
            if "inorder_keys" in calls:
                issues.append("whole inorder sequence materialised for validation")
            if calls & {"sorted", "sort"}:
                issues.append("sorting shortcut detected")

        elif name == "avl_insert":
            if not recursive:
                issues.append("recursive AVL insertion not detected")
            if "rotate_left" not in calls or "rotate_right" not in calls:
                issues.append("AVL rotation calls not detected")
            if calls & {"inorder_keys", "sorted", "sort"}:
                issues.append("whole-tree rebuild/sort strategy detected")

        findings[name] = issues

    return findings


def deep_invalid_tracked(ledger):
    root = TrackedNode(10, ledger=ledger)
    root._left = TrackedNode(5, ledger=ledger)
    root._left._right = TrackedNode(12, ledger=ledger)
    root._right = TrackedNode(15, ledger=ledger)
    ledger.reset()
    return root


def runtime_observations(module):
    output = {}

    def safe(name, callback):
        try:
            output[name] = {"ok": True, **callback()}
        except Exception as exc:
            output[name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    def inorder_probe():
        ledger = Ledger()
        root = build_balanced(range(127), ledger)
        result = unwrap(module.inorder_keys(root))
        return {
            "correct": result == list(range(127)),
            "key_reads": ledger.counts["key_read"],
            "child_reads": child_reads(ledger),
            "node_count": 127,
        }
    safe("inorder_keys", inorder_probe)

    def search_probe():
        balanced_ledger = Ledger()
        balanced_root = build_balanced(range(4095), balanced_ledger)
        balanced_result = module.bst_contains(balanced_root, 5000)
        balanced_visited = visited_keys(balanced_ledger)

        skewed_ledger = Ledger()
        skewed_root = build_right_skewed(range(512), skewed_ledger)
        skewed_result = module.bst_contains(skewed_root, 9999)
        skewed_visited = visited_keys(skewed_ledger)

        return {
            "balanced_result": balanced_result,
            "balanced_key_reads": balanced_ledger.counts["key_read"],
            "balanced_comparisons": balanced_ledger.counts["comparison"],
            "balanced_visited_count": len(balanced_visited),
            "balanced_visited_sample": balanced_visited[:20],
            "skewed_result": skewed_result,
            "skewed_key_reads": skewed_ledger.counts["key_read"],
            "skewed_visited_count": len(skewed_visited),
        }
    safe("bst_contains", search_probe)

    def insert_probe():
        ledger = Ledger()
        root = build_balanced(range(255), ledger)

        class BoundNode(TrackedNode):
            def __init__(self, key, left=None, right=None, height=1):
                super().__init__(key, left, right, height, ledger=ledger)

        original_node = module.Node
        module.Node = BoundNode
        try:
            result = module.bst_insert(root, 999)
            created = ledger.counts["node_created"]
            writes = link_writes(ledger)
            key_reads = ledger.counts["key_read"]

            ledger.reset()
            result = module.bst_insert(result, 127)
            duplicate_created = ledger.counts["node_created"]
            duplicate_writes = link_writes(ledger)
        finally:
            module.Node = original_node

        return {
            "valid_after_insert": is_valid_bst_structure(result),
            "node_created_for_new_key": created,
            "link_writes_for_new_key": writes,
            "key_reads_for_new_key": key_reads,
            "node_created_for_duplicate": duplicate_created,
            "link_writes_for_duplicate": duplicate_writes,
        }
    safe("bst_insert", insert_probe)

    def height_probe():
        ledger = Ledger()
        root = build_balanced(range(127), ledger)
        result = module.bst_height(root)
        return {
            "result": result,
            "expected": 7,
            "child_reads": child_reads(ledger),
        }
    safe("bst_height", height_probe)

    def validator_probe():
        ledger = Ledger()
        root = deep_invalid_tracked(ledger)
        result = module.is_valid_bst(root)
        return {
            "deep_invalid_result": result,
            "key_reads": ledger.counts["key_read"],
            "child_reads": child_reads(ledger),
        }
    safe("is_valid_bst", validator_probe)

    def rotation_probe():
        ledger = Ledger()
        root = TrackedNode(10, ledger=ledger)
        root._right = TrackedNode(20, ledger=ledger)
        root._right._right = TrackedNode(30, ledger=ledger)
        root._height = 3
        root._right._height = 2
        ledger.reset()

        new_root = module.rotate_left(root)
        return {
            "new_root": generic_key(new_root),
            "valid_bst": is_valid_bst_structure(new_root),
            "link_writes": link_writes(ledger),
            "height_writes": ledger.counts["height_write"],
            "actual_height": actual_height(new_root),
        }
    safe("rotate_left", rotation_probe)

    def avl_probe():
        ledger = Ledger()

        class BoundNode(TrackedNode):
            def __init__(self, key, left=None, right=None, height=1):
                super().__init__(key, left, right, height, ledger=ledger)

        original_node = module.Node
        original_left = module.rotate_left
        original_right = module.rotate_right
        rotations = Counter()

        def counted_left(node):
            rotations["left"] += 1
            return original_left(node)

        def counted_right(node):
            rotations["right"] += 1
            return original_right(node)

        module.Node = BoundNode
        module.rotate_left = counted_left
        module.rotate_right = counted_right

        try:
            root = None
            for key in range(1, 65):
                root = module.avl_insert(root, key)
        finally:
            module.Node = original_node
            module.rotate_left = original_left
            module.rotate_right = original_right

        created = ledger.counts["node_created"]
        return {
            "node_count": count_nodes(root),
            "actual_height": actual_height(root),
            "valid_bst": is_valid_bst_structure(root),
            "valid_avl": is_valid_avl_structure(root),
            "nodes_created_across_64_insertions": created,
            "left_rotations": rotations["left"],
            "right_rotations": rotations["right"],
            "total_rotations": rotations["left"] + rotations["right"],
        }
    safe("avl_insert", avl_probe)

    return output


def complexity_observations(module):
    output = {}

    balanced = []
    for n in (255, 511, 1023, 2047, 4095):
        ledger = Ledger()
        root = build_balanced(range(n), ledger)
        module.bst_contains(root, n + 100)
        balanced.append((n, ledger.counts["key_read"]))

    skewed = []
    for n in (64, 128, 256, 512):
        ledger = Ledger()
        root = build_right_skewed(range(n), ledger)
        module.bst_contains(root, n + 100)
        skewed.append((n, ledger.counts["key_read"]))

    output["bst_contains_balanced"] = {
        "measurements": balanced,
        "max_key_reads": max(cost for _, cost in balanced),
    }
    skewed_exp = adjacent_exponents(skewed)
    output["bst_contains_skewed"] = {
        "measurements": skewed,
        "doubling_exponents": skewed_exp,
        "median_exponent": median(skewed_exp),
    }

    allocations = []
    heights = []
    for n in (16, 32, 64, 128):
        ledger = Ledger()

        class BoundNode(TrackedNode):
            def __init__(self, key, left=None, right=None, height=1):
                super().__init__(key, left, right, height, ledger=ledger)

        original_node = module.Node
        original_left = module.rotate_left
        original_right = module.rotate_right
        module.Node = BoundNode
        module.rotate_left = lambda node, f=original_left: f(node)
        module.rotate_right = lambda node, f=original_right: f(node)

        try:
            root = None
            for key in range(n):
                root = module.avl_insert(root, key)
        finally:
            module.Node = original_node
            module.rotate_left = original_left
            module.rotate_right = original_right

        allocations.append((n, max(1, ledger.counts["node_created"])))
        heights.append((n, actual_height(root)))

    allocation_exponents = adjacent_exponents(allocations)
    output["avl_cumulative_node_allocations"] = {
        "measurements": allocations,
        "doubling_exponents": allocation_exponents,
        "median_exponent": median(allocation_exponents),
    }
    output["avl_final_height"] = {
        "measurements": heights,
    }

    return output


def memory_observations(module):
    output = {}

    large_root = build_balanced_normal(module, range(2047))

    for name, function, args in [
        ("bst_contains", module.bst_contains, (large_root, 9999)),
        ("is_valid_bst", module.is_valid_bst, (large_root,)),
    ]:
        try:
            _, peak = peak_allocated_bytes(function, *args)
            output[name] = {"peak_bytes": peak}
        except Exception as exc:
            output[name] = {"error": f"{type(exc).__name__}: {exc}"}

    return output


def evaluate(path):
    module = load_module(path)
    functional = functional_checks(module)
    static = static_observations(path)
    methods = methodological_findings(static)
    runtime = runtime_observations(module)
    complexity = complexity_observations(module)
    memory = memory_observations(module)

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
    }


def to_markdown(data):
    lines = [
        "# List 03 implementation report",
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

    lines += ["", "## Runtime tree observations", ""]
    for name, item in data["runtime"].items():
        lines += [f"### {name}", ""]
        for key, value in item.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    lines += ["## Complexity and shape evidence", ""]
    for name, item in data["complexity"].items():
        lines += [f"### {name}", ""]
        for key, value in item.items():
            if key == "doubling_exponents":
                value = [round(x, 3) for x in value]
            elif key == "median_exponent" and value is not None:
                value = round(value, 3)
            lines.append(f"- {key}: {value}")
        lines.append("")

    lines += ["## Memory diagnostics", ""]
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
