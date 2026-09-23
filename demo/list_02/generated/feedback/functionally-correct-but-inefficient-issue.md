# List 02 — automated technical feedback

Analysed revision: `9e0b0f7a95deaeb7cc845fe8cd653ecd516efdf7`
Demonstration profile: **functionally correct but inefficient**

## Summary

- functional checks: **31/31**
- methodological findings: **5**

## Correctness

All functional checks in this demonstration pass.

## Implementation observations

- `insertion_sort_in_place`: loop nesting too shallow for requested method: 0; banned shortcut calls: sorted; slicing detected.
- `merge_sort`: required recursive structure not detected.
- `quick_sort_in_place`: required recursive structure not detected.

## Binary-search access pattern

The large absent-target probe performed **4096** reads.

The task expects interval halving. Keep low/high bounds and inspect only the midpoint of the current search interval.

## Selection-sort data movement

The probe observed **4032** writes for 64 elements.

Canonical selection sort searches for the minimum first and performs at most one swap per outer iteration.

## Merge complexity signal

For `merge_sorted`, the measured comparison-growth exponent is approximately **1.984**.

The merge step should be linear in the combined input size. Advance one of the two input cursors after each comparison instead of re-sorting the combined data.

## Merge-sort complexity signal

The measured comparison-growth exponent is approximately **1.938**.

This is substantially above the expected n log n pattern. Use recursive splitting and linear merging rather than a quadratic sorting method.

## Quicksort complexity signal

The measured comparison-growth exponent is approximately **1.981** on deterministic shuffled inputs.

The implementation is sorting correctly, but its measured growth is closer to a quadratic method than to quicksort's expected average behaviour.

---

This feedback is generated from versioned technical evidence. It is intended to support revision of the implementation and is not a standalone final grade.
