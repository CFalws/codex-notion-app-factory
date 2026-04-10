# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already communicates live ownership clearly, but thread switching still has to preserve that workspace continuity. Users should stay attached to the same conversation shell and composer while a newly selected thread snapshot binds, rather than experiencing a generic reset or stale old-thread live state.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to selected-thread switching continuity in the center workspace.
- Keep the selected-thread SSE path, session strip ownership, bottom follow control, composer behavior, and side-panel behavior unchanged.
- Leave transport scope, selected-row live ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but make intentional thread switches stay inside the current workspace shell: clear old-thread live ownership immediately, keep the center header and composer dock visible, and render exactly one compact selected-thread transition placeholder until the new snapshot attaches instead of falling back to a generic empty-state reset.
