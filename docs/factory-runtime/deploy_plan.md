# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It keeps the selected-conversation SSE path, transcript follow behavior, footer dock, and composer-adjacent live rail intact, but upgrades the live rail from generic run wording to explicit proposal, review, verify, auto-apply, ready, and applied session phases.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open an active conversation on desktop and phone widths and trigger proposal, review, verify, proposal-ready, and apply-relevant events through the healthy selected-thread SSE path.
4. Verify the composer-adjacent live rail shows explicit `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, `AUTO APPLY`, and `APPLIED` phases instead of generic thinking or done wording.
5. Confirm the phase label updates immediately on thread switch and never implies live state for non-selected conversations.
6. Confirm the transcript-plus-bottom-composer layout remains unchanged and the live rail remains the only visible in-pane live-status surface inside the conversation pane.
7. Confirm polling only appears as degraded fallback when the append stream is absent or interrupted.
