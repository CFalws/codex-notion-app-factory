# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the selected-thread live session surface now exposes the latest autonomy verdict inline, so the operator does not have to open the secondary panel to understand the current iteration path and blocker state.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an app that has a relevant autonomy goal and an active selected-thread live session.
4. Confirm the selected-thread inline live session block shows iteration, intended-path verdict, verifier acceptability, and blocker reason without opening the secondary panel.
5. Confirm proposal, review, verify, ready, applied, and blocker signals stay synchronized with the same selected-thread live surface.
6. Confirm thread switch, reconnect, ownership-loss, polling fallback, or no-goal states clear the inline autonomy projection immediately.
7. Confirm non-selected threads stay snapshot-only and do not project autonomy verdicts into the main workspace.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the inline autonomy-visibility contract passes through the intended selected-thread surface.
