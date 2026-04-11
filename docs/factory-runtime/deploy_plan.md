# Factory Runtime Deploy Plan

## Iteration 123

This deploy plan validates the healthy selected-thread SSE authority contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes authority handling only. The bounded expectation is that healthy selected-thread SSE appends remain the sole visible source for live job meta, proposal readiness, verifier progress, and autonomy state, while reconnect and polling fallback remain explicit degraded paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm proposal, review, verify, ready, apply, and terminal job state appear immediately in the center session timeline, header, and footer without waiting for polling.
5. Confirm a late poll tick does not overwrite visible job meta, proposal readiness, or autonomy state while the selected-thread SSE path remains authoritative.
6. Trigger reconnect or polling fallback and confirm the same state downgrades explicitly in the same render cycle and polling resumes ownership only on that degraded path.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread authority contract succeeds through the intended path.
