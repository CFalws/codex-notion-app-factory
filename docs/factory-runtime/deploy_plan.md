# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes only the frontend render ownership boundary for the existing conversation-first workspace. The bounded expectation is that healthy selected-thread execution visibility is readable from the center conversation surface, while the secondary execution-status panel only participates on degraded or non-owned paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Open an existing selected thread on the healthy attach path and confirm the transcript plus session strip expose the current phase without opening the secondary panel.
5. Confirm the secondary execution-status card is hidden and marked `center-lane` while the selected thread remains on the healthy SSE-owned path.
6. Submit a message from the fixed composer and confirm proposal, review, verify, ready, and applied progress remain readable from the central conversation surface without `/api/jobs/{id}` polling.
7. Force reconnect downgrade or fallback and confirm the secondary execution-status card reappears as `secondary-detail` only after the downgrade is visible and explicit.
8. Confirm intentional thread switch still preserves the mounted shell and composer while avoiding stale live execution ownership.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread session succeeds through the intended central-surface ownership path.
