# Factory Runtime Deploy Plan

## Iteration 153

This deploy plan validates the selected-thread center-pane session convergence contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes center-pane selected-thread session presentation and verification only. The bounded expectation is that the transcript-native live activity becomes the sole selected-thread session item across healthy, handoff, degraded, and restore states while duplicate inline ownership surfaces clear immediately on degraded and switching paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the center timeline shows exactly one selected-thread live session item with the current phase plus path, verifier, and blocker chips, with no separate inline session block.
5. Trigger a bounded pending handoff and confirm the same transcript-native session item flips to `HANDOFF` without rendering a second inline handoff block.
6. Trigger reconnect downgrade or polling fallback and confirm the same center item downgrades in place while no inline selected-thread session block remains visible.
7. Trigger restore attach, terminal idle, deselection, and thread switch and confirm the center pane shows at most one selected-thread session item and clears duplicate ownership surfaces immediately.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible center-pane convergence contract succeeds through the intended selected-thread session path.
