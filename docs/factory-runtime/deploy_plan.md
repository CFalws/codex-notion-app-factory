# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, footer dock, and non-selected thread rendering intact, but makes the selected-thread header and composer-adjacent live rail show exact live phase progression with phase-specific detail copy.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths while a selected conversation progresses through proposal, review, verify, auto-apply, ready, or applied states if available.
4. Confirm the thread phase chip and composer-adjacent live rail both show the exact current phase instead of generic running wording, and confirm their visible updates remain attributable to selected-thread SSE.
5. Confirm non-selected rows remain snapshot-only and transcript plus composer accessibility do not regress on phone or desktop widths.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
