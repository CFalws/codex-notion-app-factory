# Factory Runtime Tasks

## Iteration 104

- [x] Add a footer-follow helper that derives healthy selected-thread `NEW` and `PAUSED` state from the existing live-follow datasets.
- [x] Render detached healthy follow state only in the composer-adjacent session strip instead of as a visible transcript-level jump control.
- [x] Make the existing session-strip toggle execute `jumpToLatest(...)` while the footer owns follow state.
- [x] Clear or downgrade footer follow ownership immediately on reconnect, polling fallback, terminal idle, and thread switch.
- [x] Align focused verifiers and proposal artifacts with the iteration-104 unified footer-follow contract.
