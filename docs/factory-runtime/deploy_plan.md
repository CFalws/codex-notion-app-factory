# Factory Runtime Deploy Plan

## Iteration 159

This deploy plan validates the canonical selected-thread `session_status` append-SSE contract plus the new compact center-pane live session strip.

## Deployment Impact

This iteration adds a canonical append-SSE `session_status` payload and consumes it in exactly one compact selected-thread session strip above the transcript. The transcript append flow, footer composer docking, rail mirroring, and secondary detail drawer remain otherwise unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the center pane shows one compact live session strip above the transcript with current phase, path verdict, verifier acceptability, and blocker state sourced from append-SSE `session_status`.
5. Confirm reconnect downgrade and polling fallback demote that same strip immediately instead of leaving it healthy-looking.
6. Confirm switch, deselection, and terminal completion clear the strip without stale carryover.
7. Confirm the transcript append flow, footer composer, rail markers, and secondary detail drawer still behave as before.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible center-pane strip succeeds through the intended selected-thread session-status path.
