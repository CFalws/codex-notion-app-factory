# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, footer dock, center-pane header, and rail markers intact, but tightens selected-thread transcript follow behavior and reuses the existing jump-to-latest affordance without widening transport scope.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and scroll up in a selected live thread while new SSE appends arrive.
4. Confirm the transcript stops auto-following when the reader has scrolled away, and that the jump-to-latest control only appears once unseen live content has arrived off-screen.
5. Confirm using the jump control or re-engaging the active composer returns to the newest append and restores follow mode without affecting transcript and footer composer accessibility.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
