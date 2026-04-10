# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread handoff path is now compact and verified, but recent thread history is still mostly trapped in the left rail. On phone-sized layouts that means the operator has to leave the active transcript and composer to move between the current thread and nearby recent threads, which breaks the Codex-style session feel even when the live path itself is correct.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing conversation list payload, `threadTransition`, selected-thread SSE ownership, append-stream, and snapshot labels instead of widening transport scope.
- Constrain this iteration to a bounded quick-switch rail inside the center conversation workspace.
- Keep the left rail, runtime APIs, side-panel behavior, SSE transport, and selected-thread handoff path unchanged.
- Keep transcript and composer mounted during switches and ensure non-selected threads never retain live-owned treatment.

## Deliverable

Render one compact recent-thread quick-switch rail beneath the conversation header using a bounded set of existing conversation-list entries, let the operator jump directly between the selected thread and recent threads from the center pane, mirror selected and live-state cues with chip-only labels, and continue to clear stale live ownership immediately on switch, downgrade, or terminal completion.
