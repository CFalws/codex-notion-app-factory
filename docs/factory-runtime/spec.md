# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The desktop layout is now materially conversation-first, but thread navigation still requires the user to infer which conversation is actively generating by reading the center pane or opening secondary status surfaces. The remaining friction is navigation ambiguity, not transport or layout ownership.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Add compact selected-thread and live-run markers directly into the existing left rail so the user can identify the active and currently generating conversation from navigation alone, while keeping the center pane, footer dock, and secondary panel behavior unchanged.
