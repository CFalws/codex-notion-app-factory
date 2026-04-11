# Factory Runtime Spec

## Iteration

- current iteration: `102`
- bounded focus: `selected-thread switch continuity through one transition owner`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread restore stage, healthy live surface, and autonomy authority are now canonical, but the intentional thread-switch moment can still look split across surfaces. The remaining UX gap is that switching still relies on mixed cues instead of one explicit transition owner across the center pane and fixed composer.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session-status, live-autonomy, phase-progression, restore-stage, and handoff helpers in the frontend store.
- Do not introduce a new transport or a new polling contract.
- Keep exactly one live-owned center-pane session surface during healthy selected-thread SSE progress.
- Preserve the bottom-fixed composer, restore stage, thread-switch clearing, degraded reconnect or polling markers, and rail behavior already established in earlier iterations.
- Do not change transport contracts or add new polling behavior in this iteration.
- Keep the center conversation shell and bottom-fixed composer mounted during intentional thread changes.
- Clear stale old-thread live or polling-owned markers immediately when thread transition starts.
- Let the thread transition state own switch presentation instead of introducing separate switching mirrors elsewhere.

## Deliverable

Define and verify one selected-thread switch continuity contract where intentional thread changes keep one compact switching placeholder in the center pane, one switching composer target state, no generic empty-state flash, and immediate clearing of old-thread ownership until the new thread snapshot or SSE attach becomes authoritative.
