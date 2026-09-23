# Evidence snapshot — weak tree submission

## Summary

- functional checks: 14 / 34
- methodological findings: 2

## Traversal order

The implementation labelled `inorder_keys` returns pre-order for non-trivial trees.

The grader distinguishes the required traversal order rather than checking only that all keys appear.

## BST search branch direction

The search passes root/absent cases but fails both left- and right-subtree hits.

The generated feedback points directly to the branch rule:

~~~text
target < node.key → left
target > node.key → right
~~~

## Duplicate insertion

A duplicate-key insertion creates:

- 1 new node
- 1 child-link write

The task requires no structural change.

## Height convention

Balanced seven-level probe expected:

- height: 7

Observed:

- height: 6

The implementation uses the edge-count convention while the assignment explicitly defines empty = 0 and leaf = 1.

## Global BST invariant

A deep ancestor-bound violation is incorrectly accepted because the implementation checks only immediate children.

## Rotations

The left-rotation probe performs:

- link writes: 2
- stored-height writes: 0

The local links form a BST, but AVL metadata is stale.

## AVL insertion

For 64 ascending keys:

- final height: 64
- valid BST: yes
- valid AVL: no
- rotations: 0

The result is an ordinary degenerate BST rather than a balanced AVL tree.
