# Factory Runtime Spec

## Iteration

- current iteration: `164`
- bounded focus: `mirror the selected-thread live session onto the selected left-rail conversation row`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center-pane session surfaces are stronger now, but the selected conversation row in the left rail still looks snapshot-only. Operators still need to infer which thread is actively live instead of reading it directly from the navigator.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the left rail and center pane to agree immediately about which selected thread is actively alive.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected conversation-row mirror in the left rail.
- Do not change transport scope, transcript message ownership, composer docking, recent-thread rail behavior, footer ownership rules, or secondary-panel behavior.
- Keep the selected-row live marker single-instance and fail closed on switch, deselection, terminal completion, reconnect downgrade, polling fallback, or lost authority.
- Do not let non-selected rows appear live-owned.

## Deliverable

Render one compact chip-first selected-row live marker plus bounded cue on the selected conversation row only, sourced from the existing selected-thread canonical session and follow state, with immediate fail-closed clearing on degraded or switched paths.
