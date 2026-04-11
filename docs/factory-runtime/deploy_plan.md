# Factory Runtime Deploy Plan

## Iteration 148

This deploy plan validates the selected-thread left-rail session-mirroring contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread left-rail active-session presentation and verification only. The bounded expectation is that the row mirrors the selected-thread session owner, phase, follow, handoff, and switching state directly from the selected-thread session contract while failing closed on degraded paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the active-session row is visible with `SSE OWNER`, the selected-thread phase label, and `LIVE`, `NEW`, or `PAUSED` follow cues that match the selected-thread workspace.
5. Trigger a bounded pending handoff and confirm the same row flips to `HANDOFF` without making any non-selected thread look live-owned.
6. Intentionally switch to another thread and confirm the row stays visible with compact `TARGET`, `SWITCHING`, and `ATTACH` cues while the center workspace is in the bounded switching state.
7. Trigger reconnect downgrade, polling fallback, terminal idle, and deselection and confirm the row clears or demotes immediately instead of preserving stale selected-thread ownership.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible rail-row contract succeeds through the intended selected-thread session path.
