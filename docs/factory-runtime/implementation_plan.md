# Factory Runtime Implementation Plan

1. Add one shared selected-thread session-ownership helper in the frontend state layer that combines existing SSE authority, pending handoff, and session phase signals.
2. Use that helper in `ops-jobs.js` to prevent routine polling from starting or continuing while the selected thread remains on the healthy SSE-owned active run.
3. Use the same helper in `app.js` so submit flows keep the no-job-poll rule after the handoff stage and into the active run.
4. Preserve existing degraded fallback behavior so reconnect downgrade, ownership loss, stale-or-missing freshness, or off-thread tracking can still reopen polling explicitly.
5. Align focused browser-proof verifiers and iteration artifacts around the bounded active-run polling-suppression contract.
