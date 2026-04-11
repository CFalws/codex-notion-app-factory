# Factory Runtime Spec

## Iteration

- current iteration: `99`
- bounded focus: `machine-readable selected-thread restore stage`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Saved selected-thread restore still lacks an explicit machine-readable stage in this proposal worktree. Reload or re-entry can therefore look correct in prose while remaining harder to prove through the intended authoritative SSE attach or resume path.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session-status, live-autonomy, and phase-progression helpers in the frontend store.
- Reuse existing append-stream `attachMode` and `resumeMode` state; do not introduce a new transport or a new polling contract.
- Keep exactly one live session surface in the transcript timeline during saved selected-thread restore and subsequent healthy SSE ownership.
- Preserve the bottom-fixed composer, thread-switch clearing, degraded reconnect or polling markers, and rail behavior already established in earlier iterations.
- Do not suppress `/api/jobs` or `/api/goals` polling in this iteration; make the restore path explicit and machine-readable instead.

## Deliverable

Define and verify one canonical selected-thread restore stage contract shared by the store, transcript-tail live item, compact header summary, and composer ownership row so a saved selected conversation can move from explicit restore `ATTACH` or `RESUME` into authoritative SSE ownership without snapshot-ready ambiguity.
