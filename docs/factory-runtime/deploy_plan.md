# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the selected-thread header now exposes one explicit transport-ownership marker in the main conversation workspace instead of relying on inferred healthy-path cues.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an active selected conversation.
4. Trigger a healthy selected-thread SSE run and confirm the header shows exactly one `SSE OWNER` chip adjacent to the session summary.
5. Confirm the chip publishes machine-readable ownership/source/reason markers and that no polling marker appears on the healthy path.
6. Trigger reconnect downgrade or retry and confirm the chip changes immediately to `RECONNECT`.
7. Trigger polling fallback or session-rotation fallback and confirm the chip changes immediately to `POLLING`.
8. Confirm the chip clears on thread switch, terminal idle, and non-selected-thread views.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread header ownership proof passes through the intended path without stale ownership on degraded or terminal states.
