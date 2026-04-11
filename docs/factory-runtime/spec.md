# Factory Runtime Spec

## Iteration

- current iteration: `175`
- bounded focus: `make the sticky active-session row the single healthy navigation mirror for the selected thread`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center pane now has one authoritative healthy live session surface, but the left rail still duplicates selected-thread live ownership through both the sticky active-session row and the selected-card helper row. That overlap keeps the navigation layer noisier than the already-authoritative center pane.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the left rail to make the current live session obvious at a glance without multiple selected-row helper surfaces competing for attention.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the left navigation presentation seam in the operator console.
- Reuse the existing selected-thread SSE and `session_status` authority; do not add a new navigation state source.
- Promote the sticky active-session row as the only healthy navigation-level mirror for the selected thread.
- Suppress selected-card helper live detail when that sticky row is authoritative.
- Fail closed on degraded, restore-gap, deselected, switched, and no-selection states.

## Deliverable

Expose one obvious healthy sticky active-session row above the thread list as the canonical navigation mirror for the selected thread, while the selected card falls back to minimal chips and helper-style live detail stays suppressed on that same path.
