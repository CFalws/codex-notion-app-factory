# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace still reads too much like an operator console because deeper context lives in an always-present sidecar and the center pane still depends on prose-heavy summary copy. Even with the conversation shell anchored, the main workspace does not yet surface compact selected-thread context strongly enough on its own.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the selected-thread center workspace summary and optional side-panel behavior.
- Keep non-selected thread behavior and selected-thread SSE ownership unchanged.
- Leave selected-thread transport ownership, dock behavior, selected-row live ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but move the primary selected-thread context into one compact machine-readable header summary inside the center pane and leave the deeper operator context behind a collapsed-by-default secondary panel. The center workspace should explain selected-thread path and attach state without reintroducing a second live-status surface, while the secondary panel remains available only for deeper inspection.
