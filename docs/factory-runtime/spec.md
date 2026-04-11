# Factory Runtime Spec

## Iteration

- current iteration: `124`
- bounded focus: `promote the selected-thread transcript live activity item to the single rich realtime phase surface on the healthy SSE-owned path`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, transition continuity, and fixed-composer behavior are already established. The remaining gap is live-surface composition: the transcript already carries the authoritative live session item, but the header and composer can still read like competing rich status surfaces on the healthy path.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, switching continuity, compact header ownership chrome, footer session bar, and degraded fallback UI contracts intact.
- Do not introduce a new transport, backend protocol, persistence layer, or a second live-status authority.
- Reuse the existing selected-thread append projection, phase progression, and ownership helpers instead of adding another authority source.
- On the healthy selected-thread SSE path, keep proposal, review, verify, ready, auto-apply, applied, and autonomy detail inside exactly one transcript live activity item.
- Preserve reconnect and polling fallback only as explicit degraded paths that clear or downgrade healthy ownership in the same render cycle.

## Deliverable

Define and verify one render contract where the healthy selected-thread SSE path exposes exactly one rich transcript live activity item, while the header and footer remain compact ownership or fallback chrome and degraded paths still clear or downgrade immediately.
