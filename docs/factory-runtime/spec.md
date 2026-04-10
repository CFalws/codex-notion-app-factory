# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership, polling suppression, and switch continuity are now in place, but the left thread rail still makes the current live session too easy to lose visually. Operators can understand the center pane, but they still have to infer which thread currently owns the live session when glancing at navigation.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session summary, live indicator, follow state, and thread-transition state instead of introducing a new transport or ownership source.
- Keep the change bounded to the sticky active-session row above the conversation list.
- Preserve snapshot-only behavior for non-selected threads and clear the sticky row immediately on idle, terminal, reconnect downgrade, polling fallback, or switched-away paths.

## Deliverable

Define and verify one compact sticky active-session row above the conversation list so the selected thread's healthy live ownership, phase, follow or unseen state, and attach transition are visible directly from the left rail.
