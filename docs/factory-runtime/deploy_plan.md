# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes only selected-thread switch continuity in the existing conversation-first workspace. The bounded expectation is that intentional switches keep the mounted shell and composer visible, one switching placeholder remains in place, and stale older switch results can no longer retake the workspace after a newer selection.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two existing conversations.
4. Select a conversation on the healthy path and confirm the central shell and fixed composer are mounted.
5. Click a different conversation and confirm exactly one switching placeholder appears, old-thread live ownership clears immediately, and the generic empty state does not flash.
6. Before that switch resolves, click another conversation and confirm the placeholder retargets to the new selection without restoring stale ownership or duplicate placeholders.
7. Confirm the transition clears when the latest target attaches, and that degraded fallback still clears ownership before fallback surfaces appear.
8. Confirm true no-conversation idle is still the only path that shows the generic empty timeline state.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread switch path succeeds through the intended continuity contract.
