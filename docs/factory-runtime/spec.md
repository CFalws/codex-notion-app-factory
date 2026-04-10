# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected row in the left rail is more prominent now, but it still uses helper-style live detail text instead of a small finite session mirror. The rail should expose only the selected-thread owner state and follow state through compact chips so thread navigation feels session-native without adding another status surface.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE, handoff, and live-follow ownership model instead of widening transport scope.
- Constrain this iteration to the selected-thread left-rail render path.
- Keep the selected-thread SSE path, footer composer structure, side-panel behavior, and center-pane session chrome unchanged.
- Leave transport scope, runtime APIs, thread-switch behavior, and selected-row ownership semantics unchanged while making the rail mirror finite and chip-first.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but convert the selected row in the left rail into a compact live-session chip mirror: one owner chip plus one follow-state chip drawn only from existing selected-thread handoff, live, and follow datasets, with non-selected rows remaining snapshot-only.
