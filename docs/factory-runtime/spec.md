# Factory Runtime Spec

## Iteration

- current iteration: `81`
- bounded focus: `composer-adjacent session strip phase authority`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread session ownership and switch continuity are now bounded, but the composer-adjacent session strip still spreads live phase reading across owner, transport, and phase chips, which forces the operator to infer the current session phase instead of reading one authoritative strip state.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership, `liveRun`, `sessionPhase`, and degraded-path datasets.
- Keep the change bounded to the composer-adjacent session strip renderer and the focused selected-thread verifier contract.
- Render the healthy selected-thread strip as one compact machine-readable phase row driven by selected-thread SSE provenance.
- Downgrade the strip immediately to `RECONNECT` or `POLLING` on degraded ownership and clear stale healthy phase on switch or idle.
- Keep the bottom-fixed composer intact on desktop and phone layouts.
- Do not introduce new transport, new side surfaces, or renewed `/api/goals` dependency on the healthy path.

## Deliverable

Make the composer-adjacent selected-thread session strip the single authoritative live phase surface on the healthy SSE path so it shows `LIVE`, `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, and `APPLIED` directly from selected-thread SSE provenance, then relabels or clears immediately on reconnect, polling fallback, switch, or idle.
