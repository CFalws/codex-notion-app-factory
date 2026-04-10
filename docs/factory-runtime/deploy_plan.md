# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes selected-thread attach semantics on the existing SSE route. The bounded expectation is that healthy attach hydrates from `session.bootstrap` on the authoritative stream, while degraded fallback remains explicit through attach-mode datasets and compatible snapshot recovery.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Click into a selected thread on a healthy internal SSE path and confirm attach completes without a separate `GET /api/conversations/{id}` fetch after selection.
5. Confirm the stream emits `session.bootstrap` with version `1`, attach mode `sse-bootstrap`, and enough data to hydrate transcript continuity before new append events arrive.
6. Confirm the session strip and thread scroller expose `attachMode=sse-bootstrap` and `bootstrapVersion=1` on the healthy attach path.
7. Force degraded attach or fallback conditions and confirm attach mode flips to explicit snapshot fallback instead of looking like healthy realtime bootstrap.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible attach path passes the bootstrap-no-snapshot assertion on the intended path.
