# Evidence snapshot — functionally correct but inefficient submission

## Summary

- functional checks: 31 / 31
- methodological findings: 5

Every functional check passes. The deeper grader still exposes several algorithmic mismatches.

## Binary search implemented as linear search

For a sorted sequence of 4,096 elements:

- strong implementation: 13 reads
- this implementation: 4,096 reads

The returned answer is correct, but the access pattern is linear rather than logarithmic.

## Insertion sort replaced by a library sort

AST evidence identifies:

- no insertion-sort loop structure;
- call to sorted;
- slicing.

The output is correct and stable, but the requested algorithm was not implemented.

## Selection-sort task implemented with bubble sort

For 64 reverse-ordered elements:

- comparisons: 2,016
- writes: 4,032
- canonical strong implementation writes: 64

The asymptotic comparison count alone does not distinguish the two algorithms. Data-movement instrumentation does.

## Linear merge replaced by quadratic re-sorting

Measured comparison-growth exponent for merge_sorted:

- 1.984

The requested merge operation should be linear in the combined input size.

## Merge sort replaced by a quadratic sorting method

- functional checks: pass
- recursive structure: not detected
- measured comparison-growth exponent: 1.938

## Quicksort replaced by insertion sort

- functional checks: pass
- recursive quicksort structure: not detected
- measured comparison-growth exponent: 1.981 on deterministic shuffled inputs

This profile is the clearest demonstration that output correctness and algorithmic implementation are independent dimensions.
