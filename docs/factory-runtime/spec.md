# Factory Runtime Spec

## Iteration

- current iteration: `80`
- bounded focus: `left-rail active-session row continuity`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread session ownership, transcript-tail follow visibility, and center-pane switch continuity are now bounded, but the sticky left-rail active-session row still disappears during intentional switches, which forces the operator to infer continuity from the center pane alone.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership, session summary, follow, and thread-transition datasets.
- Keep the change bounded to `syncActiveSessionRow(...)`, the existing active-session row DOM and CSS, and the focused browser-proof verifier.
- Keep the row visible for the healthy selected thread and for exactly one bounded switching target during intentional switches.
- Clear stale old-thread ownership immediately by switching the row to non-owned transition state instead of reusing `OWNER` copy.
- Hide the row on reconnect downgrade, polling fallback, terminal idle, and true no-conversation idle.
- Keep all non-selected conversation rows snapshot-only and do not introduce new transport or side surfaces.

## Deliverable

Keep the sticky left-rail active-session row alive through healthy selected-thread runs and intentional switches so it mirrors `OWNER` plus phase and follow state on the healthy SSE path, then retargets to one non-owned `SWITCHING` row for the pending conversation until attach or degrade resolves it.
