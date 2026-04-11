# Factory Runtime Spec

## Iteration

- current iteration: `206`
- bounded focus: `make append SSE the sole healthy-path selected-thread session authority`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, and switch continuity are already present, but the selected-thread workspace can still inherit polling-owned job or autonomy state during healthy attach and render paths. The remaining bounded risk is hidden polling authority mutating a supposedly live session surface, which breaks the goal of a true session-level realtime workspace.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting healthy selected-thread job, phase, proposal, verifier, and apply state to update from one live session path without hidden polling-driven overrides.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread healthy path, the existing append SSE session status payload, and the job and goals fallback gate in the operator console.
- Reuse the current selected-thread session status and session strip model; do not change backend transport or broader multi-thread ownership rules.
- On the healthy selected-thread path, treat append SSE session status as the sole authority for current job, phase, proposal readiness, verifier status, and apply availability.
- Preserve the current fallback behavior only for reconnect, deselection, switch, restore-gap, or terminal authority loss.

## Deliverable

Expose one conversation-first selected-thread workspace where healthy selected-thread session state is owned by append SSE alone, with polling and goal-summary fallback re-enabled only on explicit authority loss.
