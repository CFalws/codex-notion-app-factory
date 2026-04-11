# Factory Runtime Spec

## Iteration

- current iteration: `103`
- bounded focus: `selected-thread autonomy progression as one canonical timeline surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread restore stage, healthy live surface, autonomy authority, and switch continuity are now canonical, but bounded autonomy progress still reads as scattered status cues instead of one explicit session timeline progression. The remaining gap is to make proposal, review, verify, ready, and applied state first-class in the selected-thread timeline itself.

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
- Reuse the existing selected-thread SSE authority, autonomy, and phase-progression contract instead of adding another status source.
- Keep degraded, reconnect, restore, and polling provenance explicit instead of letting them resemble healthy session ownership.
- Suppress duplicate healthy-path autonomy or execution presentation outside the center timeline when the timeline already owns the session progression.

## Deliverable

Define and verify one selected-thread timeline progression contract where healthy SSE-owned proposal, review, verify, ready, and applied state appears in one canonical center-timeline surface, while degraded and fallback provenance remains explicit and non-healthy.
