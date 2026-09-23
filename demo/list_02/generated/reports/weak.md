# List 02 implementation report

Solution: `demo/list_02/sample_submissions/weak.py`

## Summary

- functional checks: **25/31**
- methodological findings: **5**

## Functional correctness

| Function | Passed | Total |
|---|---:|---:|
| binary_search | 4 | 5 |
| insertion_sort_in_place | 5 | 6 |
| selection_sort_in_place | 3 | 5 |
| merge_sorted | 3 | 5 |
| merge_sort | 5 | 5 |
| quick_sort_in_place | 5 | 5 |

## Methodological findings

- `binary_search`: none
- `insertion_sort_in_place`: none
- `selection_sort_in_place`: none
- `merge_sorted`: none
- `merge_sort`: banned shortcut calls: sorted; required recursive structure not detected
- `quick_sort_in_place`: loop nesting too shallow for requested method: 0; banned shortcut calls: sort; required recursive structure not detected

## Runtime observations

### binary_search

- ok: True
- result: -1
- reads: 26
- writes: 0
- visited_indices: [2047, 2047, 3071, 3071, 3583, 3583, 3839, 3839, 3967, 3967, 4031, 4031, 4063, 4063, 4079, 4079, 4087, 4087, 4091, 4091, 4093, 4093, 4094, 4094, 4095, 4095]
- logarithmic_probe: True

### insertion_sort_in_place

- ok: True
- sorted_input_comparisons: 63
- sorted_input_writes: 63
- reverse_input_comparisons: 2016
- reverse_input_writes: 2079
- stable: False
- tagged_result: [(1, 3), (1, 1), (2, 4), (2, 2), (2, 0)]

### selection_sort_in_place

- ok: True
- comparisons: 1953
- expected_canonical_comparisons: 2016
- writes: 62
- canonical_comparison_count: False
- limited_data_movement: True

### merge_sorted

- ok: True
- result: [1, 2, 2, 3, 5, 6]
- comparisons: 8
- reads: 22
- input_writes: 0
- stable: True
- tagged_result: [(1, 0), (2, 1), (2, 2), (3, 6), (5, 3), (6, 7)]

### merge_sort

- ok: True
- result: [1, 1, 2, 2, 3, 4, 4]
- input_writes: 0
- comparisons: 13
- stable: True
- recursive_calls: 1
- max_call_depth: 1

### quick_sort_in_place

- ok: True
- returned: None
- sorted: True
- reads: 0
- writes: 0
- comparisons: 729
- slice_reads: 0
- slice_writes: 0
- recursive_calls: 1
- max_call_depth: 1

## Empirical complexity evidence

### binary_search

- measurements: [(128, 16), (256, 18), (512, 20), (1024, 22), (2048, 24), (4096, 26)]
- max_reads: 26

### insertion_reverse

- measurements: [(32, 496), (64, 2016), (128, 8128), (256, 32640)]
- doubling_exponents: [2.023, 2.011, 2.006]
- median_exponent: 2.011

### insertion_sorted

- measurements: [(32, 31), (64, 63), (128, 127), (256, 255)]
- doubling_exponents: [1.023, 1.011, 1.006]
- median_exponent: 1.011

### selection_reverse

- measurements: [(32, 465), (64, 1953), (128, 8001), (256, 32385)]
- doubling_exponents: [2.07, 2.034, 2.017]
- median_exponent: 2.034

### merge_sorted

- measurements: [(128, 190), (256, 382), (512, 766), (1024, 1534)]
- doubling_exponents: [1.008, 1.004, 1.002]
- median_exponent: 1.004

### merge_sort

- measurements: [(64, 302), (128, 726), (256, 1712), (512, 3951)]
- doubling_exponents: [1.265, 1.238, 1.207]
- median_exponent: 1.238
- nlogn_ratios: [(64, 0.7864583333333334), (128, 0.8102678571428571), (256, 0.8359375), (512, 0.857421875)]

### quick_sort

- measurements: [(64, 304), (128, 729), (256, 1734), (512, 3945)]
- doubling_exponents: [1.262, 1.25, 1.186]
- median_exponent: 1.25
- nlogn_ratios: [(64, 0.7916666666666666), (128, 0.8136160714285714), (256, 0.8466796875), (512, 0.8561197916666666)]

## Memory diagnostics

- insertion_sort_in_place: {'peak_bytes': 116}
- selection_sort_in_place: {'peak_bytes': 128}
- merge_sort: {'peak_bytes': 8264}
- quick_sort_in_place: {'peak_bytes': 0}

## Output capture

- stdout: ``
- stderr: ``
