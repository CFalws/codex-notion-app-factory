# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread SSE path is already conversation-first, but intentional thread switching still needs stronger intended-path proof to show that the workspace stays mounted, clears stale ownership immediately, and uses the dedicated transition placeholder instead of falling through to generic empty-state behavior.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread ownership, thread-transition, header summary, and composer-owner contracts instead of adding a new backend or transport path.
- Keep the change bounded to intentional selected-thread switch continuity and its verification contract.
- Keep the center workspace mounted during switch: no generic empty-state flash unless there is truly no selected conversation.
- Clear old-thread live ownership immediately in header, rail, transcript, and composer while making degraded fallback remain explicit rather than looking healthy.

## Deliverable

Define and verify one selected-thread switch path where the center workspace stays mounted, the dedicated transition placeholder owns the gap until the new snapshot attaches, the header live indicator clears immediately, and the composer remains docked with an explicit `SWITCHING` target state.
