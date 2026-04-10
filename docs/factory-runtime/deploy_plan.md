# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes selected-thread switching semantics in the existing conversation-first workspace. The bounded expectation is that intentional thread switches keep the shell and composer mounted, show one switching placeholder, and explicitly clear phase ownership to non-authoritative `UNKNOWN` until the new selected thread attaches or degrades.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Click from one selected thread to another while the first thread is still visible and confirm the center pane never flashes the generic empty state.
5. Confirm exactly one `data-thread-transition="loading"` placeholder appears and carries `data-thread-transition-phase="switching"` until the target thread attaches or degrades.
6. Confirm the session strip stays mounted with `composerState=switching`, `composerTransport=attach`, and the target conversation id set to the new selected thread.
7. Confirm the session strip and thread scroller both expose `phaseValue=UNKNOWN`, `phaseAuthoritative=false`, and `phaseProvenance=thread-transition` during the switch.
8. Confirm old-thread live ownership clears immediately across the inline live block, active-session row, follow control, and thread scroller datasets.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch continuity contract passes on the intended path.
