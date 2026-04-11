# Factory Runtime Spec

## Iteration

- current iteration: `166`
- bounded focus: `preserve the selected-thread conversation shell and composer dock through intentional thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread switch path still risks feeling like a reset instead of one continuous live workspace. Operators should keep the center shell and bottom composer dock in place while old-thread ownership clears and the next snapshot attaches.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting thread switches to preserve the live session shell instead of flashing through a generic empty reset.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread switch path in the center workspace shell.
- Do not change transport scope, transcript message ownership, or introduce new multi-thread live ownership surfaces.
- Preserve the bottom-fixed composer dock and fail-closed clear old-thread ownership immediately on switch, cancellation, deselection, terminal completion, reconnect downgrade, polling fallback, or lost authority.
- Keep exactly one compact selected-thread transition placeholder visible during intentional switches and fall back to the generic empty view only for true no-selection idle.

## Deliverable

Keep the selected-thread conversation shell mounted during intentional switches, replace the generic empty reset with one compact transition placeholder, and keep the composer dock visible until the target snapshot attaches or the switch is truly cleared.
