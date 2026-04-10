# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, dock behavior, transcript-tail live surface, and selected-row live-owner cues intact, but replaces the old blank thread-switch reset with a compact in-place session handoff placeholder.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Switch between two conversations and confirm the center pane keeps the conversation surface and composer anchored, clears old-thread live cues immediately, and shows exactly one compact transition placeholder until the target snapshot attaches.
5. Submit a new message in the selected thread and confirm the selected row still flips to `HANDOFF`, then to `LIVE`, and surfaces `NEW` or `PAUSED` only for the selected thread as the session state changes.
6. Confirm non-selected rows continue to show only snapshot labels and bounded preview lines even while the selected thread is active.
7. Confirm thread-switch transition cues clear as soon as the new snapshot attaches or degraded fallback takes over, without leaving stale live markers in the rail or center pane.
8. Confirm transcript plus composer reachability do not regress on phone or desktop widths and that the transition placeholder does not become a second persistent status surface.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals, stale live leakage, or transition-state residue.
