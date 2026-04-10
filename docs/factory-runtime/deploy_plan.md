# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the selected-thread transcript render and verification layers. The bounded expectation is that healthy selected-thread session milestones now appear as compact timeline rows sourced directly from append events, while degraded and switch paths keep their existing inline indicators without stale healthy ownership.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Trigger proposal, review, verify, auto-apply, ready, applied, completed, and failed transitions on the selected thread and confirm the central timeline renders compact session-event rows instead of generic event cards for those milestones.
5. Confirm the bottom-fixed composer remains unchanged and attached to the same selected-thread workspace while those session-event rows appear.
6. Confirm reconnect, polling fallback, or thread-switch paths do not leave stale healthy current-session rows visible, and that the existing degraded indicator or switch placeholder still owns the current-session surface during those transitions.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the session-event timeline projection passes through the intended selected-thread path.
