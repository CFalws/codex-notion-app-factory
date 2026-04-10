# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The rail is clearer now, but users can still lose live-session context when they scroll upward inside the selected transcript. The workspace needs one compact bottom follow control that makes detached-from-live state obvious and lets the operator return to the latest selected-thread output in one tap without opening any side panel.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to one selected-thread transcript follow control.
- Keep non-selected thread behavior snapshot-only.
- Leave selected-thread transport ownership, the rail behavior, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and overall shell ownership, but turn the bottom transcript follow affordance into one explicit conversation-local control that shows `NEW` for healthy off-screen SSE appends, `PAUSED` for degraded detached state, and clears immediately when the user jumps back to latest or re-engages the composer.
