# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path and a conversation-first center pane, but thread selection still costs too much. The remaining friction is in the left rail: users should be able to identify the active thread, distinguish live versus idle state, and see one bounded recent preview before opening a conversation.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only left-rail conversation-card work on top of the existing selected-thread state path.
- Leave the selected-thread timeline, center-pane header, footer rail, submit handoff, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but make the left rail clearer by exposing one bounded recent preview line and a compact clearer state label per conversation card, while keeping selected-thread live precedence tied only to the existing selected-thread state path.
