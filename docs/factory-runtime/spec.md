# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already keeps progress and switching continuity visible, but the composer still relies on surrounding context to explain which thread the next input will target. Users should be able to see the exact selected conversation and whether the composer is `READY`, `SWITCHING`, or in `HANDOFF` without inferring hidden ownership from nearby UI.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to composer ownership presentation and send gating in the center workspace.
- Keep the selected-thread SSE path, session strip ownership, bottom follow control, composer behavior, and side-panel behavior unchanged.
- Leave transport scope, selected-row live ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but add a compact composer target row that names the selected conversation and shows `READY`, `SWITCHING`, or `HANDOFF` from the same selected-thread owner state already used elsewhere. Keep it visible on desktop and phone, block send only while attach is unresolved, and never let it advertise stale old-thread or polling-derived live ownership.
