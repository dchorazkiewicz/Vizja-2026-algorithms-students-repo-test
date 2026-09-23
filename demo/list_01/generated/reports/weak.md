# List 01 implementation report

Solution: demo/list_01/sample_submissions/weak.py

## Summary

- Functional checks: 9/23
- Methodological findings: 7

## Functional correctness

| Function | Passed | Total |
|---|---:|---:|
| clamp | 1 | 4 |
| first_index | 2 | 4 |
| min_max | 0 | 4 |
| reverse_in_place | 0 | 3 |
| first_negative_running_sum | 4 | 4 |
| analyse_scores | 2 | 4 |

## Methodological findings

- clamp: no explicit selection
- first_index: none
- min_max: none
- reverse_in_place: no explicit loop; banned shortcut calls: list, reversed
- first_negative_running_sum: banned shortcut calls: sum; slicing detected
- analyse_scores: no explicit loop; banned shortcut calls: max, min, sum

## Runtime observations

### first_index

- ok: True
- result: 3
- reads: 6
- writes: 0
- iterations: 0
- visited_indices: [0, 1, 2, 3, 4, 5]
- early_exit: False

### min_max

- ok: True
- result: (0, 99)
- reads: 100
- writes: 0
- iterations: 1
- slices: 0
- comparisons: 200

### reverse_in_place

- ok: True
- result: [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
- correct_final_state: False
- reads: 20
- writes: 0
- slice_reads: 0
- slice_writes: 0

### first_negative_running_sum

- ok: True
- result: 0
- reads: 1
- iterations: 0
- slices: 1
- early_exit: True

### analyse_scores

- ok: True
- result: (53.333333333333336, 0, 100, 4)
- reads: 24
- writes: 0
- iterations: 4
- slices: 0

## Empirical growth

### first_index

- measurements: [(64, 64), (128, 128), (256, 256), (512, 512)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

### min_max

- measurements: [(64, 64), (128, 128), (256, 256), (512, 512)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

### first_negative_running_sum

- measurements: [(64, 2080), (128, 8256), (256, 32896), (512, 131328)]
- doubling exponents: [1.989, 1.994, 1.997]
- median exponent: 1.994

### analyse_scores

- measurements: [(64, 256), (128, 512), (256, 1024), (512, 2048)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

## Control-flow trace

- result: (0, 9)
- line_counts: {17: 1, 18: 1, 19: 5, 20: 4, 22: 4, 23: 2, 24: 1}
- call_counts: {'min_max': 1}
- stdout: 
- stderr: 

## Memory diagnostics

- min_max: {'current_bytes': 0, 'peak_bytes': 48}
- first_negative_running_sum: {'current_bytes': 72, 'peak_bytes': 80192}
- analyse_scores: {'current_bytes': 144, 'peak_bytes': 85240}
