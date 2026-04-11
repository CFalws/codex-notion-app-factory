# Factory Runtime Deploy Plan

## Iteration 166

This deploy plan validates selected-thread switch continuity in the center workspace shell and bottom composer dock.

## Deployment Impact

This iteration keeps transport and transcript ownership unchanged while preserving the selected-thread shell through intentional switches and keeping the composer target row explicit at the bottom dock.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the composer target row shows `READY` for the attached selected thread.
5. Switch to a different conversation and confirm the center pane keeps the shell mounted, shows exactly one compact `SWITCHING` placeholder, and does not flash the generic empty state.
6. Confirm the bottom composer dock stays fixed in place during the switch and the composer target row remains visible with `SWITCHING` until the target snapshot attaches.
7. Confirm reconnect downgrade, polling fallback, deselection, terminal completion, and lost authority clear the composer target row instead of leaving stale ready state behind.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch placeholder and composer target row are driven only by current selected-thread state with no stale old-thread ownership.
