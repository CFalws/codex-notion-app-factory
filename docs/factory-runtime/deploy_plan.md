# Factory Runtime Deploy Plan

## Iteration 205

This deploy plan validates intentional selected-thread switch continuity in the mounted conversation-first workspace.

## Deployment Impact

This iteration keeps transport and ownership unchanged while validating the existing switch-continuity behavior. The mounted conversation shell and fixed composer should persist through intentional thread switches, with stale owner chrome cleared and one compact switching placeholder bridging to the new snapshot.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm an intentional selected-thread switch keeps the mounted conversation shell visible and never falls through to the generic empty workspace.
6. Confirm the bottom-fixed composer dock remains visible and usable throughout the switch path.
7. Confirm stale owner chrome clears immediately, only one compact switching placeholder appears, and reconnect, polling fallback, deselection, restore-gap loss, and terminal completion still downgrade or clear correctly.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch path passes only when there is no empty-state flash, no hidden composer dock, no duplicate switching placeholders, and no stale owner residue.
