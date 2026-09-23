# Evidence snapshot — functionally correct but inefficient tree submission

## Summary

- functional checks: 34 / 34
- methodological findings: 6

All required results are correct. The grader still exposes expensive implementation strategies.

## BST search by full traversal

On a balanced BST with 4,095 nodes:

- strong path search: 24 key reads
- this implementation: 4,095 key reads

The function builds the complete in-order sequence and then searches it.

## BST validation by materialising all keys

The validator is functionally correct, including deep global violations, but constructs the full in-order key list before checking adjacent values.

Memory diagnostic on a 2,047-node tree:

- bst_contains peak allocation: about 18 KB
- is_valid_bst peak allocation: about 18 KB

The strong path/bounds implementations allocate essentially constant or recursion-stack-only auxiliary storage in the same diagnostic.

## AVL rebuilt after every insertion

For 64 ascending insertions:

- final height: 7
- valid AVL: yes
- total rotations: 0
- nodes created: 2,080

The strong implementation creates exactly 64 nodes over the same 64 insertions.

Cumulative allocations:

| insert count | nodes created |
|---:|---:|
| 16 | 136 |
| 32 | 528 |
| 64 | 2,080 |
| 128 | 8,256 |

Empirical allocation-growth exponent: 1.978.

This profile demonstrates why a valid final tree does not prove an efficient AVL update algorithm.
