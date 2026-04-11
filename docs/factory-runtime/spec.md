# Factory Runtime Spec

## Iteration

- current iteration: `94`
- bounded focus: `canonical selected-thread phase progression contract`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread session ownership is canonical, but bounded autonomy progress still reads as fragmented cues rather than one explicit realtime phase flow. The active session can show that it is live, yet still force the operator to infer whether the run is in proposal, review, verify, auto-apply, ready, or applied progression.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session-status boundary and selected-thread live-autonomy boundary in the frontend store.
- Reuse existing append-stream, pending-handoff, session-phase, autonomy summary, and thread-transition state; do not introduce a new transport or a new polling contract.
- Make proposal, review, verify, auto-apply, ready, applied, and fallback progression finite and machine-readable on the selected-thread path.
- Preserve the bottom-fixed composer, center transcript card, and rail behavior already established in earlier iterations.
- Do not suppress `/api/jobs` or `/api/goals` polling in this iteration; only make the selected-thread SSE phase progression explicit and consistent.

## Deliverable

Define and verify one canonical selected-thread phase progression model on the existing SSE path, then have the center-lane autonomy or session surface and composer-adjacent phase surface consume that model so the active session shows explicit proposal, review, verify, auto-apply, ready, and applied flow without transport or polling changes.
