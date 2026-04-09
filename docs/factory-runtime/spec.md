# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace now has a stronger realtime handoff inside the transcript, but the active-thread header still duplicates live and autonomy status above the conversation. The remaining friction is top-of-pane dashboard chrome that competes with the transcript instead of letting the thread begin immediately.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Reduce the active-thread header to conversation identity and navigation only, remove duplicated live and autonomy status from above the timeline, and keep deeper state in the existing composer-adjacent activity bar, left-rail markers, and secondary panel.
