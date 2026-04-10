# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the selected-thread transcript render and verification layers. The bounded expectation is that healthy live autonomy progress now appears through one transcript-tail live activity item, while degraded and handoff paths remain explicit but separate, and stale healthy ownership is cleared immediately on degraded or switched paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Confirm the healthy selected-thread path shows exactly one transcript-tail live activity item with the current live phase and inline autonomy chips, and that the separate inline session block does not also render as a healthy owner.
5. Trigger reconnect or polling fallback and confirm the transcript-tail live item disappears immediately while the degraded inline session block takes over without stale healthy ownership.
6. Switch intentionally to another thread and confirm the healthy transcript-tail live item clears on the same transition that removes old selected-thread ownership from the center workspace.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm header, rail, footer, and transcript all agree on the intended selected-thread SSE path through the browser DOM.
