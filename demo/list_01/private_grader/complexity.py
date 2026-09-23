"""Helpers for empirical operation-growth experiments."""

from __future__ import annotations

import math
import time
import tracemalloc


def empirical_exponent(cost_n: float, cost_2n: float) -> float:
    """Estimate p in C(n) ~= n**p from measurements at n and 2n."""
    if cost_n <= 0 or cost_2n <= 0:
        raise ValueError("costs must be positive")
    return math.log(cost_2n / cost_n, 2)


def timed_call(function, *args, **kwargs):
    """Diagnostic wall-clock timing; do not use as the primary grade."""
    start = time.perf_counter_ns()
    result = function(*args, **kwargs)
    return result, time.perf_counter_ns() - start


def peak_allocated_bytes(function, *args, **kwargs):
    """Diagnostic peak allocation measured by tracemalloc."""
    tracemalloc.start()
    try:
        result = function(*args, **kwargs)
        _, peak = tracemalloc.get_traced_memory()
        return result, peak
    finally:
        tracemalloc.stop()
