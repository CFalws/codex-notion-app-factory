# Factory Runtime Deploy Plan

## Iteration 155

This deploy plan validates the selected-thread single-badge header contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread center-header presentation and verification only. The bounded expectation is that the title row remains identity-first while the transcript and footer composer stay authoritative and the header exposes at most one compact live badge.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the conversation header shows only the selected-thread title plus one compact live phase badge, with no summary strip above the transcript.
5. Confirm the badge reflects healthy phase progression through the intended SSE-owned path and that the transcript remains the primary live session surface.
6. Trigger reconnect downgrade, polling fallback, switch, restore, terminal idle, and deselection and confirm the badge downgrades or clears immediately without preserving stale selected-thread ownership.
7. Confirm the secondary panel still opens as a compact facts drawer and does not regain a primary-looking execution strip.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible single-badge header contract succeeds through the intended selected-thread session path.
