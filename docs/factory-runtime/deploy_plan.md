# Factory Runtime Deploy Plan

## Iteration 240

This deploy plan validates that the selected-thread workspace stays compact and chip-first while the existing session-status bootstrap plus SSE authority path remains unchanged.

## Deployment Impact

This iteration keeps transport and authority behavior intact and compacts the selected-thread session chrome. The gate should pass only when healthy, switching, restore, handoff, reconnect, and polling-fallback states remain readable through compact owner, phase, and target cues without reintroducing a second live-status owner or prose-heavy helper panel.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned progress, reconnect downgrade, polling fallback, terminal resolution, and a switch or restore path on desktop and phone widths.
5. Confirm the selected-thread header summary, transition placeholder, inline session block, and composer-adjacent strip use compact owner, phase, and target cues rather than sentence-style helper copy.
6. Confirm the transcript inline session block remains the only in-timeline live progress surface.
7. Confirm the unified header capsule, footer dock, and left-rail cues remain coherent on the same selected-thread authority path.
8. Confirm thread switch clears old-thread ownership immediately.
9. Confirm reconnect downgrade, polling fallback, terminal resolution, and deselection visibly downgrade or clear selected-thread state with no stale retention.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first, single-owner, compact, and free of reintroduced prose-heavy status panels.
