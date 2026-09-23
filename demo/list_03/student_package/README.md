# List 03 — Binary Trees, BST and AVL Trees

Implement the functions in `starter.py`.

The `Node` class is part of the provided interface. Do not replace it with a different tree representation.

## Height convention

- empty tree: height `0`;
- leaf: height `1`.

The `height` field stored in AVL nodes follows the same convention.

## Task 1 — inorder_keys

~~~python
def inorder_keys(root) -> list[int]:
    ...
~~~

Return all keys using recursive in-order traversal.

Requirements:

- visit left subtree, node, right subtree;
- `O(n)` time;
- `O(h)` recursion stack, excluding the returned list;
- no sorting shortcut.

## Task 2 — bst_contains

~~~python
def bst_contains(root, target) -> bool:
    ...
~~~

Search a valid BST.

Requirements:

- follow only one search path;
- return as soon as the answer is known;
- `O(h)` time;
- `O(1)` auxiliary space for an iterative solution, or `O(h)` for recursion;
- do not materialise a traversal and search it.

## Task 3 — bst_insert

~~~python
def bst_insert(root, key):
    ...
~~~

Insert `key` into the BST and return the root.

Requirements:

- preserve the existing tree except for the single new link;
- ignore duplicate keys;
- allocate at most one new node;
- `O(h)` time;
- do not rebuild or sort the whole tree.

## Task 4 — bst_height

~~~python
def bst_height(root) -> int:
    ...
~~~

Return the actual tree height using recursion.

Requirements:

- empty tree -> 0;
- leaf -> 1;
- visit every node once;
- `O(n)` time;
- `O(h)` recursion stack.

## Task 5 — is_valid_bst

~~~python
def is_valid_bst(root) -> bool:
    ...
~~~

Return whether the complete tree satisfies the strict BST invariant.

Requirements:

- duplicates are invalid;
- validate **global bounds**, not only parent/child relationships;
- `O(n)` time;
- `O(h)` recursion stack;
- do not materialise the whole in-order sequence.

## Task 6 — rotate_left

Implement the standard AVL left rotation.

Requirements:

- preserve BST order;
- modify only the local links involved in the rotation;
- update stored heights correctly;
- return the new subtree root.

## Task 7 — rotate_right

Implement the standard AVL right rotation with the same requirements.

## Task 8 — avl_insert

~~~python
def avl_insert(root, key):
    ...
~~~

Insert a key into an AVL tree.

Requirements:

- recursive BST insertion;
- ignore duplicates;
- update stored heights on the return path;
- restore balance with LL, RR, LR and RL rotations;
- preserve BST order;
- `O(log n)` time when the AVL invariant is maintained;
- do not rebuild the entire tree.

## Design note

For each task, complete `DESIGN_TEMPLATE.md`.

For BST/AVL tasks explicitly discuss how complexity depends on tree height `h`, not only node count `n`.
