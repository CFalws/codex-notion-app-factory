# Factory Runtime Spec

## Iteration

- current iteration: `199`
- bounded focus: `preserve one continuous selected-thread workspace through intentional thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already has strong healthy-path SSE ownership proof, but the realtime session illusion still breaks if an intentional thread change drops the user out of the mounted conversation shell or flashes the generic empty workspace before the next thread attaches.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation to read like one continuous live Codex-style session rather than a live strip plus duplicate session-event cards.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the intentional selected-thread switch path in the existing conversation-first workspace shell.
- Reuse the existing thread-transition datasets, active-session row, session strip, and workspace placeholder seams; do not change transport ownership rules.
- Keep the center conversation shell and bottom-fixed composer dock mounted while a deliberate switch is in progress.
- Clear prior selected-thread live ownership immediately on switch start and expose exactly one compact switching placeholder until the incoming thread snapshot attaches.
- Reserve the generic empty workspace for true no-selection idle only.

## Deliverable

Expose one continuous conversation-first selected-thread workspace where an intentional switch keeps the mounted shell and composer visible, clears old live ownership immediately, and renders one compact switching placeholder instead of flashing a generic empty state.
