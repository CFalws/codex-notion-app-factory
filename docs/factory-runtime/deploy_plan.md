# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes selected-thread reconnect semantics on the existing SSE route. The bounded expectation is that healthy reconnect resumes from `session.bootstrap` plus append cursor on the authoritative stream, while degraded fallback remains explicit through attach-mode and resume-mode datasets.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Click into a selected thread on a healthy internal SSE path and confirm attach completes without a separate `GET /api/conversations/{id}` fetch after selection.
5. Confirm the stream emits `session.bootstrap` with version `2`, attach mode `sse-bootstrap`, and enough data to hydrate transcript continuity before new append events arrive.
6. Trigger a transient selected-thread disconnect and confirm the next reopen uses `/append-stream?after={lastAppendId}`, emits `session.bootstrap` with attach mode `sse-resume`, and does not start job polling or fetch `/api/conversations/{id}` on the healthy resume path.
7. Confirm the session strip and thread scroller expose `attachMode=sse-resume`, `bootstrapVersion=2`, non-zero `resumeCursor`, and `resumeMode=resumed` after healthy reconnect.
8. Force degraded reconnect or repeated resume failure and confirm fallback becomes explicit instead of looking like healthy realtime resume.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible attach and reconnect paths pass the bootstrap-resume intended-path assertions.
