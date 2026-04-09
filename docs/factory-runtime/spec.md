# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live rail is clearer now, but thread navigation still depends on too much inference because conversation cards mostly show only a title and timestamp. Users cannot quickly tell which thread is active, currently progressing, or recently completed without opening it first.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Keep the current sidebar structure, but render each conversation card with one bounded recent-preview line and a clearer compact state label. Use only existing conversation snapshots for non-selected threads and the current selected-conversation SSE-derived state for the active thread.
