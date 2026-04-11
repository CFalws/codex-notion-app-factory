# Factory Runtime Spec

## Iteration

- current iteration: `131`
- bounded focus: `unify the transcript-tail live activity item and composer-adjacent session strip behind one canonical selected-thread session surface model`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership, verifier evidence, and shell-phase vocabulary are already established, but the transcript-tail live activity item and the composer-adjacent session strip still derive overlapping live session state independently. That leaves two selected-thread session surfaces that can drift in wording or autonomy detail even when they represent the same authoritative SSE-owned session.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation and fixed composer dock to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, switching continuity, transcript-primary center-lane contract, compact shell labels, left-rail compaction, and degraded fallback UI contracts intact.
- Do not introduce a new transport, backend protocol, persistence layer, or polling-derived session heuristic.
- Reuse the existing selected-thread SSE session status, phase progression, verifier acceptability, blocker reason, and degraded-path clearing rules.
- Keep proposal or snapshot-only state from implying healthy selected-thread session ownership.
- Preserve reconnect, polling fallback, restore, switch, and deselection only as explicit degraded or cleared states in the same render cycle.

## Deliverable

Define and verify one canonical selected-thread session surface model that both the transcript-tail live activity item and the composer-adjacent session strip render from, so the center workspace and fixed composer read as one authoritative live session surface.
