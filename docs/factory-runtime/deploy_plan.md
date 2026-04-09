# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It tightens the phone-width conversation-first layout by making navigation an explicit drawer or sheet while keeping the selected-conversation SSE path, transcript follow behavior, phone footer dock, and composer-adjacent live rail intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on phone width and confirm the active conversation is visible before navigation is opened.
4. Verify the mobile nav toggle explicitly opens the drawer or sheet, updates its expanded state, and does not leave the nav stack occupying the top reading flow by default.
5. Verify thread switching remains one explicit action away and app-level controls stay behind the collapsed operator section.
6. Confirm the live rail and composer remain in the active conversation workspace while navigation is closed.
7. Confirm the composer-adjacent live rail remains the only visible in-pane live-status surface inside the conversation pane.
