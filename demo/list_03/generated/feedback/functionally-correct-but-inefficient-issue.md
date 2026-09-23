# List 03 — automated technical feedback

Analysed revision: `c01a4778ec2b2f4d57861599386b166fa2adb9ff`
Demonstration profile: **functionally correct but inefficient**

## Summary

- functional checks: **34/34**
- methodological findings: **6**

## Correctness

All functional checks in this demonstration pass.

## Implementation observations

- `bst_contains`: path traversal structure not detected; full inorder traversal used for BST search.
- `is_valid_bst`: required recursive global validation not detected; whole inorder sequence materialised for validation.
- `avl_insert`: AVL rotation calls not detected; whole-tree rebuild/sort strategy detected.

## BST search path

On a balanced BST with 4,095 nodes, the probe observed **4095** key reads.

A BST search should follow one root-to-leaf path. Avoid materialising a full traversal before searching.

## AVL update cost

Across 64 insertions the probe observed **2080** node allocations and **0** rotation calls.

The final tree is valid, but the implementation is rebuilding large parts of the tree. AVL insertion should allocate one node per new key and repair balance locally with rotations.

## AVL allocation-growth signal

Cumulative node-allocation growth has an empirical exponent of approximately **1.978**.

That is consistent with repeated whole-tree rebuilding rather than local O(log n) AVL updates.

---

This feedback is generated from versioned technical evidence. It is intended to support revision of the implementation and is not a standalone final grade.
