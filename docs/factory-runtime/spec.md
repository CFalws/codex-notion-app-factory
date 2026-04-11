# Factory Runtime Spec

## Iteration

- current iteration: `119`
- bounded focus: `footer session strip and detached follow converge into one bottom-fixed session bar`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, switching continuity, one center live session lane, and a canonical detached follow model are already established. The remaining gap is the footer itself: the composer dock still splits live session state and detached follow behavior across the session strip and a separate bottom follow control.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, center live-lane, rail, and polling-fallback contracts unchanged.
- Do not introduce a new transport, polling path, backend protocol, or a second footer follow surface.
- Reuse the existing selected-thread footer dock and follow-control models instead of adding a new footer state machine.
- Show exactly one composer-adjacent footer session bar on the healthy selected-thread SSE path.
- Let that bar carry live phase progression while following and switch into explicit `NEW` or `PAUSED` follow state with unseen-count metadata when detached from the tail.
- Clear or degrade that footer follow treatment immediately on jump-to-latest, switching, reconnect downgrade, polling fallback, terminal idle, or any non-selected context.

## Deliverable

Define and verify one footer session-bar contract where the selected-thread footer strip is the only live-owned footer surface and it switches between phase progression and `NEW` or `PAUSED` follow state without a separate bottom follow button.
