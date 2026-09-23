"""Rich runtime instrumentation for the algorithm laboratory."""

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


class TrackedNumber:
    """Number-like object that records comparisons and arithmetic."""

    def __init__(self, value: int | float, ledger: Ledger):
        self.value = value
        self.ledger = ledger

    @staticmethod
    def raw(other):
        return other.value if isinstance(other, TrackedNumber) else other

    def _cmp(self, op, other, fn):
        other_value = self.raw(other)
        result = fn(self.value, other_value)
        self.ledger.record("comparison", op=op, left=self.value, right=other_value, result=result)
        return result

    def _arith(self, op, other, fn):
        other_value = self.raw(other)
        result = fn(self.value, other_value)
        self.ledger.record("arithmetic", op=op, left=self.value, right=other_value, result=result)
        return TrackedNumber(result, self.ledger)

    def __lt__(self, other): return self._cmp("<", other, lambda a, b: a < b)
    def __le__(self, other): return self._cmp("<=", other, lambda a, b: a <= b)
    def __gt__(self, other): return self._cmp(">", other, lambda a, b: a > b)
    def __ge__(self, other): return self._cmp(">=", other, lambda a, b: a >= b)
    def __eq__(self, other): return self._cmp("==", other, lambda a, b: a == b)
    def __ne__(self, other): return self._cmp("!=", other, lambda a, b: a != b)

    def __add__(self, other): return self._arith("+", other, lambda a, b: a + b)
    def __sub__(self, other): return self._arith("-", other, lambda a, b: a - b)
    def __mul__(self, other): return self._arith("*", other, lambda a, b: a * b)

    def __radd__(self, other):
        other_value = self.raw(other)
        result = other_value + self.value
        self.ledger.record("arithmetic", op="+", left=other_value, right=self.value, result=result)
        return TrackedNumber(result, self.ledger)

    def __rsub__(self, other):
        other_value = self.raw(other)
        result = other_value - self.value
        self.ledger.record("arithmetic", op="-", left=other_value, right=self.value, result=result)
        return TrackedNumber(result, self.ledger)

    def __truediv__(self, other):
        other_value = self.raw(other)
        result = self.value / other_value
        self.ledger.record("arithmetic", op="/", left=self.value, right=other_value, result=result)
        return result

    def __repr__(self):
        return f"TrackedNumber({self.value!r})"


def unwrap(value):
    if isinstance(value, TrackedNumber):
        return value.value
    if isinstance(value, tuple):
        return tuple(unwrap(item) for item in value)
    if isinstance(value, list):
        return [unwrap(item) for item in value]
    return value


class InstrumentedSequence:
    """List-like object that records reads, writes, iteration and slicing."""

    def __init__(self, values, *, track_numbers: bool = False, ledger: Ledger | None = None):
        self.ledger = ledger or Ledger()
        self._data = [
            TrackedNumber(value, self.ledger) if track_numbers else value
            for value in values
        ]

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

    def snapshot(self):
        return [unwrap(item) for item in self._data]

    def count(self, kind: str) -> int:
        return self.ledger.counts[kind]

    def visited_indices(self) -> list[int]:
        return [
            event["index"]
            for event in self.ledger.events
            if event["kind"] == "read" and "index" in event
        ]
