# List 01 — automated technical feedback

Analysed revision: `ac9fa99e73dfc05541f7528cb4f919f940fbc1bf`
Demonstration profile: **weak**

## Summary

- functional checks: **9/23**
- methodological findings: **7**

## Correctness issues

- `clamp`: 1/4 checks passed; failing cases: below, above, negative interval.
- `first_index`: 2/4 checks passed; failing cases: first, duplicate-first.
- `min_max`: 0/4 checks passed; failing cases: single, mixed, all-negative, empty-rejected.
- `reverse_in_place`: 0/3 checks passed; failing cases: empty, odd, even.
- `analyse_scores`: 2/4 checks passed; failing cases: empty-rejected, invalid-score-rejected.

## Implementation observations

- `clamp`: no explicit selection.
- `reverse_in_place`: no explicit loop; banned shortcut calls: list, reversed.
- `first_negative_running_sum`: banned shortcut calls: sum; slicing detected.
- `analyse_scores`: no explicit loop; banned shortcut calls: max, min, sum.

## Early termination

`first_index` returned the correct result in the probe, but inspected **6** elements and visited `[0, 1, 2, 3, 4, 5]`.

The target was available earlier. Return immediately once the first occurrence is known.

## Repeated work in score analysis

`analyse_scores` started **4** sequence iterations and performed **24** reads in the probe.

Accumulate total, minimum, maximum, and passing count in the same traversal.

## Complexity signal

For `first_negative_running_sum`, the measured doubling exponent is approximately **1.994**.

Measured reads: `[[64, 2080], [128, 8256], [256, 32896], [512, 131328]]`.

This is consistent with substantially worse than linear growth. Maintain a running sum instead of recomputing prefixes.

---

This message is generated from automated technical evidence. It is intended as feedback on the implementation, not as a standalone final grade.
