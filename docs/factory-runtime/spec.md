# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path and explicit live-rail stream health, but the left conversation rail still makes users re-open the thread to confirm which conversation owns the live session. The remaining friction is navigation awareness: the active or generating thread should be recognizable directly from the rail.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only left-rail session marker work on top of the existing selected-thread state path.
- Leave the selected-thread timeline, center-pane header, footer live rail, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but make the selected conversation row in the left rail carry one compact session marker for the active thread while keeping non-selected rows snapshot-only and preserving selected-thread ownership tied only to the existing selected-thread state path.
