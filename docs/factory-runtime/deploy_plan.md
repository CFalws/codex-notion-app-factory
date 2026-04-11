# Factory Runtime Deploy Plan

## Iteration 154

This deploy plan validates the selected-thread secondary-panel detail-drawer contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread secondary-panel presentation and verification only. The bounded expectation is that the transcript and footer composer remain authoritative while the optional secondary panel exposes compact selected-thread facts and drill-down detail without looking like a parallel live dashboard.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the transcript remains the primary session surface while the secondary panel stays closed by default.
5. Open the secondary panel and confirm the compact facts header shows selected-thread scope, transport, phase, path, verifier, and blocker facts that match the healthy selected-thread session datasets.
6. Confirm the autonomy and execution cards remain visible only as detail drill-down content inside the panel and do not replace the transcript-native session surface.
7. Trigger reconnect downgrade, polling fallback, switch, restore, terminal idle, and deselection and confirm the panel facts update or clear immediately without preserving stale selected-thread ownership.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible secondary-panel detail-drawer contract succeeds through the intended selected-thread session path.
