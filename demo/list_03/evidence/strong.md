# Evidence snapshot — strong tree submission

## Summary

- functional checks: 34 / 34
- methodological findings: 0

## In-order traversal

For a balanced tree with 127 nodes:

- key reads: 127
- child-link reads: 254
- returned order: correct

The traversal touches each node once and each child reference once per side.

## BST search depends on tree height

Balanced tree with 4,095 nodes:

- key reads: 24
- comparisons: 24

Degenerate right chain with 512 nodes:

- key reads: 1,024

This is direct runtime evidence for the usual O(h) model.

## BST insertion locality

For one new key:

- nodes created: 1
- child-link writes: 1

For a duplicate key:

- nodes created: 0
- child-link writes: 0

## Global BST validation

A deliberately subtle tree contains key 12 inside the left subtree of root 10.

The strong validator rejects it even though the immediate parent/child relation 5 < 12 is locally valid.

## AVL insertion

For 64 ascending keys:

- final node count: 64
- final actual height: 7
- valid BST: yes
- valid AVL: yes
- nodes created across all insertions: 64
- left rotations: 57
- right rotations: 0

For 128 ascending keys the final height is 8.

Cumulative node-allocation growth exponent: 1.000.
