"""Runtime instrumentation for List 02 searching and sorting algorithms."""

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


class TrackedItem:
    """Comparable value carrying a stable identity tag."""

    def __init__(self, key, tag, ledger: Ledger):
        self.key = key
        self.tag = tag
        self.ledger = ledger

    @staticmethod
    def raw_key(other):
        return other.key if isinstance(other, TrackedItem) else other

    def _compare(self, op, other, fn):
        other_key = self.raw_key(other)
        result = fn(self.key, other_key)
        self.ledger.record(
            "comparison",
            op=op,
            left_key=self.key,
            left_tag=self.tag,
            right_key=other_key,
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
        return f"TrackedItem(key={self.key!r}, tag={self.tag!r})"


def unwrap(value):
    if isinstance(value, TrackedItem):
        return value.key
    if isinstance(value, list):
        return [unwrap(item) for item in value]
    if isinstance(value, tuple):
        return tuple(unwrap(item) for item in value)
    return value


class InstrumentedSequence:
    """Mutable sequence recording reads, writes, slicing and iteration."""

    def __init__(
        self,
        values,
        *,
        track_items: bool = False,
        ledger: Ledger | None = None,
        tag_offset: int = 0,
    ):
        self.ledger = ledger or Ledger()
        self._data = []
        for index, value in enumerate(values):
            if isinstance(value, TrackedItem):
                item = value
            elif track_items:
                item = TrackedItem(value, tag_offset + index, self.ledger)
            else:
                item = value
            self._data.append(item)

    def __len__(self):
        self.ledger.record("len", value=len(self._data))
        return len(self._data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            result = self._data[key]
            self.ledger.record(
                "slice_read",
                start=key.start,
                stop=key.stop,
                step=key.step,
                elements=len(result),
            )
            self.ledger.counts["read"] += len(result)
            return result

        value = self._data[key]
        self.ledger.record("read", index=key, value=unwrap(value))
        return value

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            replacement = list(value)
            self.ledger.record(
                "slice_write",
                start=key.start,
                stop=key.stop,
                step=key.step,
                elements=len(replacement),
            )
            self.ledger.counts["write"] += len(replacement)
            self._data[key] = replacement
            return

        self.ledger.record("write", index=key, value=unwrap(value))
        self._data[key] = value

    def __iter__(self):
        self.ledger.record("iteration_start")
        for index, value in enumerate(self._data):
            self.ledger.record("read", index=index, value=unwrap(value))
            yield value

    def sort(self, *args, **kwargs):
        """Allow library sort so the grader can observe the forbidden shortcut.

        Instrumentation should observe student behaviour rather than crashing
        before the AST/runtime evidence can be recorded.
        """
        self.ledger.record("library_sort")
        self._data.sort(*args, **kwargs)

    def snapshot(self):
        return [unwrap(item) for item in self._data]

    def tagged_snapshot(self):
        result = []
        for item in self._data:
            if isinstance(item, TrackedItem):
                result.append((item.key, item.tag))
            else:
                result.append((item, None))
        return result

    def count(self, kind: str) -> int:
        return self.ledger.counts[kind]

    def visited_indices(self) -> list[int]:
        return [
            event["index"]
            for event in self.ledger.events
            if event["kind"] == "read" and "index" in event
        ]


def tagged_output(values):
    result = []
    for item in values:
        if isinstance(item, TrackedItem):
            result.append((item.key, item.tag))
        else:
            result.append((item, None))
    return result


def is_stable_tagged(values) -> bool:
    by_key: dict[Any, list[Any]] = {}
    for key, tag in values:
        by_key.setdefault(key, []).append(tag)

    for tags in by_key.values():
        if tags != sorted(tags):
            return False
    return True
