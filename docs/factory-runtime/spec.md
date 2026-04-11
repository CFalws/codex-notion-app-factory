# Factory Runtime Spec

## Iteration

- current iteration: `161`
- bounded focus: `preserve selected-thread session continuity during intentional thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center workspace already has a canonical selected-thread live strip, but intentional thread switches can still feel like a reset unless the old thread is cleared immediately and the shell stays mounted behind one bounded transition placeholder.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting intentional thread switches to feel like one continuous selected-thread session shell rather than a generic empty reset.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to selected-thread switch handling in the center conversation workspace and its existing ownership state.
- Do not change transport scope, transcript append ownership, composer docking, footer ownership rules, rail mirroring, or secondary-panel behavior.
- Preserve the center conversation shell and bottom composer during intentional switches.
- Replace generic empty-state fallback with exactly one compact selected-thread transition placeholder until the new snapshot attaches.
- Clear stale selected-thread ownership immediately on switch, terminal completion, deselection, or thread loss of authority.
- Keep reconnect and polling fallback from reclaiming primary selected-thread ownership during or after a switch.
- Never make a non-selected thread appear live-owned.

## Deliverable

Keep the selected-thread conversation shell mounted during intentional switches, clear old-thread ownership immediately, and expose exactly one compact transition placeholder until the new thread snapshot attaches.
