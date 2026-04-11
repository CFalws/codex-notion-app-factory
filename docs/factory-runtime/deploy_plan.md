# Factory Runtime Deploy Plan

## Iteration 179

This deploy plan validates the healthy selected-thread header session row as the primary readable header-level session surface.

## Deployment Impact

This iteration keeps transport and healthy live ownership unchanged while turning the existing header summary seam into one authoritative healthy-path row for scope, path, ownership, and phase.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation with internal append SSE enabled and confirm the header shows exactly one compact chip-first summary row with scope, path, ownership, and phase.
5. Confirm the old phase badge is hidden on that healthy path, and the side-panel facts do not become a competing healthy summary surface.
6. Confirm reconnect downgrade, polling fallback, restore-gap, deselection, switch, and terminal completion immediately hide or neutralize the header summary row and return authority to the fallback badge path.
7. Confirm non-selected threads and no-selection idle do not leave stale header summary ownership behind.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy selected-thread path shows one authoritative header row while degraded and ambiguous paths clear it immediately.
