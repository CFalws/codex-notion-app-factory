# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace now has a stronger conversation-first shell and compact thread context, but current live execution state still feels split between the session strip and the composer footer region. The remaining friction is a fragmented active-session surface inside the composer area, not transport or layout ownership.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Unify the selected-thread live session strip and footer status into one compact composer-adjacent activity bar in the center conversation pane, while keeping the left rail, collapsed secondary panel, selected-conversation SSE path, and mobile drawer behavior unchanged.
