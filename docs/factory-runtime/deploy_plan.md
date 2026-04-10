# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on selected-thread switch continuity. The bounded expectation is that intentional thread switches keep the shell mounted, clear stale old-thread ownership immediately, and show only one compact `SWITCHING` placeholder until the new snapshot attaches.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Intentionally switch between conversations and confirm the old thread loses live-owner treatment immediately.
5. Confirm the transcript shell and footer composer stay mounted during the switch instead of dropping to a generic empty reset.
6. Confirm exactly one compact `SWITCHING` placeholder appears until the new selected-thread snapshot attaches.
7. Confirm the generic empty state appears only in true no-conversation idle state, not during thread transitions.
8. Confirm desktop and phone widths keep the conversation-first shell stable through the switch path.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread switch continuity proof still passes without degraded-path signals.
