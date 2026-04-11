# Factory Runtime Spec

## Iteration

- current iteration: `104`
- bounded focus: `selected-thread follow control absorbed into the footer dock`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread restore stage, healthy live surface, autonomy authority, switch continuity, and timeline milestones are now canonical, but the detached follow or unseen-state affordance still lives as a separate transcript-level control. The remaining gap is to absorb that follow surface into the existing footer dock so the active conversation ends with one unified session footer beside the composer.

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
- Reuse the existing selected-thread SSE ownership and follow datasets instead of introducing another follow model.
- Keep degraded, reconnect, restore, and polling provenance explicit instead of letting them resemble healthy session ownership.
- Remove transcript-level follow duplication on the healthy path by moving detached NEW or PAUSED state into the footer dock.

## Deliverable

Define and verify one selected-thread footer-follow contract where healthy SSE-owned detached follow state appears only in the composer-adjacent footer strip with compact NEW or PAUSED context and unseen-count metadata, while degraded and fallback paths clear or downgrade that footer ownership immediately.
