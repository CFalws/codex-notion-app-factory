# Factory Runtime Implementation Plan

## Iteration 92

Move selected-thread session-status ownership into the frontend store without changing transport or polling behavior.

1. Add a compact canonical selected-thread session-status helper in `ops-store.js` using existing append-stream, pending-handoff, session-phase, live-follow, app-session, and thread-transition state.
2. Make `isSelectedThreadSessionOwned(...)` delegate to that helper so polling control keeps the same behavior but shares the same ownership boundary.
3. Replace duplicated ownership and degradation checks in the center header, composer owner or transport strip, inline live block, and left-rail active-session row with reads from the canonical helper.
4. Keep reconnect, polling fallback, handoff, attach, and clear reasons explicit and finite, but do not change `/api/jobs` or `/api/goals` fallback policy in this iteration.
5. Reconfirm the focused verifier layer and record the iteration-92 boundary contract in the durable proposal artifacts.
