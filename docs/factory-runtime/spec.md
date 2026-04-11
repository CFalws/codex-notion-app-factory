# Factory Runtime Spec

## Iteration

- current iteration: `207`
- bounded focus: `collapse healthy-path autonomy and execution state into the center session surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, switch continuity, and healthy-path SSE authority are already present, but the workspace still splits live state across the center session surface and separate secondary-detail cards. The remaining bounded risk is operator inference caused by duplicate healthy-path execution and autonomy surfaces that should no longer be authoritative.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting current phase, verifier state, blocker reason, and apply readiness to read from one live conversation surface instead of split status panels.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread presentation layer and the existing render helpers for the secondary autonomy and execution surfaces.
- Reuse the current selected-thread session status, timeline authority, session strip, and milestone models; do not change backend transport or broader ownership rules.
- On the healthy selected-thread path, keep the center timeline and session strip authoritative and suppress duplicate autonomy and execution detail cards.
- Preserve the current bottom-fixed composer, switch placeholder, reconnect fallback, restore flow, and degraded-path secondary detail behavior.

## Deliverable

Expose one conversation-first selected-thread workspace where healthy selected-thread autonomy and execution state read from the center timeline and adjacent session strip without duplicate secondary-detail cards.
