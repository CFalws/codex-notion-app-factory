# Factory Runtime Deploy Plan

## Iteration 204

This deploy plan validates the selected-thread center timeline as an explicit healthy-path autonomy progression lane.

## Deployment Impact

This iteration keeps transport and ownership unchanged while making the healthy selected-thread milestone lane explicit. The healthy path should now expose `AUTO APPLY` as its own visible progression state between `VERIFY` and `READY`.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm the healthy selected-thread center timeline shows one explicit milestone lane with visible `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED` chips.
6. Confirm `AUTO APPLY` appears as its own active milestone when the corresponding SSE phase is emitted and no longer masquerades as `READY`.
7. Confirm reconnect downgrade, polling fallback, switch, deselection, restore-gap loss, and terminal completion still downgrade or clear the timeline lane in the same frame rather than leaving stale active milestones behind.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy path passes only when the explicit milestone lane is present and non-healthy transitions clear or downgrade it immediately.
