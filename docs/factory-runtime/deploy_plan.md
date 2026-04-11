# Factory Runtime Deploy Plan

## Iteration 193

This deploy plan validates the healthy selected-thread transcript-tail session path as one continuous live session surface.

## Deployment Impact

This iteration keeps transport and selected-thread ownership unchanged while validating that the healthy SSE-owned path updates one transcript-tail live session block in place and suppresses duplicate selected-thread session-event cards until the path degrades or loses authority.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through proposal, review, verify, ready, and applied progression.
5. Confirm the center transcript shows at most one compact transcript-tail live session block for the selected thread and that the block updates in place through `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, and `APPLIED`.
6. Confirm duplicate selected-thread session-event cards sourced from SSE do not appear while that healthy transcript-tail block is authoritative.
7. Confirm reconnect downgrade, polling fallback, restore-gap, deselection, switch, and terminal paths immediately restore or clear separate session-event visibility instead of leaving the healthy collapse active.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy path stays on one transcript-tail live session block with `data-live-session-duplicates="collapsed"` and no duplicate `.timeline-item.session-event[data-append-source="sse"]` entries.
