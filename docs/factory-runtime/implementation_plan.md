# Factory Runtime Implementation Plan

## Iteration 80

Record the active-session-row continuity contract for this proposal branch without widening the already-correct implementation scope.

1. Reuse the existing selected-thread session summary, follow, and thread-transition datasets instead of inventing a second rail state model.
2. Extend `syncActiveSessionRow(...)` so the sticky left-rail row mirrors healthy selected-thread `OWNER`, phase, and `LIVE` or `NEW` or `PAUSED` state from the current session datasets.
3. Add one bounded switching branch so the same row stays mounted as non-owned `TARGET · SWITCHING · ATTACH` for the pending conversation during intentional thread changes.
4. Keep degraded reconnect, polling fallback, terminal idle, and true idle behavior explicit by clearing the row immediately when ownership is no longer healthy or switching.
5. Extend focused browser-proof verifiers and iteration artifacts around the bounded active-session-row continuity contract.
