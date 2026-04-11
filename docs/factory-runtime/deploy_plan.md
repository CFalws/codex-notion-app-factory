# Factory Runtime Deploy Plan

## Iteration 101

This deploy plan validates the selected-thread autonomy authority contract on the healthy SSE path and does not introduce new transport, new layout surfaces, or broad polling refactors beyond tightening when `/api/goals` may act as fallback.

## Deployment Impact

This iteration changes selected-thread autonomy authority only. The bounded expectation is that healthy selected-thread `session.bootstrap` plus live append events own blocker, path, verifier, and apply state immediately, while `/api/goals` remains available only for degraded, stale, or missing-authority cases.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Drive a healthy selected-thread SSE session and confirm proposal, review, verify, ready, and applied autonomy state appears from session bootstrap plus append events without a `/api/goals` owned success path.
6. Confirm the fixed composer remains bound to the same conversation and the center-pane live surface remains unchanged from iteration 100.
7. Confirm degraded reconnect, missing authority, or stale-or-missing bootstrap data still allow explicit `/api/goals` fallback instead of silently dropping autonomy state.
8. Confirm no new `/api/jobs` suppression or transport change was introduced in this iteration beyond the existing intended-path behavior.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread autonomy authority contract succeeds through the intended path.
