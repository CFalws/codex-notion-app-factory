# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The left rail still gives too much visual weight to app and operator controls compared with thread history. Even after the center pane and footer became more session-like, the workspace still does not feel conversation-first because the rail does not lead with conversations strongly enough.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the left sidebar structure and app or operator control ranking.
- Keep the selected-thread SSE path, session strip ownership, bottom follow control, composer behavior, and side-panel behavior unchanged.
- Leave transport scope, selected-row live ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but make the left rail strictly conversation-first: thread history appears as the primary visible rail surface, the selected app remains identifiable through a compact always-visible summary near the rail header, and heavier app or operator controls move into a collapsed secondary section that stays reachable without competing with conversation history.
