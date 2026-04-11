# Factory Runtime Spec

## Iteration

- current iteration: `106`
- bounded focus: `healthy selected-thread transcript session cards collapsed into one live session item`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread footer dock now owns healthy current execution state, but the transcript still fragments one healthy selected-thread run into multiple session-status cards. The remaining gap is to collapse those duplicate healthy SSE authority cards so the active conversation reads as one realtime session timeline instead of repeated phase/status events.

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
- Remove duplicate healthy selected-thread transcript status cards when the live session is already represented by the healthy footer dock and live item.

## Deliverable

Define and verify one selected-thread transcript-collapse contract where healthy SSE-owned authority events no longer append duplicate session-status cards when the live session is already represented elsewhere, while degraded, restore, reconnect, switching, failure, ready, and applied evidence remain explicit when they are no longer healthy live-owned.
