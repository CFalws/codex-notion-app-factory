# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, footer dock, and non-selected thread rendering intact, but makes phone navigation behave more like a deliberate conversation drawer and returns focus to the selected conversation surface after drawer actions.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and confirm the active conversation with its composer dock is the default visible phone surface before navigation is opened.
4. On phone widths, open the nav sheet and confirm the conversation list is the first actionable surface while app or operator controls remain behind the collapsed secondary section.
5. Select a thread and an app from the phone drawer and confirm each action closes the drawer and returns focus to the selected conversation surface instead of leaving the user in navigation chrome.
6. Confirm non-selected rows remain snapshot-only and transcript plus composer accessibility do not regress on phone or desktop widths.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
