# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that an intentional selected-thread switch keeps the center conversation shell and composer dock mounted, clears stale live ownership from the old thread immediately, and renders exactly one compact attach placeholder until the new snapshot and append stream attach.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path and at least one additional thread available for switching.
4. Confirm an intentional selected-thread switch never flashes the generic empty-state view and instead shows exactly one compact transition placeholder in the center pane.
5. Confirm the previous thread's live-owned chips, rails, and strip clear immediately on switch and that no non-selected thread gains live-owned treatment.
6. Confirm the transition placeholder clears as soon as the target snapshot attaches and the selected-thread conversation resumes through the intended path.
7. Confirm transcript history, composer access, and the secondary panel remain continuously reachable on phone-sized layouts while the switch placeholder appears and clears.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the thread-transition continuity proof passes without unexpected degraded-path signals or stale live ownership.
