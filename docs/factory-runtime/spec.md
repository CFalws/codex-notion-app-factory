# Factory Runtime Spec

## Iteration

- current iteration: `100`
- bounded focus: `single live-owned center-pane session surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread restore stage is now canonical, but healthy selected-thread SSE progress still keeps a duplicate composer-adjacent session strip visible above the fixed composer. That leaves the center pane reading like two competing live session surfaces instead of one conversation-first session timeline.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session-status, live-autonomy, phase-progression, restore-stage, and handoff helpers in the frontend store.
- Do not introduce a new transport or a new polling contract.
- Keep exactly one live-owned center-pane session surface during healthy selected-thread SSE progress.
- Preserve the bottom-fixed composer, restore stage, thread-switch clearing, degraded reconnect or polling markers, and rail behavior already established in earlier iterations.
- Do not suppress `/api/jobs` or `/api/goals` polling in this iteration; only remove duplicate healthy live-owned presentation in the center pane.

## Deliverable

Define and verify one conversation-first selected-thread live surface by keeping the transcript-tail live activity item as the only healthy SSE-owned session surface, while the composer-adjacent strip hides during that healthy path and remains available only for restore, handoff, switching, reconnect, or polling fallback.
