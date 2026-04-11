# Factory Runtime Deploy Plan

## Iteration 206

This deploy plan validates the healthy selected-thread append SSE path as the sole realtime authority for session state.

## Deployment Impact

This iteration keeps transport unchanged while tightening healthy-path ownership. Job, phase, proposal, verifier, and apply state should now remain append-SSE-owned on the selected thread until explicit authority loss downgrades back to polling fallback.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm the visible job, phase, proposal readiness, verifier state, and apply availability change immediately from append SSE without a polling-owned overwrite on the healthy path.
6. Confirm bootstrap attach does not trigger a healthy-path `syncLatestJob` or goals-summary mutation when append SSE session status is already authoritative.
7. Confirm reconnect downgrade, polling fallback, switch, deselection, restore-gap loss, and terminal completion still re-enable fallback behavior only after explicit authority loss.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy path passes only when append SSE remains the sole authority until downgrade and no stale polling-owned updates appear during healthy ownership.
