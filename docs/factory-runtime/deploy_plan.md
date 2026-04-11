# Factory Runtime Deploy Plan

## Iteration 175

This deploy plan validates the sticky active-session row as the single healthy navigation-level mirror of the selected thread.

## Deployment Impact

This iteration keeps transport and healthy live ownership unchanged while making the left-rail sticky active-session row the only healthy navigation mirror and suppressing selected-card helper live detail on that same path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation with internal append SSE enabled and confirm the sticky active-session row above the thread list shows the selected thread’s owner, phase, and NEW or PAUSED follow cues immediately.
5. Confirm the selected conversation card does not show an extra live-owner helper row while the sticky row is authoritative, and only minimal selected chips remain.
6. Confirm reconnect downgrade, polling fallback, deselection, restore-gap, switch, and terminal completion clear or downgrade the sticky row immediately.
7. Confirm non-selected rows and recent-thread chips never look live-owned.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible left rail shows one canonical sticky active-session row on the healthy path and no duplicate selected-card helper mirror.
