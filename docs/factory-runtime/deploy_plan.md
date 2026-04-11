# Factory Runtime Deploy Plan

## Iteration 117

This deploy plan validates the selected-thread transcript live-lane contract and does not introduce new transport, polling behavior, or a backend switch protocol.

## Deployment Impact

This iteration changes center transcript presentation only. The bounded expectation is that the healthy selected-thread path shows one compact live session lane at the transcript tail with milestone progression and autonomy-path datasets on the article itself, while degraded and non-healthy paths clear or downgrade that lane immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the transcript shows exactly one live session article at the tail.
5. Confirm that article publishes explicit proposal or review or verify or ready or applied progression, milestone chips, and path or verifier or blocker datasets without rendering a second transcript status meta block beneath it.
6. Confirm there is no duplicate healthy selected-thread session-event article or separate prose-heavy center-pane status surface.
7. Confirm reconnect downgrade, polling fallback, restore-only, switching, and terminal idle still clear or downgrade the live lane immediately.
8. Confirm the rail, composer strip, and detached follow contracts from earlier iterations remain unchanged.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread transcript live-lane contract succeeds through the intended path.
