# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread inline live and degraded markers are now in place, and live autonomy summary is already projected from append events, but the central transcript still renders many session milestones as generic event cards. That leaves the operator inferring phase progression instead of seeing one conversation-first session timeline.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append events, live-run state, and autonomy summary projection instead of changing backend transport or state schema.
- Keep the change bounded to the transcript render layer for selected-thread session milestones.
- Preserve the current degraded-session indicator and thread-switch placeholder behavior without duplicating state in separate panels.

## Deliverable

Define and verify one compact session-event projection layer so proposal, review, verify, auto-apply, ready, applied, and failure transitions render directly in the selected-thread conversation timeline from append events while healthy SSE ownership holds.
