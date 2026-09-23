# Evidence snapshot — functionally correct but inefficient submission

Source profile: demo/list_01/sample_submissions/functionally_correct_but_inefficient.py

## Summary

- functional checks: 23 / 23
- methodological findings: 7

This profile is intentionally important: an output-only grader would accept every functional check.

## Structural findings

- clamp: no explicit selection; built-in min/max shortcut detected
- min_max: no explicit loop; built-in min/max shortcut detected
- reverse_in_place: no explicit loop; slicing detected
- analyse_scores: built-in sum/min/max shortcuts detected

## Runtime evidence

### first_index

- result: 1
- reads: 6
- visited indices: [0, 1, 2, 3, 4, 5]
- early termination: no

The correct answer was found at index 1, but the implementation scanned the entire sequence.

### min_max

- reads for 100 elements: 200
- sequence iterations: 2
- comparisons: 198

The implementation remains O(n), but performs two full passes rather than the intended single pass.

### analyse_scores

- reads for 6 elements: 30
- sequence iterations: 5

Again, the asymptotic class remains linear, but the implementation performs avoidable repeated passes.

Interpretation: correct outputs do not imply that the intended algorithmic method was implemented.
