# Algorithm design template — List 03

## Contract

State the accepted input structure and required result.

## Structural invariant

What tree property must remain true?

For BST tasks, distinguish local parent/child order from the global BST invariant.

## State meaning

What does the current node or recursive call represent?

## Termination

Why does the traversal or recursion terminate?

## Visited nodes

Which nodes may be visited in the best and worst cases?

## Tree shape

How does a balanced tree differ from a degenerate tree for this algorithm?

## Mutation

Which child links or stored heights may change?

## Complexity

Give the cost in terms of tree height `h` and, where useful, node count `n`.

## AVL rotations

For AVL tasks, explain which imbalance case leads to LL, RR, LR or RL correction.

## Pseudocode

Give a language-independent algorithm description.
