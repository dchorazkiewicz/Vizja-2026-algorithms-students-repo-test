# Private grader layer

This directory demonstrates the instructor-side components that would be private in production.

It contains the reference implementation, AST analysis helpers, runtime instrumentation, empirical complexity helpers, and the report generator. The adjacent tests directory is also instructor-side in production.

## Evidence model

The grader combines independent forms of evidence.

**Functional evidence** asks whether the implementation produces the required result.

**Structural evidence** asks which programming constructs and shortcuts appear in the source.

**Runtime evidence** asks how the implementation actually interacts with the data.

**Growth evidence** asks how measured operation cost changes as input size increases.

**Memory and side-effect evidence** captures copying, mutation, and selected runtime effects.

No single signal is treated as a universal proof of algorithmic quality. The value comes from combining several observations and binding them to a specific student commit.
