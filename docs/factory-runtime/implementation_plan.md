# Factory Runtime Implementation Plan

## Iteration 81

Tighten the composer-adjacent session strip into one authoritative selected-thread phase row without widening transport or layout scope.

1. Reuse the existing selected-thread SSE ownership, `liveRun`, `sessionPhase`, and degraded-path datasets.
2. Collapse the healthy selected-thread strip state row to one compact phase chip instead of multiple owner and transport chips.
3. Keep degraded reconnect and polling paths explicit by relabeling that same row to `RECONNECT` or `POLLING`.
4. Clear stale healthy phase copy immediately on thread switch or idle by moving the strip state row to transition or cleared state.
5. Extend focused browser-proof and static verifiers so the strip proves a single-chip phase-first contract with no healthy `/api/goals` fallback after submit.
