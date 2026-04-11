# Factory Runtime Deploy Plan

## Iteration 152

This deploy plan validates the left-rail sticky active-session row contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes left-rail sticky active-session presentation and verification only. The bounded expectation is that the row mirrors selected-thread owner, phase, and follow or unseen state directly from the selected-thread session contract while clearing immediately on degraded and switching paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the left rail shows exactly one sticky active-session row with `SSE OWNER`, the selected-thread phase, and `LIVE`, `NEW`, or `PAUSED` follow cues that match the selected-thread workspace.
5. Trigger a bounded pending handoff and confirm the same row flips to `HANDOFF` without making any non-selected thread look live-owned.
6. Trigger reconnect downgrade, polling fallback, terminal idle, deselection, and thread switch and confirm the row clears immediately instead of preserving stale selected-thread ownership.
7. Confirm no non-selected thread shows a sticky live-owned active-session row.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible rail-row contract succeeds through the intended selected-thread session path.
