# Factory Runtime Deploy Plan

## Iteration 156

This deploy plan validates the selected-thread combined-phase-and-path header badge contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread center-header badge mapping and verification only. The bounded expectation is that the title row remains identity-first while the transcript and footer composer stay authoritative and the one compact header badge now communicates both phase and path state.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the conversation header shows only the selected-thread title plus one compact badge whose text combines phase and healthy SSE ownership.
5. Confirm reconnect downgrade, polling fallback, restore attach, and switching update that same badge text immediately without introducing any second header surface.
6. Confirm the transcript remains the primary live session surface and the footer and rail stay aligned with the same selected-thread datasets.
7. Confirm the secondary panel still opens as a compact facts drawer and does not regain a primary-looking execution strip.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible single-badge combined-phase-and-path contract succeeds through the intended selected-thread session path.
