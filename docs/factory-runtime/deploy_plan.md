# Factory Runtime Deploy Plan

## Iteration 162

This deploy plan validates the canonical selected-thread inline timeline lane rendered from realtime `session_status`.

## Deployment Impact

This iteration keeps the existing selected-thread transport seam intact, but moves the canonical selected-thread session surface into the conversation timeline itself so non-message execution progress reads as one live session lane.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the conversation timeline shows one canonical inline session lane at the top with current phase, path state, verifier, blocker, proposal or apply readiness, and latest job id.
5. Confirm duplicate SSE session-event cards are suppressed while that canonical inline lane is visible.
6. Confirm reconnect downgrade and polling fallback keep that same lane visible but explicitly demoted.
7. Confirm switch, deselection, terminal completion, and lost authority clear the lane immediately without stale carryover.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible inline timeline lane is driven only by canonical `session_status`.
