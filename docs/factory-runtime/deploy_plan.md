# Factory Runtime Deploy Plan

## Iteration 144

This deploy plan validates the compact header ownership-indicator contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread header presentation and verification only. The bounded expectation is that the header exposes one compact ownership chip for healthy SSE, degraded, and restore states while the center timeline remains the only authority-looking live session surface.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the header shows one compact `SSE OWNER` indicator while the summary prose stays demoted and the timeline remains the authority surface.
5. Trigger reconnect, polling fallback, and restore and confirm the same indicator flips to the correct downgraded label and provenance in the same render pass.
6. Trigger switching, deselection, and terminal idle and confirm the indicator disappears immediately without leaving stale ownership cues.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible header ownership contract succeeds through the intended selected-thread session path.
