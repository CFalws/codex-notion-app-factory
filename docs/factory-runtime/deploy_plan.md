# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-conversation SSE path. The bounded expectation is that the composer visibly names the selected target thread and shows `READY`, `SWITCHING`, or `HANDOFF` from existing selected-thread ownership state, while send is blocked only during unresolved attach.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the composer target row always names the currently selected thread on desktop and phone widths.
5. Switch threads and confirm the target row immediately leaves the old thread, shows `SWITCHING`, and blocks send until the new snapshot attaches.
6. Submit a message and confirm the target row shows `HANDOFF` until the first assistant append or terminal resolution.
7. Confirm reconnect or polling fallback degrades the row back to non-live `READY` instead of falsely advertising live ownership.
8. Confirm the session strip, bottom follow control, and selected-row ownership cues remain otherwise unchanged.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals, stale old-thread target ownership, or polling-derived live target state.
