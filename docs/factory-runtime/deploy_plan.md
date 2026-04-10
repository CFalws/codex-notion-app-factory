# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes selected-thread phase semantics on the existing SSE route. The bounded expectation is that healthy selected-thread attach and resume expose one authoritative phase payload across the existing live surfaces, while non-authoritative cases stay neutral as `LIVE` or `UNKNOWN`.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Click into a selected thread on a healthy internal SSE path and confirm attach completes without a separate `GET /api/conversations/{id}` fetch after selection.
5. Confirm `session.bootstrap` carries `session_phase`, version `2`, and attach mode `sse-bootstrap`.
6. Submit a request and confirm the session strip, thread scroller, and inline live block all report the same phase value and provenance from the authoritative phase model.
7. Confirm `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, `APPLIED`, and `FAILED` appear only when `phaseAuthoritative=true`.
8. Confirm all other selected-thread live cases render `LIVE` or `UNKNOWN` instead of inferred proposal or review states.
9. Trigger a transient reconnect and confirm the resumed selected-thread path still preserves the same phase value and provenance across the live surfaces.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible phase contract passes on the intended attach and resume paths.
