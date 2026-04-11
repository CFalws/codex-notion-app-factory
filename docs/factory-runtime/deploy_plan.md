# Factory Runtime Deploy Plan

## Iteration 209

This deploy plan validates the compact default-closed composer utility affordance and its clean separation from the healthy live strip.

## Deployment Impact

This iteration keeps transport and ownership unchanged while tightening bottom composer ergonomics. The healthy selected-thread path should keep the live strip as the only live owner surface while the utility cluster stays collapsed by default and closes whenever healthy ownership is lost.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm the healthy selected-thread bottom area shows the compact live strip above a chat-first composer and that apply and auto-open are reachable only through the compact utility affordance.
6. Confirm the utility is collapsed by default and exposes explicit machine-readable open or closed state.
7. Confirm send, selected-thread switch, reconnect downgrade, polling fallback, app change, and terminal idle all leave the utility closed and do not leak stale old-thread or degraded-state cues into the cluster.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy path passes only when the live strip remains the only healthy-path live owner surface and the utility stays compact and closed outside explicit user interaction.
