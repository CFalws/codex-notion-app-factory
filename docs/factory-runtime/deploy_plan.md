# Factory Runtime Deploy Plan

## Iteration 131

This deploy plan validates the shared selected-thread session-surface contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread session derivation and render composition only. The bounded expectation is that the transcript-tail live activity item and the composer-adjacent session strip render from the same canonical selected-thread session surface model and therefore stay aligned on healthy and degraded paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the transcript-tail live activity item and composer-adjacent session strip show the same selected-thread phase, verifier acceptability, blocker, and milestone authority in the same render pass.
5. Confirm proposal or snapshot-only state does not imply healthy live ownership on either surface.
6. Trigger reconnect downgrade, polling fallback, restore, switching, deselection, and terminal resolution and confirm both surfaces downgrade or clear together in the same render cycle.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible shared selected-thread session-surface contract succeeds through the intended path.
