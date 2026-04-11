# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes the selected-thread autonomy hydration contract in the existing conversation-first workspace. The bounded expectation is that both conversation snapshot and `session.bootstrap` expose the same minimal server-authored autonomy freshness envelope before any goals fallback runs.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Confirm `GET /api/conversations/{id}` returns `autonomy_summary` with `source=conversation-snapshot`, a `generated_at` timestamp, a machine-readable `freshness_state`, and explicit `fallback_allowed`.
5. Confirm `session.bootstrap` returns top-level `autonomy_summary` plus `conversation.autonomy_summary`, both with the same freshness semantics and generated timestamp.
6. Confirm healthy bootstrap attach exposes `fallback_allowed=false` while snapshot fallback still exposes `fallback_allowed=true`.
7. Confirm missing or degraded autonomy freshness uses the canonical `freshness_state=stale-or-missing` marker.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread attach path still works with the new additive autonomy envelope.
