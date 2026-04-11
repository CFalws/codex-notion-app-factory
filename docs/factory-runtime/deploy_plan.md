# Factory Runtime Deploy Plan

## Iteration 200

This deploy plan validates the healthy selected-thread center transcript as one authoritative live session-progress surface.

## Deployment Impact

This iteration keeps transport and selected-thread ownership unchanged while validating that the healthy SSE-owned path keeps exactly one authoritative live session-progress item in the center transcript and suppresses duplicate SSE session-event cards until authority is lost.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm the center transcript shows exactly one authoritative live session-progress item for the selected thread and that it updates in place through those phases.
6. Confirm duplicate `.timeline-item.session-event[data-append-source="sse"]` entries do not remain visible while that primary live item is authoritative.
7. Confirm reconnect downgrade, polling fallback, switch, deselection, restore-gap, and terminal completion clear or fail open immediately instead of leaving stale authoritative residue behind.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy path passes only when there is one primary live session item, collapsed duplicate session events, and no stale authoritative residue on non-healthy transitions.
