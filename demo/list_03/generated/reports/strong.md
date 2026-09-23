# List 03 implementation report

Solution: `demo/list_03/sample_submissions/strong.py`

## Summary

- functional checks: **34/34**
- methodological findings: **0**

## Functional correctness

| Function | Passed | Total |
|---|---:|---:|
| inorder_keys | 4 | 4 |
| bst_contains | 5 | 5 |
| bst_insert | 5 | 5 |
| bst_height | 4 | 4 |
| is_valid_bst | 5 | 5 |
| rotate_left | 2 | 2 |
| rotate_right | 2 | 2 |
| avl_insert | 7 | 7 |

## Methodological findings

- `inorder_keys`: none
- `bst_contains`: none
- `bst_insert`: none
- `bst_height`: none
- `is_valid_bst`: none
- `rotate_left`: none
- `rotate_right`: none
- `avl_insert`: none

## Runtime tree observations

### inorder_keys

- ok: True
- correct: True
- key_reads: 127
- child_reads: 254
- node_count: 127

### bst_contains

- ok: True
- balanced_result: False
- balanced_key_reads: 24
- balanced_comparisons: 24
- balanced_visited_count: 24
- balanced_visited_sample: [2047, 2047, 3071, 3071, 3583, 3583, 3839, 3839, 3967, 3967, 4031, 4031, 4063, 4063, 4079, 4079, 4087, 4087, 4091, 4091]
- skewed_result: False
- skewed_key_reads: 1024
- skewed_visited_count: 1024

### bst_insert

- ok: True
- valid_after_insert: True
- node_created_for_new_key: 1
- link_writes_for_new_key: 1
- key_reads_for_new_key: 16
- node_created_for_duplicate: 0
- link_writes_for_duplicate: 0

### bst_height

- ok: True
- result: 7
- expected: 7
- child_reads: 254

### is_valid_bst

- ok: True
- deep_invalid_result: False
- key_reads: 6
- child_reads: 3

### rotate_left

- ok: True
- new_root: 20
- valid_bst: True
- link_writes: 2
- height_writes: 2
- actual_height: 2

### avl_insert

- ok: True
- node_count: 64
- actual_height: 7
- valid_bst: True
- valid_avl: True
- nodes_created_across_64_insertions: 64
- left_rotations: 57
- right_rotations: 0
- total_rotations: 57

## Complexity and shape evidence

### bst_contains_balanced

- measurements: [(255, 16), (511, 18), (1023, 20), (2047, 22), (4095, 24)]
- max_key_reads: 24

### bst_contains_skewed

- measurements: [(64, 128), (128, 256), (256, 512), (512, 1024)]
- doubling_exponents: [1.0, 1.0, 1.0]
- median_exponent: 1.0

### avl_cumulative_node_allocations

- measurements: [(16, 16), (32, 32), (64, 64), (128, 128)]
- doubling_exponents: [1.0, 1.0, 1.0]
- median_exponent: 1.0

### avl_final_height

- measurements: [(16, 5), (32, 6), (64, 7), (128, 8)]

## Memory diagnostics

- bst_contains: {'peak_bytes': 0}
- is_valid_bst: {'peak_bytes': 200}
