# Factory Runtime Spec

## Iteration

- current iteration: `130`
- bounded focus: `make the transcript-tail live activity item the primary selected-thread session surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership, verifier-evidence authority, and shell-phase vocabulary are already established, but the center conversation pane can still emit duplicate selected-thread session-event cards beside the transcript-tail live activity item. That splits one live session into multiple center-pane status surfaces.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, switching continuity, transcript-owned rich live detail, compact header ownership chrome, footer session bar, left-rail compaction, and degraded fallback UI contracts intact.
- Do not introduce a new transport, backend protocol, persistence layer, or a second live-status authority.
- Reuse the existing selected-thread SSE authority, phase progression, and live autonomy projection.
- Keep the transcript-tail live activity item as the primary selected-thread session surface instead of adding another center-pane status carrier.
- Preserve reconnect and polling fallback only as explicit degraded paths that clear or downgrade healthy ownership in the same render cycle.

## Deliverable

Define and verify one center-lane contract where the transcript-tail live activity item is the primary selected-thread session surface, and duplicate selected-thread session-event cards collapse whenever that primary surface is present.
