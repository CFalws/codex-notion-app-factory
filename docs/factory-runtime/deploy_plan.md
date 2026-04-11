# Factory Runtime Deploy Plan

## Iteration 119

This deploy plan validates the unified selected-thread footer session-bar contract and does not introduce new transport, polling behavior, or a backend switch protocol.

## Deployment Impact

This iteration changes footer presentation only. The bounded expectation is that the healthy selected-thread SSE path exposes one footer session bar that carries live phase progression while following and switches into `NEW` or `PAUSED` follow action when detached, while degraded and non-selected paths clear that footer follow treatment immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the footer session strip is the only live-owned footer surface above the composer.
5. Scroll away from the live tail and confirm the same footer bar switches into `NEW` or `PAUSED` follow action with unseen-count metadata instead of showing a separate transcript-bottom follow button.
6. Click the footer bar action and confirm follow clears immediately and the old transcript-bottom follow button stays hidden.
7. Confirm switching, reconnect downgrade, polling fallback, terminal idle, and deselection clear or degrade footer follow treatment immediately and do not leave stale live-owned cues behind.
8. Confirm the rail and center live session lane contracts from earlier iterations remain unchanged.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible unified footer session-bar contract succeeds through the intended path.
