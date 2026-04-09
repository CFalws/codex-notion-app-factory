# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It introduces a desktop secondary panel for nonessential operator content while leaving the selected-conversation live path, mobile drawer behavior, and phone footer dock intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on desktop width and confirm the thread rail remains continuously visible while the transcript and composer dominate the center pane.
4. Verify workspace summary, execution logs, and learning content are collapsed behind the secondary panel by default and no longer compete with the main conversation pane.
5. Open and close the secondary panel from the thread header and confirm the center conversation view remains intact.
6. On phone width, confirm the existing mobile drawer and sticky footer dock still behave unchanged.
7. Confirm the session strip still updates through connecting, live, reconnecting, idle collapse, and terminal collapse using the selected-conversation live path.
