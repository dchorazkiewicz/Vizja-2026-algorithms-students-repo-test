# Evidence snapshot — strong submission

## Summary

- functional checks: 31 / 31
- methodological findings: 0

## Binary search

For an absent target in a sorted sequence of 4,096 elements:

- reads: 13
- writes: 0
- visited indices: 2047, 3071, 3583, 3839, 3967, 4031, 4063, 4079, 4087, 4091, 4093, 4094, 4095

Measured reads for increasing sizes:

| n | reads |
|---:|---:|
| 128 | 8 |
| 256 | 9 |
| 512 | 10 |
| 1,024 | 11 |
| 2,048 | 12 |
| 4,096 | 13 |

This is the expected logarithmic access pattern.

## Insertion sort

For 64 elements:

- already sorted input: 63 comparisons, 0 writes
- reverse input: 2,016 comparisons, 2,079 writes
- stability: preserved

Empirical comparison-growth exponent:

- sorted input: 1.011
- reverse input: 2.011

The same implementation visibly exhibits adaptive best-case behaviour and quadratic worst-case behaviour.

## Selection sort

For 64 reverse-ordered elements:

- comparisons: 2,016
- canonical expected comparisons: 2,016
- writes: 64
- limited data movement: yes

The characteristic comparison count is exactly n(n-1)/2.

## Merge

The stable merge probe used:

- 7 comparisons
- 15 input reads
- 0 input writes
- stable ordering of equal keys: preserved

Its measured comparison-growth exponent is 1.003, consistent with linear merging.

## Merge sort and quicksort

Merge sort:

- measured exponent: 1.218
- n log n normalised comparison ratio remains approximately stable
- recursive call depth in the runtime probe: 4

Quicksort:

- measured exponent on deterministic shuffled inputs: 1.220
- in-place result: correct
- slice reads/writes: 0 / 0
- recursive call depth in the runtime probe: 11

This profile demonstrates the expected functional and algorithmic behaviour across all six tasks.
