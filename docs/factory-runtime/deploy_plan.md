# Factory Runtime Deploy Plan

## Iteration 125

This deploy plan validates the left-rail selected-thread compaction contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes left-rail render composition only. The bounded expectation is that the sticky active-session row remains the only live-owned rail mirror, while the selected conversation card and recent-thread chip stop presenting helper-style owner or follow detail.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the sticky active-session row appears above the conversation list with owner, phase, and follow cues.
5. Confirm the selected conversation card shows only compact chips plus snapshot preview, without helper-style live owner or follow prose, and confirm the recent-thread chip remains snapshot-only.
6. Trigger switching, reconnect downgrade, polling fallback, deselection, and terminal resolution and confirm the sticky active-session row clears in the same render cycle without stale rail ownership.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible left-rail compaction contract succeeds through the intended path.
