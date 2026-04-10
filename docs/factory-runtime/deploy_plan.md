# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation, client synchronization, and verification layers. The bounded expectation is that the healthy selected-thread append stream now refreshes adjacent session state immediately, while polling remains only as an explicit degraded fallback.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an app that has a healthy selected-thread live session.
4. Trigger `job.running`, `goal.review.phase`, `goal.verify.phase`, and `proposal.ready` on the selected thread and confirm the central job activity, apply readiness, and autonomy summary update immediately after the append arrives.
5. Confirm no recurring selected-job poller remains active while the selected thread is healthy and SSE-owned.
6. Confirm reconnect, polling fallback, ownership loss, or switched-away paths immediately restore the fallback polling path and clear live-only projections.
7. Confirm non-selected threads remain snapshot-only and do not gain append-driven live semantics.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the append-driven synchronization contract passes through the intended selected-thread surface.
