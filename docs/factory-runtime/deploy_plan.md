# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-conversation SSE path. The bounded expectation is that intentional thread switches keep the center conversation shell and composer dock visible, clear stale old-thread live ownership immediately, and show at most one compact transition placeholder until the new selected-thread snapshot attaches.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Switch between conversations on desktop and phone widths and confirm the center pane stays attached instead of dropping to a generic empty-state reset.
5. Confirm old-thread live strip and follow ownership clear immediately when a new thread is selected.
6. Confirm exactly one compact transition placeholder appears while the incoming snapshot attaches, and that it clears as soon as the new selected-thread state binds.
7. Confirm the center header, footer composer, bottom follow control, and selected-row ownership cues remain otherwise unchanged.
8. Confirm the workspace still reads as conversation-first on desktop and phone widths.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals, stale old-thread ownership, or a generic reset during thread switches.
