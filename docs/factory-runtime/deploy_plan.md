# Factory Runtime Deploy Plan

## Deployment Impact

This changes only the static Codex Ops Console assets and request documentation. No runtime service restart or backend migration is required.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Publish the updated static site through the existing GitHub Pages flow if the deployed console should reflect the fixed URL immediately.
3. Validate from a phone that the console auto-loads app lanes without asking for a backend URL.
