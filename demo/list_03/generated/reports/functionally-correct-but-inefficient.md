# List 03 implementation report

Solution: `demo/list_03/sample_submissions/functionally_correct_but_inefficient.py`

## Summary

- functional checks: **34/34**
- methodological findings: **6**

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
- `bst_contains`: path traversal structure not detected; full inorder traversal used for BST search
- `bst_insert`: none
- `bst_height`: none
- `is_valid_bst`: required recursive global validation not detected; whole inorder sequence materialised for validation
- `rotate_left`: none
- `rotate_right`: none
- `avl_insert`: AVL rotation calls not detected; whole-tree rebuild/sort strategy detected

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
- balanced_key_reads: 4095
- balanced_comparisons: 4095
- balanced_visited_count: 4095
- balanced_visited_sample: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
- skewed_result: False
- skewed_key_reads: 512
- skewed_visited_count: 512

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
- key_reads: 4
- child_reads: 8

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
- nodes_created_across_64_insertions: 2080
- left_rotations: 0
- right_rotations: 0
- total_rotations: 0

## Complexity and shape evidence

### bst_contains_balanced

- measurements: [(255, 255), (511, 511), (1023, 1023), (2047, 2047), (4095, 4095)]
- max_key_reads: 4095

### bst_contains_skewed

- measurements: [(64, 64), (128, 128), (256, 256), (512, 512)]
- doubling_exponents: [1.0, 1.0, 1.0]
- median_exponent: 1.0

### avl_cumulative_node_allocations

- measurements: [(16, 136), (32, 528), (64, 2080), (128, 8256)]
- doubling_exponents: [1.957, 1.978, 1.989]
- median_exponent: 1.978

### avl_final_height

- measurements: [(16, 5), (32, 6), (64, 7), (128, 8)]

## Memory diagnostics

- bst_contains: {'peak_bytes': 18416}
- is_valid_bst: {'peak_bytes': 18564}
