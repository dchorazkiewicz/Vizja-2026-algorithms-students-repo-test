# List 01 implementation report

Solution: demo/list_01/sample_submissions/functionally_correct_but_inefficient.py

## Summary

- Functional checks: 23/23
- Methodological findings: 7

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

- clamp: no explicit selection; banned shortcut calls: max, min
- first_index: none
- min_max: no explicit loop; banned shortcut calls: max, min
- reverse_in_place: no explicit loop; slicing detected
- first_negative_running_sum: none
- analyse_scores: banned shortcut calls: max, min, sum

## Runtime observations

### first_index

- ok: True
- result: 1
- reads: 6
- writes: 0
- iterations: 0
- visited_indices: [0, 1, 2, 3, 4, 5]
- early_exit: False

### min_max

- ok: True
- result: (0, 99)
- reads: 200
- writes: 0
- iterations: 2
- slices: 0
- comparisons: 198

### reverse_in_place

- ok: True
- result: None
- correct_final_state: True
- reads: 20
- writes: 20
- slice_reads: 1
- slice_writes: 1

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
- reads: 30
- writes: 0
- iterations: 5
- slices: 0

## Empirical growth

### first_index

- measurements: [(64, 64), (128, 128), (256, 256), (512, 512)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

### min_max

- measurements: [(64, 128), (128, 256), (256, 512), (512, 1024)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

### first_negative_running_sum

- measurements: [(64, 64), (128, 128), (256, 256), (512, 512)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

### analyse_scores

- measurements: [(64, 320), (128, 640), (256, 1280), (512, 2560)]
- doubling exponents: [1.0, 1.0, 1.0]
- median exponent: 1.0

## Control-flow trace

- result: (2, 9)
- line_counts: {20: 1, 22: 1}
- call_counts: {'min_max': 1}
- stdout: 
- stderr: 

## Memory diagnostics

- min_max: {'current_bytes': 0, 'peak_bytes': 48}
- first_negative_running_sum: {'current_bytes': 72, 'peak_bytes': 220}
- analyse_scores: {'current_bytes': 216, 'peak_bytes': 600}
