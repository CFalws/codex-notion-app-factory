# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected conversation now has one compact session strip, but on phone widths the strip and composer still read as separate stacked surfaces. That weakens the live-session feel because state visibility and input reachability do not yet behave like one persistent conversation-local footer region.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

On phone widths, merge the existing selected-conversation session strip and composer into one persistent footer dock so live state remains visible while the input stays continuously reachable, without adding new transport or expanding status scope.
