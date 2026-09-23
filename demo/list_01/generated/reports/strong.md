# List 01 implementation report

Solution: demo/list_01/sample_submissions/strong.py

## Summary

- Functional checks: 23/23
- Methodological findings: 0

## Functional correctness

| Function | Passed | Total |
|---|---:|---:|
| clamp | 4 | 4 |
| first_index | 4 | 4 |
| min_max | 4 | 4 |
| reverse_in_place | 3 | 3 |
| first_negative_running_sum | 4 | 4 |
| analyse_scores | 4 | 4 |

## Methodological findings

- clamp: none
- first_index: none
- min_max: none
- reverse_in_place: none
- first_negative_running_sum: none
- analyse_scores: none

## Runtime observations

### first_index

- ok: True
- result: 1
- reads: 2
- writes: 0
- iterations: 0
- visited_indices: [0, 1]
- early_exit: True

### min_max

- ok: True
- result: (0, 99)
- reads: 101
- writes: 0
- iterations: 0
- slices: 0
- comparisons: 198

### reverse_in_place

- ok: True
- result: None
- correct_final_state: True
- reads: 20
- writes: 20
- slice_reads: 0
- slice_writes: 0

### first_negative_running_sum

- ok: True
- result: 0
- reads: 1
- iterations: 0
- slices: 0
- early_exit: True

### analyse_scores

- ok: True
- result: (53.333333333333336, 0, 100, 4)
- reads: 6
- writes: 0
- iterations: 0
- slices: 0

## Empirical growth

### first_index

- measurements: [(64, 64), (128, 128), (256, 256), (512, 512)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

### min_max

- measurements: [(64, 65), (128, 129), (256, 257), (512, 513)]
- doubling exponents: [0.989, 0.994, 0.997]
- median exponent: 0.994

### first_negative_running_sum

- measurements: [(64, 64), (128, 128), (256, 256), (512, 512)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

### analyse_scores

- measurements: [(64, 64), (128, 128), (256, 256), (512, 512)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

## Control-flow trace

- result: (2, 9)
- line_counts: {20: 1, 22: 1, 23: 1, 24: 4, 25: 3, 26: 3, 27: 1, 28: 3, 29: 1, 30: 1}
- call_counts: {'min_max': 1}
- stdout: 
- stderr: 

## Memory diagnostics

- min_max: {'current_bytes': 0, 'peak_bytes': 148}
- first_negative_running_sum: {'current_bytes': 72, 'peak_bytes': 220}
- analyse_scores: {'current_bytes': 144, 'peak_bytes': 240}
