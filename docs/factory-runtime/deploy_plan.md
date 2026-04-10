# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-conversation SSE path. The bounded expectation is that the transcript exposes one compact bottom follow control with explicit `NEW` vs `PAUSED` state and unseen-count metadata, without changing composer dock behavior, selected-row live-owner cues, or secondary-panel scope.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Keep the selected transcript near the bottom during healthy append delivery and confirm no paused marker appears while follow mode remains active.
5. Scroll away from the bottom, let new selected-thread SSE appends arrive, and confirm exactly one compact control appears with explicit `NEW` or `PAUSED` plus unseen-count metadata.
6. Use the control to jump back to the latest append and confirm it clears immediately while follow mode resumes.
7. Confirm the control also clears on thread switch, reconnect downgrade, polling-only fallback, and terminal completion without leaving stale markers in the rail or center pane.
8. Confirm non-selected rows continue to show only snapshot labels and bounded preview lines and never gain transcript follow controls.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals, stale live leakage, or follow-control ambiguity.
