# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected conversation now has live append state and an inline run row, but the large autonomy summary card still sits at the top of the scrollable thread and delays immediate access to message history. That keeps the center pane feeling like a dashboard stack instead of a conversation-first workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Move autonomy blocker and verifier status out of the timeline body into a compact header-adjacent rail that preserves machine-readable state while leaving the central scroll region primarily for the conversation timeline plus composer.
