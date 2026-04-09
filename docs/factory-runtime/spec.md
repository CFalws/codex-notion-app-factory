# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace now has a stronger conversation-first shell, but a standalone autonomy summary still sits above the transcript in the center pane. The remaining friction is dashboard-style context occupying the main reading path instead of letting the active thread own the viewport.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Replace the standalone center-pane autonomy block with a compact active-thread context strip in the thread header, and move the fuller autonomy detail into the secondary panel while keeping the selected-conversation session strip, footer dock, thread rail markers, and mobile drawer behavior unchanged.
