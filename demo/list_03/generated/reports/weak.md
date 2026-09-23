# List 03 implementation report

Solution: `demo/list_03/sample_submissions/weak.py`

## Summary

- functional checks: **14/34**
- methodological findings: **2**

## Functional correctness

| Function | Passed | Total |
|---|---:|---:|
| inorder_keys | 2 | 4 |
| bst_contains | 3 | 5 |
| bst_insert | 4 | 5 |
| bst_height | 0 | 4 |
| is_valid_bst | 4 | 5 |
| rotate_left | 0 | 2 |
| rotate_right | 0 | 2 |
| avl_insert | 1 | 7 |

## Methodological findings

- `inorder_keys`: none
- `bst_contains`: none
- `bst_insert`: none
- `bst_height`: none
- `is_valid_bst`: none
- `rotate_left`: none
- `rotate_right`: none
- `avl_insert`: recursive AVL insertion not detected; AVL rotation calls not detected

## Runtime tree observations

### inorder_keys

- ok: True
- correct: False
- key_reads: 127
- child_reads: 254
- node_count: 127

### bst_contains

- ok: True
- balanced_result: False
- balanced_key_reads: 24
- balanced_comparisons: 24
- balanced_visited_count: 24
- balanced_visited_sample: [2047, 2047, 1023, 1023, 511, 511, 255, 255, 127, 127, 63, 63, 31, 31, 15, 15, 7, 7, 3, 3]
- skewed_result: False
- skewed_key_reads: 2
- skewed_visited_count: 2

### bst_insert

- ok: True
- valid_after_insert: False
- node_created_for_new_key: 1
- link_writes_for_new_key: 1
- key_reads_for_new_key: 8
- node_created_for_duplicate: 1
- link_writes_for_duplicate: 1

### bst_height

- ok: True
- result: 6
- expected: 7
- child_reads: 254

### is_valid_bst

- ok: True
- deep_invalid_result: True
- key_reads: 6
- child_reads: 19

### rotate_left

- ok: True
- new_root: 20
- valid_bst: True
- link_writes: 2
- height_writes: 0
- actual_height: 2

### avl_insert

- ok: True
- node_count: 64
- actual_height: 64
- valid_bst: True
- valid_avl: False
- nodes_created_across_64_insertions: 64
- left_rotations: 0
- right_rotations: 0
- total_rotations: 0

## Complexity and shape evidence

### bst_contains_balanced

- measurements: [(255, 16), (511, 18), (1023, 20), (2047, 22), (4095, 24)]
- max_key_reads: 24

### bst_contains_skewed

- measurements: [(64, 2), (128, 2), (256, 2), (512, 2)]
- doubling_exponents: [0.0, 0.0, 0.0]
- median_exponent: 0.0

### avl_cumulative_node_allocations

- measurements: [(16, 16), (32, 32), (64, 64), (128, 128)]
- doubling_exponents: [1.0, 1.0, 1.0]
- median_exponent: 1.0

### avl_final_height

- measurements: [(16, 16), (32, 32), (64, 64), (128, 128)]

## Memory diagnostics

- bst_contains: {'peak_bytes': 0}
- is_valid_bst: {'peak_bytes': 0}
