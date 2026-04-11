# Factory Runtime Deploy Plan

## Iteration 174

This deploy plan validates the transcript as the single healthy selected-thread canonical live session surface.

## Deployment Impact

This iteration keeps transport and healthy live ownership unchanged while moving the visible healthy selected-thread session contract into the transcript live activity item and suppressing duplicate summary surfaces on that same path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation with internal append SSE enabled and confirm the central transcript shows exactly one canonical live activity item with phase, milestone progression, intended-path, verifier, and blocker state from `session_status`.
5. Confirm the header summary row and secondary facts surface suppress themselves on that same healthy path instead of competing with the transcript item.
6. Confirm reconnect downgrade, polling fallback, restore, handoff, deselection, and terminal completion immediately stop looking like healthy canonical continuity.
7. Confirm the footer, rail, and composer still reflect the selected thread without reintroducing a second healthy primary session surface in the center pane.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy selected-thread path shows one canonical transcript live session item and suppressed duplicate summary chrome.
