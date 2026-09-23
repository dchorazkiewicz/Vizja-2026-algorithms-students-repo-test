# Private grader layer — List 02

This directory demonstrates the instructor-side implementation that would remain private in production.

The grader is intentionally multi-layered.

## Evidence sources

- **functional** — does the implementation return the required result?
- **property-based** — does correctness hold across generated inputs?
- **AST** — does the source contain the requested structural method rather than a library shortcut?
- **runtime instrumentation** — what data is actually read, compared and written?
- **stability probes** — are equal-key identities preserved where required?
- **adaptivity probes** — does insertion sort behave differently on sorted and reverse inputs?
- **data-movement probes** — does selection sort avoid bubble-sort-like write volume?
- **recursion traces** — are divide-and-conquer methods actually recursive?
- **complexity experiments** — how does measured comparison cost grow as input size doubles?
- **memory diagnostics** — what allocation pattern is visible at runtime?

The report generator keeps these observations separate rather than collapsing everything into one opaque score.
