# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live surface now follows the healthy SSE path, but the central session surface still collapses proposal, review, verify, ready, and apply progress into generic thinking or done language. The remaining friction is operator visibility: the runtime already emits phase-specific conversation events, but the active workspace does not expose them clearly enough where the user reads and types.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Leave submit handoff, polling fallback rules, and broader layout structure unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and composer-adjacent live rail, but promote proposal, review, verify, auto-apply, ready, and applied conversation events into one explicit live session-phase model so the active conversation shows the current phase directly inside the central workspace.
