# Factory Runtime Deploy Plan

## Iteration 170

This deploy plan validates the healthy selected-thread unified live timeline in the center pane.

## Deployment Impact

This iteration keeps transport and transcript-tail live ownership unchanged while suppressing duplicate healthy selected-thread milestone session-event cards so the transcript-tail live activity becomes the only primary live session item.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the center timeline shows exactly one primary transcript-tail live activity item.
5. Confirm proposal, review, verify, auto-apply, ready, and applied progression appears only in that item's milestone strip and datasets, not as separate selected-thread session-event cards.
6. Confirm reconnect downgrade, polling fallback, restore, deselection, switching, and terminal-cleared paths immediately stop collapsing those milestone cards and do not leave stale healthy ownership behind.
7. Confirm non-live historical rendering remains explicit outside the healthy selected-thread path.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy center timeline exposes exactly one selected-thread primary live item with no duplicate selected-thread session-event cards.
