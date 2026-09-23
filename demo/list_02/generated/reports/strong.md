# List 02 implementation report

Solution: `demo/list_02/sample_submissions/strong.py`

## Summary

- functional checks: **31/31**
- methodological findings: **0**

## Functional correctness

| Function | Passed | Total |
|---|---:|---:|
| binary_search | 5 | 5 |
| insertion_sort_in_place | 6 | 6 |
| selection_sort_in_place | 5 | 5 |
| merge_sorted | 5 | 5 |
| merge_sort | 5 | 5 |
| quick_sort_in_place | 5 | 5 |

## Methodological findings

- `binary_search`: none
- `insertion_sort_in_place`: none
- `selection_sort_in_place`: none
- `merge_sorted`: none
- `merge_sort`: none
- `quick_sort_in_place`: none

## Runtime observations

### binary_search

- ok: True
- result: -1
- reads: 13
- writes: 0
- visited_indices: [2047, 3071, 3583, 3839, 3967, 4031, 4063, 4079, 4087, 4091, 4093, 4094, 4095]
- logarithmic_probe: True

### insertion_sort_in_place

- ok: True
- sorted_input_comparisons: 63
- sorted_input_writes: 0
- reverse_input_comparisons: 2016
- reverse_input_writes: 2079
- stable: True
- tagged_result: [(1, 1), (1, 3), (2, 0), (2, 2), (2, 4)]

### selection_sort_in_place

- ok: True
- comparisons: 2016
- expected_canonical_comparisons: 2016
- writes: 64
- canonical_comparison_count: True
- limited_data_movement: True

### merge_sorted

- ok: True
- result: [1, 2, 2, 2, 2, 3, 5, 6]
- comparisons: 7
- reads: 15
- input_writes: 0
- stable: True
- tagged_result: [(1, 0), (2, 1), (2, 2), (2, 4), (2, 5), (3, 6), (5, 3), (6, 7)]

### merge_sort

- ok: True
- result: [1, 1, 2, 2, 3, 4, 4]
- input_writes: 0
- comparisons: 13
- stable: True
- recursive_calls: 22
- max_call_depth: 4

### quick_sort_in_place

- ok: True
- returned: None
- sorted: True
- reads: 1542
- writes: 402
- comparisons: 1036
- slice_reads: 0
- slice_writes: 0
- recursive_calls: 105
- max_call_depth: 11

## Empirical complexity evidence

### binary_search

- measurements: [(128, 8), (256, 9), (512, 10), (1024, 11), (2048, 12), (4096, 13)]
- max_reads: 13

### insertion_reverse

- measurements: [(32, 496), (64, 2016), (128, 8128), (256, 32640)]
- doubling_exponents: [2.023, 2.011, 2.006]
- median_exponent: 2.011

### insertion_sorted

- measurements: [(32, 31), (64, 63), (128, 127), (256, 255)]
- doubling_exponents: [1.023, 1.011, 1.006]
- median_exponent: 1.011

### selection_reverse

- measurements: [(32, 496), (64, 2016), (128, 8128), (256, 32640)]
- doubling_exponents: [2.023, 2.011, 2.006]
- median_exponent: 2.011

### merge_sorted

- measurements: [(128, 127), (256, 255), (512, 511), (1024, 1023)]
- doubling_exponents: [1.006, 1.003, 1.001]
- median_exponent: 1.003

### merge_sort

- measurements: [(64, 304), (128, 740), (256, 1721), (512, 3948)]
- doubling_exponents: [1.283, 1.218, 1.198]
- median_exponent: 1.218
- nlogn_ratios: [(64, 0.7916666666666666), (128, 0.8258928571428571), (256, 0.84033203125), (512, 0.8567708333333334)]

### quick_sort

- measurements: [(64, 479), (128, 1123), (256, 2616), (512, 5960)]
- doubling_exponents: [1.229, 1.22, 1.188]
- median_exponent: 1.22
- nlogn_ratios: [(64, 1.2473958333333333), (128, 1.2533482142857142), (256, 1.27734375), (512, 1.2934027777777777)]

## Memory diagnostics

- insertion_sort_in_place: {'peak_bytes': 116}
- selection_sort_in_place: {'peak_bytes': 128}
- merge_sort: {'peak_bytes': 18080}
- quick_sort_in_place: {'peak_bytes': 944}

## Output capture

- stdout: ``
- stderr: ``
