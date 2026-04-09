# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, header phase chip, footer dock, and non-selected thread rendering intact, but adds one selected-thread transcript-tail live activity item sourced from the existing SSE-owned live-run state.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. While the selected thread progresses through proposal, review, verify, ready, auto-apply, or applied states, confirm one compact transcript-tail live activity item mirrors the current selected-thread phase and detail in place.
5. Confirm the tail item only appears for the selected conversation while selected-thread SSE is the active owner and that non-selected rows remain snapshot-only.
6. Confirm the tail item resolves cleanly when terminal state arrives and does not accumulate duplicate transcript-tail items across repeated rerenders.
7. Confirm transcript plus composer reachability and the existing jump-to-latest behavior do not regress on phone or desktop widths.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
