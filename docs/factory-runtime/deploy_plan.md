# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that intentional thread switches now preserve the conversation-first shell, keep the composer dock mounted, and show a compact attach placeholder instead of a reset-like empty workspace.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two recent conversations in the selected app lane.
4. Trigger an intentional thread switch and confirm the center conversation shell and composer dock remain mounted while the switch is in progress.
5. Confirm the session summary and composer owner row switch to SWITCHING or ATTACH for the target thread, the old thread loses live-owned treatment immediately, and exactly one compact attach placeholder appears in the timeline.
6. Confirm the generic empty state does not flash during the switch and that the placeholder clears as soon as the target snapshot attaches.
7. Confirm reconnect downgrade, polling fallback, terminal idle, and non-selected threads do not retain stale live ownership after the switch path completes.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the thread-switch continuity proof passes without reset-like empty-state flashes or stale old-thread live markers.
