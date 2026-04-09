# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace now shows the outbound handoff in the transcript, but the assistant side of the turn still stays visually silent until the first real response content arrives. The remaining friction is the empty gap between accepted submit and the first assistant append.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Render one temporary assistant placeholder in the active transcript after the local handoff is accepted, keep it until the first real assistant append or terminal failure, and clear it through the same selected-conversation state owner without adding new transport or status surfaces.
