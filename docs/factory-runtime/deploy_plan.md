# Factory Runtime Deploy Plan

## Iteration 100

This deploy plan validates the single healthy selected-thread live-surface contract in the center pane and does not introduce new transport, new polling gates, or new status surfaces beyond that bounded frontend presentation change.

## Deployment Impact

This iteration changes healthy selected-thread presentation only. The bounded expectation is that healthy selected-thread SSE progress appears through exactly one transcript-tail live activity item, the composer-adjacent strip hides on that healthy path, restore or degraded states still keep the strip explicit, and existing polling behavior remains unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Drive a healthy selected-thread SSE session and confirm the transcript-tail live activity item is the only live-owned session surface in the center pane.
6. Confirm the composer-adjacent session strip hides on that healthy path, while the fixed composer remains bound to the same conversation.
7. Confirm restore, handoff, switching, reconnect, or polling fallback still expose the session strip with explicit downgraded or pending context.
8. Confirm no new `/api/jobs` or `/api/goals` suppression was introduced in this iteration beyond the existing intended-path behavior.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread single-surface contract succeeds through the intended path.
