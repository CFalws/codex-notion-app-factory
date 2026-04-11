# Factory Runtime Spec

## Iteration

- current iteration: `203`
- bounded focus: `promote the bottom-fixed composer into the single authoritative healthy selected-thread session bar`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace now has enough shared authority state to keep surfaces in sync, but the healthy path still distributes ownership cues across the header, rail chrome, and composer-adjacent surfaces. That weakens the “one live session” feel because the operator still has to scan multiple regions to confirm owner, phase, and current run state.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the fixed composer area to behave like the single live session control surface for the currently selected thread.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread composer bar, the shared selected-thread authority model, and the focused browser verification seam.
- Reuse the existing selected-thread SSE-owned authority datasets; do not change transport or add cross-thread session ownership.
- On the healthy selected-thread path, make the fixed composer strip the single authoritative session bar for owner, phase, and active run state.
- Suppress or clear duplicate healthy-path owner chrome outside that composer surface.
- Keep degraded, restore, switch, deselection, restore-gap loss, and terminal transitions fail-open or cleared immediately.

## Deliverable

Expose one conversation-first selected-thread workspace where the fixed composer bar is the canonical healthy selected-thread session surface and healthy ownership does not compete with header or rail chrome, while downgrade and clear transitions still happen in the same frame.
