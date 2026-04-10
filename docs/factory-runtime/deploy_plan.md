# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-conversation SSE path. The bounded expectation is that the footer reads as a chat-first composer, with textarea plus send always dominant and apply plus auto-open moved behind one compact utility affordance, without changing live-strip ownership or secondary-panel scope.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the footer shows the textarea and primary send action as the dominant path on desktop and phone widths.
5. Open the compact footer utility affordance and confirm apply plus auto-open remain reachable without permanently occupying the footer.
6. Confirm the utility panel starts collapsed, closes cleanly after submit or apply, and does not push transcript history off screen on phone widths.
7. Confirm the session strip and bottom follow control remain the only live-progress surfaces.
8. Confirm non-selected rows continue to show only snapshot labels and bounded preview lines.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals, duplicate footer controls, or a re-expanded operator-form footer.
