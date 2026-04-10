# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace is already conversation-first in the center pane, but navigation still needs to communicate active session ownership at a glance. Users should be able to identify the active or in-flight selected thread directly from the left rail without scanning the center strip or opening the secondary panel.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to selected-row navigation rendering and selected-thread live-owner state mapping.
- Keep the selected-thread SSE path, session strip ownership, bottom follow control, composer behavior, and side-panel behavior unchanged.
- Leave transport scope, selected-row live ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but make the selected conversation row alone mirror the current selected-thread session owner state with one compact `HANDOFF`, `LIVE`, `NEW`, or `PAUSED` marker plus the existing follow or unread cue. Non-selected rows remain snapshot-only and clear any live-owned treatment immediately on thread switch, reconnect downgrade, polling fallback, or terminal resolution.
