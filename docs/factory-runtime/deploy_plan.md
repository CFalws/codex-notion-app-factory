# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the selected-thread inline session block becomes the only healthy live-progress surface in the main timeline, while the duplicate composer-adjacent strip stays hidden for those same states.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an active selected conversation.
4. Trigger a healthy selected-thread SSE session and confirm the center timeline shows exactly one live session item through handoff, proposal, review, verify, and retained terminal phases.
5. Confirm the composer-adjacent live strip stays hidden for those same healthy selected-thread states while the composer owner row remains visible.
6. Confirm the thread scroller still carries selected-thread ownership so follow-state and jump-to-latest behavior remain usable.
7. Confirm reconnect downgrade, polling fallback, thread switch, and ownership loss clear or downgrade immediately without leaving a duplicate healthy strip.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the single-surface healthy live-progress contract passes on desktop and phone widths.
