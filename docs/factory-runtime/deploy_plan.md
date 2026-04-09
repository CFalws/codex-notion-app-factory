# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, footer dock, center-pane header, and rail markers intact, but compresses the selected-thread live strip into one inline activity bar instead of a split explanatory layout.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and inspect the selected-thread live bar while a selected conversation is healthy, reconnecting, proposal-ready, or terminal.
4. Confirm the active workspace shows transport, phase, proposal readiness, provenance, and compact action cues in one inline composer-adjacent surface without a split explanatory strip.
5. Confirm transcript plus composer accessibility do not regress on phone or desktop widths and that deeper operator detail remains in the secondary panel.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
