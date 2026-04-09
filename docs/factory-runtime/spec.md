# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live rail now exposes the right phase model, but the composer-adjacent surface still behaves like a prose-heavy status strip above the action area. The remaining friction is not missing state but status-panel drift at the point where the user reads and sends messages.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Leave the left navigation, central timeline, submit handoff, polling fallback rules, and broader workspace structure unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and composer-adjacent live surface, but replace the verbose strip with a compact composer state row that shows only transport state, current phase, proposal readiness, and short send or apply affordance text.
