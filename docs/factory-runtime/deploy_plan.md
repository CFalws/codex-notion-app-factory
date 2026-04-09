# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, header phase chip, transcript-tail live activity turn, and non-selected thread rendering intact, but adds one compact composer-adjacent live strip that appears only while selected-thread SSE is actively driving the current run.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. While the selected thread progresses through proposal, review, verify, or auto-apply states, confirm one compact composer-adjacent live strip appears immediately above the composer and mirrors the current selected-thread phase and detail in place.
5. Confirm the strip only appears for the selected conversation while selected-thread SSE is the active owner and that non-selected rows remain snapshot-only.
6. Confirm terminal resolution removes the strip cleanly so the transcript-tail activity item remains the only in-flow record and no stale composer-adjacent session chrome remains.
7. Confirm transcript plus composer reachability and the existing jump-to-latest behavior do not regress on phone or desktop widths.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
