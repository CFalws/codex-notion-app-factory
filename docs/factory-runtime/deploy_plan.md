# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on clearer snapshot labels and bounded preview text in the conversation list. The bounded expectation is that non-selected rows stay snapshot-only while waiting, active, ready, done, failed, and idle states remain easier to scan at a glance.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm non-selected conversation rows each show exactly one compact snapshot label and one bounded preview line.
5. Confirm recent assistant or user message content is preferred over event prose whenever message history exists.
6. Confirm event-only threads fall back to concise snapshot prose for waiting, active, proposal, review, verify, ready, done, and failed states instead of noisy raw event text.
7. Confirm selected-row live mirroring remains visually stronger than snapshot rows and non-selected rows never gain live-owner treatment.
8. Confirm desktop and phone widths keep the rail readable without adding new panels or displacing the conversation-first shell.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the rail snapshot-label and preview proof still passes without degraded-path signals.
