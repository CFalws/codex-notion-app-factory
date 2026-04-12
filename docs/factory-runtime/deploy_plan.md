# Factory Runtime Deploy Plan

## Iteration 239

This deploy plan validates that selected-thread autonomy state remains sourced from session-status bootstrap plus SSE rather than goals polling.

## Deployment Impact

This iteration keeps runtime behavior otherwise intact and removes selected-thread goals-poll authority from the active workspace. The gate should pass only when blocker, verifier, proposal, and apply state for the selected conversation remain attributable to session-status bootstrap plus SSE, and degraded or terminal transitions visibly downgrade or clear that state instead of silently refreshing it from polling.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned progress, reconnect downgrade, polling fallback, terminal resolution, and a switch or restore path on desktop and phone widths.
5. Confirm selected-thread blocker, verifier, proposal, and apply state update from session-status bootstrap plus SSE without waiting for `/api/apps/{appId}/goals`.
6. Confirm no selected-thread goals-poll refresh silently restores healthy-looking autonomy data while the transport is degraded.
7. Confirm the transcript inline session block, unified header capsule, footer dock, and left-rail cues remain coherent on the same selected-thread authority path.
8. Confirm thread switch clears old-thread autonomy ownership immediately.
9. Confirm reconnect downgrade, polling fallback, terminal resolution, and deselection visibly downgrade or clear selected-thread autonomy state with no stale retention.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first, single-owner, and free of goals-poll autonomy ownership while the session is active.
