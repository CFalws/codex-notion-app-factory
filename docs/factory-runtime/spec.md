# Factory Runtime Spec

## Iteration

- current iteration: `109`
- bounded focus: `selected-thread switch continuity keeps one compact switching workspace shell`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership is now explicit across the footer and rail, but intentional thread switches can still read like the workspace lost state because the center shell is driven through the generic null-conversation branch. The remaining gap is to keep the center shell and composer frame in place through one explicit switching placeholder until the new snapshot attaches.

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
- Reuse the existing selected-thread session-status and thread-transition state instead of adding another switch model.
- Keep the center pane and bottom-fixed composer mounted during intentional thread switches.
- Limit the center pane to one compact switching placeholder while the new thread attaches.
- Keep reconnect, polling fallback, terminal, restore, and true no-selection paths visibly distinct from intentional switching.

## Deliverable

Define and verify one selected-thread switch continuity contract where the center pane holds one compact `SWITCHING` workspace placeholder and the composer row mirrors that same target state until the new thread attaches, while true empty, restore, reconnect, polling, and terminal paths do not retain switching treatment.
