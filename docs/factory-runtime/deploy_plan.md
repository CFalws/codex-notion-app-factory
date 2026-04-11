# Factory Runtime Deploy Plan

## Iteration 130

This deploy plan validates the unified center-lane live timeline contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes center-lane render composition only. The bounded expectation is that the transcript-tail live activity item becomes the primary selected-thread session surface and duplicate selected-thread session-event cards collapse whenever that primary surface is present.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the transcript-tail live activity item carries phase, path verdict, verifier acceptability, blocker, and proposal progression as the primary center-lane session surface.
5. Confirm duplicate selected-thread session-event cards do not remain visible beside that live activity item on the healthy path.
6. Trigger reconnect downgrade, polling fallback, handoff, restore, switching, deselection, and terminal resolution and confirm the same transcript-tail surface downgrades or clears immediately without stale live-owned center-lane treatment.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible unified live-timeline contract succeeds through the intended path.
