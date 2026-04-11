# Factory Runtime Deploy Plan

## Iteration 176

This deploy plan validates switch-path continuity in the conversation-first workspace.

## Deployment Impact

This iteration keeps transport and healthy live ownership unchanged while tightening the intended thread-switch path so the center shell and fixed composer stay mounted and the incoming thread target remains explicit.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled, then intentionally switch to another thread.
5. Confirm the center workspace never flashes the generic no-conversation empty state during the switch and instead shows one compact transition placeholder until the incoming snapshot attaches.
6. Confirm the fixed composer stays mounted, its target remains on the incoming conversation, and old-thread live ownership clears immediately.
7. Confirm reconnect downgrade, polling fallback, deselection, restore-gap, switch cancellation, and terminal completion still clear or downgrade live-owned treatment immediately.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch path preserves the conversation shell, shows exactly one transition placeholder, and never falls through to a generic empty workspace until true no-selection idle.
