# Factory Runtime Spec

## Iteration

- current iteration: `176`
- bounded focus: `keep the selected-thread conversation shell and bottom composer mounted through intentional thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership is already authoritative across the transcript, footer strip, and left rail, but the remaining high-friction gap is the thread-switch boundary. If the workspace looks briefly empty during an intentional switch, the operator has to infer whether the session is attaching to a new thread or has actually fallen back to idle.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the center conversation shell and fixed composer to stay continuous while the selected thread changes.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread switch presentation seam in the operator console.
- Reuse the existing selected-thread SSE, `session_status`, and thread-transition state; do not change transport ownership rules.
- Preserve the current transcript/composer frame during intentional switches instead of flashing the generic empty workspace.
- Keep exactly one compact transition placeholder visible until the incoming thread snapshot attaches.
- Fail closed on degraded, reconnect, polling fallback, restore-gap, deselected, switched, and no-selection states.

## Deliverable

Expose one continuous conversation-first workspace during intentional thread switches: keep the fixed composer dock mounted, clear old-thread live ownership immediately, and show one compact transition placeholder until the incoming selected-thread snapshot attaches.
