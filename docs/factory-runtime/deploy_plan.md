# Factory Runtime Deploy Plan

## Iteration 147

This deploy plan validates the unified selected-thread center-timeline live-session contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread center-timeline presentation and verification only. The bounded expectation is that healthy SSE session progression updates in the existing live activity block while duplicate selected-thread SSE session-event cards stay collapsed behind it.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run that moves through proposal, review, verify, ready, or apply milestones.
5. Confirm the center timeline shows exactly one `data-live-session-primary="true"` selected-thread live activity item and that its chips and detail copy update in place as the selected-thread phase progresses.
6. Confirm no `.timeline-item.session-event[data-append-source="sse"]` cards remain visible for the selected thread while that primary live activity block is present.
7. Trigger reconnect, polling fallback, restore, handoff, terminal clear, and thread switch and confirm the live activity downgrades or clears through the existing fail-closed rules instead of leaving stale selected-thread session-event cards behind.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible unified center-timeline contract succeeds through the intended selected-thread SSE path.
