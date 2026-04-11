# Factory Runtime Deploy Plan

## Iteration 167

This deploy plan validates the sticky active-session row above the conversation list in the left navigator.

## Deployment Impact

This iteration keeps transport and center-pane ownership unchanged while making the selected-thread sticky active-session row persist in the left navigator across healthy, handoff, paused, unseen, and switching states only.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the sticky active-session row above the conversation list is visible and selected-thread-only.
5. Confirm handoff, paused follow, and unseen selected-thread paths update that row with compact chips while non-selected rows remain snapshot-only.
6. Switch to a different conversation and confirm the sticky row flips to one bounded `SWITCHING` state for the selected thread only, then clears or reattaches correctly when the target snapshot resolves.
7. Confirm reconnect downgrade, polling fallback, deselection, terminal completion, and lost authority clear the sticky row instead of leaving stale ownership behind.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible sticky row is driven only by the current selected-thread session seam and never appears live-owned for non-selected rows.
