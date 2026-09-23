"""Complexity and memory helpers for List 03."""

from __future__ import annotations

import math
import tracemalloc


def empirical_exponent(cost_n, cost_2n):
    if cost_n <= 0 or cost_2n <= 0:
        raise ValueError("costs must be positive")
    return math.log(cost_2n / cost_n, 2)


def adjacent_exponents(measurements):
    values = []
    for (n1, c1), (n2, c2) in zip(measurements, measurements[1:]):
        if n2 != 2 * n1:
            raise ValueError("adjacent sizes must double")
        values.append(empirical_exponent(c1, c2))
    return values


def median(values):
    if not values:
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def peak_allocated_bytes(function, *args):
    tracemalloc.start()
    try:
        result = function(*args)
        _, peak = tracemalloc.get_traced_memory()
        return result, peak
    finally:
        tracemalloc.stop()
