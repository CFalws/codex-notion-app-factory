# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that intentional selected-thread switches continue using the compact attach placeholder and preserve one continuous session shell rather than flashing the generic empty timeline.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two available conversations.
4. Start an intentional thread switch and confirm the center workspace and bottom-fixed composer dock remain mounted while the attach is in progress.
5. Confirm old-thread live ownership clears immediately, exactly one compact attach placeholder appears, and the generic empty timeline does not flash during the handoff.
6. Confirm the session summary, composer owner row, and follow target all point at the incoming selected thread before the new snapshot attaches.
7. Confirm reconnect, ownership-loss, or polling fallback paths clear the live-owned transition treatment instead of pretending the new thread is already active.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the switch-continuity contract passes without reset-like empty-state flashes.
