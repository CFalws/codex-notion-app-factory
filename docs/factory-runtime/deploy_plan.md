# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that selected-thread downgrade transitions now stay visible inside the center timeline through one compact degraded-session marker while healthy ownership and degraded fallback behavior remain unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an app that has a healthy selected-thread live session.
4. Force a reconnect, polling fallback, session rotation, or ownership-loss transition on the selected thread and confirm the center timeline shows exactly one compact degraded-session marker with explicit path or reason attribution.
5. Confirm the degraded marker clears immediately on healthy reattach, idle, terminal completion, or thread switch, and that no stale healthy owner chips remain in the timeline block.
6. Confirm non-selected threads remain snapshot-only and never receive the degraded marker.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the degraded-session marker contract passes through the intended selected-thread surface.
