# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, footer dock, center-pane header, and selected-row live-owner treatment intact, but refines non-selected rows so they show one stronger snapshot label and one more useful bounded preview line.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a mix of idle, review, verify, ready, done, and failed conversations if available.
4. Confirm the selected row still reads as the sole live-owned lane, while every non-selected row shows exactly one snapshot chip with the expected precedence and one bounded preview line that prefers recent message content.
5. Confirm non-selected rows remain snapshot-only and transcript plus composer accessibility do not regress on phone or desktop widths.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
