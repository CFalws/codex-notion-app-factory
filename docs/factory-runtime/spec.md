# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace now has stronger phone-width navigation and a tighter active pane, but the transcript still behaves like a static log during live generation. The remaining friction is that users can lose the newest SSE append when they are not pinned to the bottom, and there is no compact return-to-latest affordance when they intentionally scroll away.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Add conversation-local live-follow behavior so the selected transcript stays pinned to the newest append while the user is already near the bottom, preserves manual reading position when they scroll up, and shows one compact jump-to-latest control that restores the newest append without changing the existing SSE, composer, or navigation structure.
