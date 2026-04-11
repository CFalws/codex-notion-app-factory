# Factory Runtime Spec

## Iteration

- current iteration: `144`
- bounded focus: `add one compact selected-thread header ownership indicator derived from existing session status without creating a second authority surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Iteration 143 made the center timeline the sole authority-looking selected-thread session surface, but the header still leaves operators inferring whether the selected conversation is SSE-owned, reconnecting, polling, or restoring. That ownership state exists already, but it is not exposed as one compact secondary indicator in the header.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the selected conversation header to show current session ownership at a glance without competing with the timeline.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration presentation-only in the render layer plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, or composer ownership rules.
- Keep the center timeline as the only authority-looking live session surface.
- Reuse the existing selected-thread session status, timeline authority, and degraded-path rules.
- Clear the header indicator immediately on switch and terminal idle.

## Deliverable

Expose one compact selected-thread header ownership indicator derived from existing session status so healthy SSE, reconnect, polling fallback, and restore states are visible at a glance while the timeline remains the sole selected-thread authority surface.
