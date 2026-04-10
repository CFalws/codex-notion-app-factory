# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-conversation switch path. The bounded expectation is that the center pane and composer stay mounted during intentional thread switches, old-thread ownership clears immediately, and one compact `SWITCHING` placeholder bridges the attach gap until the new snapshot binds.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Switch threads on desktop and phone widths and confirm the old thread loses live-owner treatment immediately.
5. Confirm the transcript and composer shell stay mounted while the switch is in progress.
6. Confirm exactly one compact `SWITCHING` placeholder appears until the new snapshot attaches.
7. Confirm send stays blocked only while attach is unresolved and resumes normally once the new selected thread is bound.
8. Confirm no generic empty-state flash, duplicate live strip, or duplicate transcript activity block appears during the switch.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals or stale old-thread ownership during the transition.
