# Factory Runtime Spec

## Iteration

- current iteration: `181`
- bounded focus: `keep the selected-thread conversation shell and composer mounted through intentional switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread path is already conversation-first, but the switch boundary is where continuity is still easiest to misread. If the workspace flashes generic empty state or leaves stale old-thread ownership behind during attach, the operator has to infer whether the session is still live.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting intentional thread switches to feel like one continuous live session instead of a drop to idle.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to selected-thread switch state mapping and rendering over the existing selected-thread authority model in the operator console.
- Reuse the existing selected-thread SSE and session model already driving workspace placeholder, transition, and composer surfaces; do not change transport ownership rules.
- Keep the transcript shell and bottom-fixed composer mounted during intentional thread switches.
- Render exactly one compact switching placeholder while the incoming selected thread snapshot attaches.
- Fail closed on degraded, reconnect, polling fallback, restore-gap, deselected, switched, and no-selection states.

## Deliverable

Expose one continuous conversation-first switch path where old-thread live ownership clears immediately, the generic empty workspace never flashes during intentional switches, and the incoming selected thread stays visible through one compact transition placeholder until attach completes.
