# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that healthy selected-thread SSE ownership now drives visible phase, apply readiness, and recent activity immediately from conversation events, while polled job state remains only the degraded fallback path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an active selected conversation.
4. Trigger a healthy selected-thread SSE session through proposal, review, verify, `READY`, and `APPLIED` states and confirm the visible phase chips and recent activity update immediately from append events.
5. Confirm the apply control becomes enabled from the same selected-thread SSE-owned state when `READY` appears and clears again after `APPLIED`.
6. Confirm reconnect downgrade, polling fallback, thread switch, ownership loss, and non-selected threads fall back to the existing polled or snapshot path without stale healthy state.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm healthy visible status updates no longer depend on 3-second polling while the selected thread remains SSE-owned.
