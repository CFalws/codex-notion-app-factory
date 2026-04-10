# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the left thread rail now exposes a single sticky active-session row for the intended selected-thread live path, without letting degraded or switched-away paths linger as if they were still live-owned.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an app that has a healthy selected-thread live session.
4. Confirm the left rail shows exactly one sticky active-session row above the conversation list when the selected thread is handoff, live-following, paused, has unseen appends, or is intentionally switching.
5. Confirm the row publishes the expected owner, phase, follow, source, and unseen-count cues and still leaves non-selected rows snapshot-only.
6. Confirm idle, terminal, reconnect downgrade, polling fallback, ownership loss, or switched-away paths clear the sticky row immediately.
7. Confirm intentional attach keeps the sticky row visible only as `SWITCHING` or `ATTACH` until the new selected snapshot takes ownership.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the left-rail active-session contract passes through the intended selected-thread surface.
