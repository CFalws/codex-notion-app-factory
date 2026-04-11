# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes only sticky left-rail active-session-row continuity in the existing conversation-first workspace. The bounded expectation is that the row stays visible for the healthy selected thread, retargets to one non-owned switching row during intentional thread changes, and clears immediately when the selected-thread path degrades or becomes truly idle.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two existing conversations.
4. Select a conversation on the healthy SSE-owned path and confirm the active-session row stays visible with `OWNER`, current phase, and `LIVE` or `NEW` or `PAUSED` follow state.
5. Click a different conversation and confirm the row stays mounted as one non-owned `SWITCHING` row for the pending target while the center shell and composer remain mounted.
6. Before that switch resolves, click another conversation and confirm the row retargets immediately to the newer selection without restoring stale previous owner text or duplicate switching rows.
7. Confirm the row clears immediately on reconnect downgrade, polling fallback, terminal completion, and true no-conversation idle.
8. Confirm non-selected conversation rows remain snapshot-only and never appear live-owned.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible active-session-row path succeeds through the intended selected-thread continuity contract.
