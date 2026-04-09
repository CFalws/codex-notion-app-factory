# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live rail now sits in the right place, but its current behavior is too binary: it expands during activity and then disappears on idle or terminal states. That forces users to infer the latest outcome from the transcript or reopen other UI instead of keeping one compact conversation-local result surface visible.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Keep the selected-conversation live rail attached to the composer, but make idle and terminal states collapse into a one-line last-result summary with an in-rail re-expand control. Running, thinking, sending, connecting, and reconnecting states must stay expanded and continue to use the existing selected-conversation SSE path as the only status source.
