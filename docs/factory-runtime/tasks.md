# Factory Runtime Tasks

- [x] Keep the existing selected-thread render surfaces and selected-thread-only ownership rules unchanged.
- [x] Replace the append-path autonomy refetch trigger with a client-side projection from healthy selected-thread SSE events into `state.autonomySummary`.
- [x] Reuse the existing live phase event types so inline autonomy chips and compact session markers update immediately from append delivery.
- [x] Leave `refreshGoalSummary()` in place for initial app load, thread attach, and degraded recovery paths.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the append-driven autonomy projection contract.
