# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes the selected-thread autonomy ownership boundary in the existing conversation-first workspace. The bounded expectation is that healthy selected-thread attach, resume, and switch stay on the existing snapshot-plus-SSE path without hidden goals polling, while degraded freshness or ownership loss explicitly reopens the fallback path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Confirm `GET /api/conversations/{id}` returns `autonomy_summary` with `source=conversation-snapshot`, a `generated_at` timestamp, a machine-readable `freshness_state`, and explicit `fallback_allowed`.
5. Confirm `session.bootstrap` returns top-level `autonomy_summary` plus `conversation.autonomy_summary`, both with the same freshness semantics and generated timestamp.
6. Confirm healthy bootstrap or resume attach with `fallback_allowed=false` performs no `/api/apps/{app_id}/goals` fetch after the selected-thread attach mark.
7. Confirm missing or degraded autonomy freshness uses the canonical `freshness_state=stale-or-missing` marker before goals polling is allowed again.
8. Confirm reconnect downgrade, session-ownership loss, or snapshot fallback visibly downgrades the selected-thread autonomy path before any goals fallback runs.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread attach path works through the intended snapshot-plus-SSE ownership contract.
