# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace still makes live transcript following too implicit during active SSE delivery. When the operator scrolls away from the bottom, the console needs to make it obvious whether new selected-thread appends are arriving live off-screen or whether the session has degraded back toward a paused or snapshot path.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the selected-thread transcript follow control and live-follow state presentation.
- Keep non-selected thread behavior, selected-thread SSE ownership, composer dock, thread-switch continuity, and side-panel behavior unchanged.
- Leave selected-thread transport ownership, selected-row live ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but make the selected transcript expose one compact bottom follow control with explicit `NEW` vs `PAUSED` state and unseen-append count derived only from selected-thread scroll position plus append provenance. The control should appear only when relevant, clear immediately on jump-to-latest, thread switch, terminal idle, or degraded fallback, and avoid creating any new multi-thread or secondary-panel status surface.
