# Factory Runtime Implementation Plan

1. Treat structured intended-path verdicts as the single bounded hypothesis for this iteration.
2. Add a small iteration-level contract with `expected_path`, `degraded_signals`, and `verdict`.
3. Compute that verdict from durable runtime signals the controller already owns instead of from prose.
4. Make continuation fail closed when the intended-path verdict is missing or degraded.
5. Prove both the healthy intended path and a fallback-only success path in the runtime contract test.
