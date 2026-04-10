# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already preserves shell continuity across thread switches, but the composer-adjacent session rail still under-explains the intended realtime path. Operators should be able to tell at a glance whether the selected thread is on a healthy `LIVE` SSE path, reconnecting, or offline without scanning secondary panels or mistaking polling fallback for live ownership.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the selected-thread composer-adjacent live rail in the existing center workspace.
- Keep the selected-thread SSE path, transcript shell, composer ownership row, bottom follow control, and side-panel behavior unchanged.
- Leave transport scope, runtime APIs, selected-row live ownership, and polling fallback semantics unchanged while making the selected-thread transport-health rail clearer.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but make the composer-adjacent session rail expose one compact chip-first source of truth for selected-thread transport health and phase: show explicit `LIVE`, `RECONNECT`, `OPEN`, or `OFFLINE` transport state beside the current phase and compact provenance, keep degraded transport visibly distinct without pretending live ownership, and clear the rail on polling-only fallback, terminal idle, or thread switch.
