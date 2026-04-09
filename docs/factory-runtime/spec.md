# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace now has a stronger conversation-first shell and unified composer-adjacent activity bar, but the send handoff still feels like a request-submit pause because nothing lands in the transcript until the round trip returns. The remaining friction is the gap between composer submit and the first accepted or live conversation signal.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Render one temporary pending outbound user message inside the active timeline at submit time and keep the composer-adjacent activity bar in a short sending-to-live handoff state until the first accepted or live signal arrives, without changing transport or adding new status surfaces.
