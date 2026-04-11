# Factory Runtime Spec

## Iteration

- current iteration: `110`
- bounded focus: `selected-thread SSE phase progression appears as one compact in-timeline session event lane`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread ownership and switch continuity are now explicit, but proposal, review, verify, ready, and applied progress still live mostly in footer or rail context. The remaining gap is to project that healthy SSE-owned phase progression into the active conversation timeline itself as one compact in-place session event lane.

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
- Reuse the existing selected-thread phase progression and milestone helpers instead of inventing another transcript model.
- Keep the center conversation to at most one compact healthy selected-thread session event lane.
- Clear or downgrade that lane immediately on reconnect, polling fallback, restore-only, terminal idle, and thread switch paths.
- Keep non-selected threads from gaining healthy selected-thread session-event presentation.

## Deliverable

Define and verify one selected-thread transcript session-event lane contract where healthy SSE-owned proposal, review, verify, ready, and applied progression appears through one compact live timeline item with milestone datasets, while reconnect, polling, restore, empty, and switch paths clear or downgrade that lane immediately.
