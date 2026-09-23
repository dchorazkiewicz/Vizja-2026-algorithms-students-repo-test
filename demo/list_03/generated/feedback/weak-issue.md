# List 03 — automated technical feedback

Analysed revision: `901128068b6a6a58b95eb8eec03eebff2d1b1adf`
Demonstration profile: **weak**

## Summary

- functional checks: **14/34**
- methodological findings: **2**

## Correctness issues

- `inorder_keys`: 2/4 checks passed; failing cases: balanced, unbalanced.
- `bst_contains`: 3/5 checks passed; failing cases: left, right.
- `bst_insert`: 4/5 checks passed; failing cases: duplicate-ignored.
- `bst_height`: 0/4 checks passed; failing cases: empty, leaf, balanced-3, left-chain.
- `is_valid_bst`: 4/5 checks passed; failing cases: deep-global-violation.
- `rotate_left`: 0/2 checks passed; failing cases: basic-shape-and-heights, subtree-preserved.
- `rotate_right`: 0/2 checks passed; failing cases: basic-shape-and-heights, subtree-preserved.
- `avl_insert`: 1/7 checks passed; failing cases: LL, RR, LR, RL, long-sequence, duplicate-ignored.

## Implementation observations

- `avl_insert`: recursive AVL insertion not detected; AVL rotation calls not detected.

## BST search correctness

The search contract fails for: **left, right**.

Check the branch direction carefully: when target < node.key, continue in the left subtree; when target > node.key, continue in the right subtree.

## Duplicate handling

Inserting an existing key created **1** new node(s).

Duplicate keys must be ignored without changing the tree.

## Height convention

The balanced probe returned height **6** where **7** is required.

Use the declared convention consistently: empty tree has height 0 and a leaf has height 1.

## Global BST invariant

The validator accepted a tree whose direct parent/child comparisons look valid locally but whose deeper node violates an ancestor bound.

Carry lower and upper bounds through the recursion. Checking only immediate children is not sufficient.

## Rotation maintenance

The rotation probe observed **2** local link writes but **0** stored-height updates.

A structurally correct rotation is not enough for AVL trees: after rewiring the subtree, recompute the stored heights of the demoted node first and the new subtree root second.

## AVL invariant

After inserting 64 ascending keys, the resulting tree has height **64** and fails the AVL invariant.

Update heights on the recursive return path and apply the appropriate LL, RR, LR or RL rotation when the balance factor leaves [-1, 1].

---

This feedback is generated from versioned technical evidence. It is intended to support revision of the implementation and is not a standalone final grade.
