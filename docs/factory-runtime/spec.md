# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread inline live and degraded markers are now in place and deployed verification can now prove them in the browser, but live autonomy-phase visibility still depends on an extra app-goals refetch. That makes the session surface feel less immediate than the append stream that already carries the phase events.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE append stream and autonomy summary shape instead of changing backend transport or state schema.
- Keep the change bounded to client-side selected-thread append handling and the live session summary projection it feeds.
- Preserve full goal fetches for initial load, thread attach, and degraded recovery paths.

## Deliverable

Define and verify a client-side projection so proposal, review, verify, auto-apply, ready, applied, and failure transitions update the selected-thread live session surfaces directly from healthy SSE append events without an app-goals refetch on each live phase event.
