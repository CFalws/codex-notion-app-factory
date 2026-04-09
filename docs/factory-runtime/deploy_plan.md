# Factory Runtime Deploy Plan

## Deployment Impact

This still changes only the static Codex Ops Console assets plus the app-scoped delivery docs. Backend runtime behavior is unchanged, so the visible UX change takes effect after proposal apply and the normal GitHub Pages/static asset publish path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Publish the updated static site through the existing GitHub Pages flow so the deployed console reflects the chat-first layout.
3. Validate from both phone and desktop that conversation switching is easier than before, drafts still persist, and `Ctrl/Cmd + Enter` still sends without breaking the current lane.
