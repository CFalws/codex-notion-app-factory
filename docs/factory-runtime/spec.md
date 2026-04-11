# Factory Runtime Spec

## Iteration

- current iteration: `105`
- bounded focus: `selected-thread live session dock promoted beside the fixed composer`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread restore stage, healthy live surface, autonomy authority, switch continuity, timeline milestones, and footer-follow ownership are now canonical, but the composer-adjacent footer still does not own current run phase and proposal or review or verify or apply progress on the healthy path. The remaining gap is to promote that footer into the single selected-thread live session dock so the active conversation shows current execution state beside the fixed composer without scanning other surfaces.

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
- Reuse the existing selected-thread SSE ownership, phase, milestone, and follow datasets instead of introducing another state model.
- Keep degraded, reconnect, restore, and polling provenance explicit instead of letting them resemble healthy session ownership.
- Remove duplicate healthy selected-thread live-status surfaces when the footer dock owns the live session.

## Deliverable

Define and verify one selected-thread footer session-dock contract where healthy SSE-owned phase and proposal or review or verify or ready or applied progression appear in the composer-adjacent footer strip with compact milestone chips and follow metadata, while degraded and fallback paths clear or downgrade that footer ownership immediately.
