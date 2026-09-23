"""Tree-aware runtime instrumentation for List 03."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Ledger:
    counts: Counter = field(default_factory=Counter)
    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, kind: str, **payload: Any) -> None:
        self.counts[kind] += 1
        self.events.append({"kind": kind, **payload})

    def reset(self) -> None:
        self.counts.clear()
        self.events.clear()


class TrackedKey:
    def __init__(self, value, ledger: Ledger):
        self.value = value
        self.ledger = ledger

    @staticmethod
    def raw(other):
        return other.value if isinstance(other, TrackedKey) else other

    def _compare(self, op, other, fn):
        other_value = self.raw(other)
        result = fn(self.value, other_value)
        self.ledger.record(
            "comparison",
            op=op,
            left=self.value,
            right=other_value,
            result=result,
        )
        return result

    def __lt__(self, other): return self._compare("<", other, lambda a, b: a < b)
    def __le__(self, other): return self._compare("<=", other, lambda a, b: a <= b)
    def __gt__(self, other): return self._compare(">", other, lambda a, b: a > b)
    def __ge__(self, other): return self._compare(">=", other, lambda a, b: a >= b)
    def __eq__(self, other): return self._compare("==", other, lambda a, b: a == b)
    def __ne__(self, other): return self._compare("!=", other, lambda a, b: a != b)

    def __repr__(self):
        return f"TrackedKey({self.value!r})"


def raw_key(value):
    return value.value if isinstance(value, TrackedKey) else value


def unwrap(value):
    if isinstance(value, TrackedKey):
        return value.value
    if isinstance(value, list):
        return [unwrap(item) for item in value]
    if isinstance(value, tuple):
        return tuple(unwrap(item) for item in value)
    return value


class TrackedNode:
    def __init__(self, key, left=None, right=None, height=1, *, ledger: Ledger | None = None):
        if ledger is None:
            raise ValueError("TrackedNode requires a ledger")
        self.ledger = ledger
        self._key = raw_key(key)
        self._left = left
        self._right = right
        self._height = height
        self.ledger.record("node_created", key=self._key)

    @property
    def key(self):
        self.ledger.record("key_read", key=self._key)
        return TrackedKey(self._key, self.ledger)

    @key.setter
    def key(self, value):
        self.ledger.record("key_write", old=self._key, new=raw_key(value))
        self._key = raw_key(value)

    @property
    def left(self):
        self.ledger.record("left_read", key=self._key)
        return self._left

    @left.setter
    def left(self, value):
        self.ledger.record(
            "left_write",
            key=self._key,
            child=None if value is None else node_raw_key(value),
        )
        self._left = value

    @property
    def right(self):
        self.ledger.record("right_read", key=self._key)
        return self._right

    @right.setter
    def right(self, value):
        self.ledger.record(
            "right_write",
            key=self._key,
            child=None if value is None else node_raw_key(value),
        )
        self._right = value

    @property
    def height(self):
        self.ledger.record("height_read", key=self._key, value=self._height)
        return self._height

    @height.setter
    def height(self, value):
        self.ledger.record("height_write", key=self._key, value=value)
        self._height = value


def node_raw_key(node):
    if isinstance(node, TrackedNode):
        return node._key
    return raw_key(node.key)


def build_balanced(keys, ledger: Ledger):
    keys = list(keys)

    def build(low, high):
        if low >= high:
            return None
        middle = (low + high) // 2
        node = TrackedNode(keys[middle], ledger=ledger)
        node._left = build(low, middle)
        node._right = build(middle + 1, high)
        node._height = 1 + max(
            0 if node._left is None else node._left._height,
            0 if node._right is None else node._right._height,
        )
        return node

    root = build(0, len(keys))
    ledger.reset()
    return root


def build_right_skewed(keys, ledger: Ledger):
    root = None
    for key in reversed(list(keys)):
        node = TrackedNode(key, right=root, ledger=ledger)
        node._height = 1 + (0 if root is None else root._height)
        root = node
    ledger.reset()
    return root


def visited_keys(ledger: Ledger):
    return [
        event["key"]
        for event in ledger.events
        if event["kind"] == "key_read"
    ]


def child_reads(ledger: Ledger) -> int:
    return ledger.counts["left_read"] + ledger.counts["right_read"]


def link_writes(ledger: Ledger) -> int:
    return ledger.counts["left_write"] + ledger.counts["right_write"]


def generic_key(node):
    if isinstance(node, TrackedNode):
        return node._key
    return raw_key(node.key)


def generic_left(node):
    return node._left if isinstance(node, TrackedNode) else node.left


def generic_right(node):
    return node._right if isinstance(node, TrackedNode) else node.right


def generic_height_field(node):
    return node._height if isinstance(node, TrackedNode) else node.height


def inorder_plain(root):
    result = []

    def visit(node):
        if node is None:
            return
        visit(generic_left(node))
        result.append(generic_key(node))
        visit(generic_right(node))

    visit(root)
    return result


def actual_height(root):
    if root is None:
        return 0
    return 1 + max(actual_height(generic_left(root)), actual_height(generic_right(root)))


def count_nodes(root):
    if root is None:
        return 0
    return 1 + count_nodes(generic_left(root)) + count_nodes(generic_right(root))


def is_valid_bst_structure(root):
    def valid(node, lower, upper):
        if node is None:
            return True
        key = generic_key(node)
        if lower is not None and key <= lower:
            return False
        if upper is not None and key >= upper:
            return False
        return (
            valid(generic_left(node), lower, key)
            and valid(generic_right(node), key, upper)
        )

    return valid(root, None, None)


def is_valid_avl_structure(root):
    def validate(node):
        if node is None:
            return True, 0, None, None

        left_ok, left_height, left_min, left_max = validate(generic_left(node))
        right_ok, right_height, right_min, right_max = validate(generic_right(node))
        key = generic_key(node)

        bst_ok = (
            (left_max is None or left_max < key)
            and (right_min is None or key < right_min)
        )
        expected_height = 1 + max(left_height, right_height)
        stored_ok = generic_height_field(node) == expected_height
        balance_ok = abs(left_height - right_height) <= 1

        minimum = left_min if left_min is not None else key
        maximum = right_max if right_max is not None else key
        return (
            left_ok and right_ok and bst_ok and stored_ok and balance_ok,
            expected_height,
            minimum,
            maximum,
        )

    return validate(root)[0]
