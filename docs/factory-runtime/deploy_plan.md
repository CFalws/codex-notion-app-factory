# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside selected-thread autonomy presentation and verification layers. The bounded expectation is that healthy selected-thread autonomy authority now appears only inside the center live session item, while the side-panel autonomy detail remains secondary-only outside that healthy state.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Start a healthy selected-thread SSE-owned run and confirm the center live session item shows autonomy blocker, path, and verifier state inline while the side-panel autonomy detail card is hidden.
5. Confirm reconnect, polling fallback, ownership loss, terminal idle, or thread switch clear the center live autonomy authority item instead of leaving stale healthy cues.
6. Confirm the side-panel autonomy detail remains available again outside the healthy selected-thread SSE authority state.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible workspace shows exactly one healthy autonomy authority surface in the center timeline instead of duplicating it in the side panel.
