# Factory Runtime Implementation Plan

## Iteration 193

Lock the already-present healthy selected-thread transcript-tail session-event collapse path into the iteration 193 proposal artifacts.

1. Keep the change bounded to the existing transcript-tail live activity and session-event seams.
2. Preserve healthy selected-thread SSE ownership as the one authoritative transcript-tail live session block.
3. Collapse duplicate selected-thread SSE session-event cards only while that healthy live block is authoritative.
4. Preserve machine-readable datasets for phase progression, append provenance, intended-path verdict, verifier acceptability, and blocker state across `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, and `APPLIED`.
5. Restore or fail open immediately on degraded, reconnect, polling fallback, restore-gap, deselected, switched, and terminal paths.
6. Align focused verification and proposal artifacts with the iteration-193 single-block healthy-path contract.
