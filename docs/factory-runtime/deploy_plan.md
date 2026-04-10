# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the selected-thread client synchronization and verification layers. The bounded expectation is that healthy selected-thread SSE events now update autonomy and phase-adjacent session state directly in the live session surfaces without an extra app-goals refetch on each live phase event.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Trigger proposal, review, verify, auto-apply, ready, applied, and failed transitions on the selected thread and confirm the inline session block plus compact session markers update immediately from the arriving append event.
5. Confirm those healthy live transitions do not trigger an app-goals refetch, while initial load, thread attach, and degraded recovery still use the existing goal fetch path.
6. Confirm reconnect, polling fallback, or switched-away paths still clear live-owned treatment and do not leave stale autonomy chips behind.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread append-driven autonomy projection contract passes through the intended path.
