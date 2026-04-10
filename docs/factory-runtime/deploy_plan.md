# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the bottom follow affordance now appears only when the selected SSE-owned thread has real unseen live backlog, so detached-tail recovery reads as a precise session control instead of a generic paused badge.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation attached through the internal append SSE path and enough history to scroll away from the tail.
4. Confirm the bottom follow control stays hidden while the selected thread is live but no unseen appends exist.
5. Scroll away, wait for unseen live appends, and confirm exactly one compact follow control appears with selected-thread ownership, explicit NEW or PAUSED labeling, and unseen-count metadata.
6. Confirm the control never appears for polling-only or non-selected threads and clears immediately on jump-to-latest, thread switch, reconnect downgrade, polling fallback, or terminal completion.
7. Confirm transcript history, the inline transcript-tail live block, and composer access remain reachable on phone widths while the follow control appears and clears.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the detached-tail follow proof passes without stale paused exposure or non-selected-thread ownership.
