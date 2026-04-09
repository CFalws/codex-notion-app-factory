# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, footer dock, center-pane header, and rail markers intact, but compresses the composer so send stays primary while proposal apply and auto-open move into a compact utility cluster.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and inspect the selected-thread composer while proposal apply is available.
4. Confirm the textarea and primary send action dominate the footer and that proposal apply plus auto-open read as a compact secondary cluster rather than peer primary controls.
5. Confirm proposal apply remains reachable and transcript plus composer accessibility do not regress on phone or desktop widths.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
