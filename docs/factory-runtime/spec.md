# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live surface is stronger than before, but the desktop shell still reads too much like a dashboard with a competing side panel instead of a conversation-first session workspace. The remaining friction is layout hierarchy: the active thread does not dominate the screen strongly enough on desktop.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to desktop-width layout and shell hierarchy only.
- Leave the selected-thread timeline, live row, submit handoff, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and compact composer state row, but tighten the desktop shell into a strict two-pane workspace with a narrower persistent left rail, a dominant active conversation center pane, and a secondary panel that no longer behaves like a third primary column.
