# Factory Runtime Spec

## Iteration

- current iteration: `173`
- bounded focus: `make selected-thread session_status the single healthy live autonomy source across the workspace`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace still depends on autonomy-summary polling fallback for some proposal, review, verify, blocker, intended-path, and verifier state. That leaves part of the active session delayed or inferred even when the healthy selected-thread SSE seam already carries the canonical autonomy signal.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting healthy selected-thread autonomy state to update immediately from the same live session stream without waiting for separate goals polling.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to read-only derivation over the existing selected-thread append SSE and `session_status` seam.
- Reuse the existing selected-thread `session_status` payload; do not add a new autonomy authority source.
- Promote healthy selected-thread SSE ownership over goals polling fallback for visible autonomy state.
- Fail closed back to degraded or polling treatment on reconnect, deselection, restore gap, or polling-owned paths.

## Deliverable

Drive visible selected-thread autonomy state from canonical `session_status` during healthy SSE ownership, suppress goals polling fallback on that intended path, and keep degraded, restore, deselected, and polling-owned paths explicitly non-authoritative.
