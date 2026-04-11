# Factory Runtime Deploy Plan

## Iteration 164

This deploy plan validates the selected-row live session mirror in the left conversation rail.

## Deployment Impact

This iteration keeps the center-pane session surfaces unchanged and adds one selected-card live marker row so the navigator and workspace agree immediately about the active live thread.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the selected conversation row shows one compact chip-first marker with finite labels `HANDOFF`, `LIVE`, `NEW`, or `PAUSED` plus one bounded cue.
5. Confirm non-selected conversation rows remain snapshot-only and do not gain live-owned markers.
6. Confirm reconnect downgrade and polling fallback clear the selected-row live marker instead of leaving stale ownership behind.
7. Confirm thread switch, deselection, and terminal completion clear the selected-row marker immediately without stale carryover.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-row marker is driven only by current selected-thread state and does not appear on recent-thread chips or non-selected rows.
