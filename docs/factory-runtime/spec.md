# Factory Runtime Spec

## Iteration

- current iteration: `95`
- bounded focus: `single selected-thread center-lane session surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread session ownership and phase progression are now canonical, but the operator still reads one active session through multiple live-owned center-lane surfaces. The header, inline block, transcript card, and composer-adjacent strip still duplicate ownership cues enough to make the session feel split instead of conversation-first.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session-status, live-autonomy, and phase-progression helpers in the frontend store.
- Reuse existing append-stream, pending-handoff, session-phase, autonomy summary, and thread-transition state; do not introduce a new transport or a new polling contract.
- Keep exactly one live-owned selected-thread session block in the center lane during handoff or healthy SSE progress.
- Preserve the bottom-fixed composer, thread-switch clearing, degraded reconnect or polling markers, and rail behavior already established in earlier iterations.
- Do not suppress `/api/jobs` or `/api/goals` polling in this iteration; only collapse duplicate live-owned presentation in the selected-thread workspace.

## Deliverable

Define and verify one primary selected-thread session surface in the center lane by reusing the existing canonical helpers, demoting the header and composer strip to compact supporting context, and preserving explicit degraded or cleared markers without transport or polling changes.
