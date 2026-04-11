# Factory Runtime Deploy Plan

## Iteration 161

This deploy plan validates selected-thread switch continuity while the canonical center-pane live strip remains fail closed.

## Deployment Impact

This iteration keeps the existing selected-thread session strip and transport seam intact, but tightens the intentional switch path so the shell and composer stay mounted, the old thread clears immediately, and one compact transition placeholder owns the switch window.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the selected-thread center strip is visible only for the selected thread.
5. Switch to another thread and confirm the center shell stays mounted, the composer remains docked, the prior thread strip clears immediately, and exactly one compact transition placeholder remains until the new snapshot attaches.
6. Confirm reconnect downgrade, polling fallback, deselection, and terminal completion do not leave stale selected-thread ownership behind and do not let non-selected threads become the primary live surface.
7. Confirm the transcript append flow, footer composer, rail markers, and secondary detail drawer still behave as before.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch continuity path succeeds without flashing `.timeline-empty` during intentional switches.
