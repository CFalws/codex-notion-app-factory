# Factory Runtime Spec

## Iteration

- current iteration: `146`
- bounded focus: `preserve the selected-thread conversation shell and composer through intentional thread switches with one compact transition placeholder and no empty-state flash`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live timeline, header chip, and composer rail already reflect healthy and degraded state, but intentional thread switches can still force the workspace through a reset-looking gap that makes operators infer whether the session is loading, cleared, or broken.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting an intentional thread switch to feel continuous rather than like a transient reset.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread switch render path plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, or composer ownership rules.
- Keep the center conversation shell and bottom composer mounted during an intentional switch.
- Reuse the existing switching placeholder and selected-thread workspace ownership rules.
- Suppress the generic empty-state only during an active intentional switch for the selected thread.
- Clear the previous thread's live-owned treatment immediately, and clear the switch placeholder as soon as the new selected-thread snapshot or live session attaches.
- Preserve the normal empty-state for true idle with no selected conversation.

## Deliverable

Preserve the selected-thread conversation shell and fixed composer through an intentional thread switch by rendering at most one compact, machine-readable `SWITCHING` placeholder until the new selected-thread snapshot or live session attaches, without ever flashing the generic empty-state during that switch window.
