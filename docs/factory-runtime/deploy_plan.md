# Factory Runtime Deploy Plan

## Deployment Impact

This changes only the static Codex Ops Console assets plus the app-scoped delivery docs. Backend runtime behavior is unchanged, so the visible UX improvements appear after the proposal is applied and the GitHub Pages/static asset publish path runs normally.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Publish the updated static site through the existing GitHub Pages flow so the deployed console reflects the richer compose workspace.
3. Validate from both phone and desktop that drafts persist, quick prompts insert correctly, and `Ctrl/Cmd + Enter` sends a message without breaking the current conversation lane.
