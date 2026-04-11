# Factory Runtime Spec

## Iteration

- current iteration: `123`
- bounded focus: `healthy selected-thread SSE becomes the sole visible authority for live job and autonomy state`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, transition continuity, and fixed-composer behavior are already established. The remaining gap is state authority: live job and autonomy state can still be reclaimed by poll-driven updates even after the selected-thread SSE path is already authoritative.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, center live-lane, header ownership surface, footer session bar, and degraded fallback UI contracts unchanged.
- Do not introduce a new transport, backend protocol, persistence layer, or a second live-status authority.
- Reuse the existing selected-thread append projection and ownership helpers instead of adding another authority source.
- On the healthy selected-thread SSE path, keep live job meta, proposal readiness, verifier progress, and autonomy state sourced from append SSE instead of poll-driven jobs or goals refresh.
- Preserve reconnect and polling fallback only as explicit degraded paths that clear or downgrade healthy ownership in the same render cycle.

## Deliverable

Define and verify one authority contract where the healthy selected-thread SSE path is the sole visible source for live job and autonomy state, while degraded and non-selected paths fall back explicitly without stale healthy ownership.
