# Factory Runtime Spec

## Iteration

- current iteration: `96`
- bounded focus: `transcript-tail selected-thread live session item`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread session ownership, phase progression, and compact context are now canonical, but the active session still arrives through a separate center-lane live block instead of reading as the tail of the conversation itself. That leaves a final gap between prior transcript history and the currently generating session.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session-status, live-autonomy, and phase-progression helpers in the frontend store.
- Reuse existing append-stream, pending-handoff, session-phase, autonomy summary, and thread-transition state; do not introduce a new transport or a new polling contract.
- Keep exactly one live session surface in the transcript timeline during handoff, healthy SSE progress, or degraded reconnect or polling states.
- Preserve the bottom-fixed composer, thread-switch clearing, degraded reconnect or polling markers, and rail behavior already established in earlier iterations.
- Do not suppress `/api/jobs` or `/api/goals` polling in this iteration; only collapse duplicate live-owned presentation in the selected-thread workspace.

## Deliverable

Define and verify one primary selected-thread session surface as a transcript-tail live timeline item by reusing the existing canonical helpers, retiring the separate inline live block as an owning surface, and preserving explicit degraded or cleared markers without transport or polling changes.
