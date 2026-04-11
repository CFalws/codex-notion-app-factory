# Factory Runtime Spec

## Iteration

- current iteration: `118`
- bounded focus: `transcript-bottom follow control is owned only by healthy selected-thread SSE follow state`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, switching continuity, left-rail mirroring, and one center live session lane are already established. The remaining gap is off-tail follow ownership: the transcript-bottom follow control still depends on render-local logic instead of the same selected-thread SSE session model as the rest of the workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, center live-lane, composer, rail, and polling-fallback contracts unchanged.
- Do not introduce a new transport, polling path, backend protocol, or a second follow-status surface.
- Reuse the existing selected-thread session-status and live-follow state instead of relying on render-local ownership checks.
- Show exactly one compact transcript-bottom follow control only for the healthy selected-thread SSE-owned path when the operator is detached from the tail.
- Carry explicit `NEW` or `PAUSED` follow state plus unseen-count metadata through machine-readable datasets.
- Clear that control immediately on jump-to-latest, composer re-engagement, switching, reconnect downgrade, polling fallback, terminal idle, or any non-selected context.

## Deliverable

Define and verify one selected-thread follow-control contract where the transcript-bottom control is owned only by healthy SSE-selected follow state with explicit `NEW` or `PAUSED` plus unseen-count metadata, while degraded and non-selected paths clear it immediately.
