# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The main workspace is already more conversation-first, but the active-pane header still carries dead status and autonomy chrome assumptions from earlier iterations. The remaining friction is header competition: the transcript should become the first readable surface under a minimal identity-only header, while fuller operator detail stays in the existing secondary panel.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the desktop active-pane header render layer and stale header-only support code.
- Leave the selected-thread timeline, live row, submit handoff, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path, left rail markers, and compact composer state row, but reduce the desktop active-thread header to identity and navigation only while removing stale duplicated header-status and autonomy render paths that no longer belong outside the secondary panel.
