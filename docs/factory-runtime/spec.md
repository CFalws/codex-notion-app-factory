# Factory Runtime Spec

## Iteration

- current iteration: `125`
- bounded focus: `collapse left-rail selected-thread live mirroring into one sticky active-session row`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, transition continuity, and transcript-owned rich live detail are already established. The remaining gap is left-rail duplication: the sticky active-session row is already the canonical rail mirror, but the selected conversation card and recent-thread chip can still inject helper-style live storytelling that competes with it.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, switching continuity, transcript-owned rich live detail, compact header ownership chrome, footer session bar, and degraded fallback UI contracts intact.
- Do not introduce a new transport, backend protocol, persistence layer, or a second live-status authority.
- Reuse the existing selected-thread append projection, follow-control, and ownership helpers instead of adding another authority source.
- Keep the sticky active-session row as the only live-owned left-rail mirror for the selected thread.
- Preserve reconnect and polling fallback only as explicit degraded paths that clear or downgrade healthy ownership in the same render cycle.

## Deliverable

Define and verify one rail contract where the healthy selected-thread SSE path exposes at most one sticky active-session row in the left navigation, while selected cards stay chip-first and non-selected rows remain snapshot-only.
