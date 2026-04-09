# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It adds transcript-local live follow behavior and a compact jump-to-latest control while leaving the selected-conversation live path, navigation structure, transcript handoff states, composer-adjacent activity bar, desktop secondary panel, phone footer dock, and thread rail markers intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console with an active generating conversation and confirm new live appends stay visible while the user is already near the bottom.
4. Scroll upward during generation and verify forced scrolling stops, the reading position is preserved, and a compact jump-to-latest control appears.
5. Use the jump control and confirm it returns the transcript to the newest append and resumes follow mode.
6. Switch threads or wait for an empty or terminal reset and confirm the jump affordance clears.
7. Confirm the composer-adjacent activity bar remains the only visible live-status surface inside the conversation pane.
