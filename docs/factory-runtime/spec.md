# Factory Runtime Spec

## Iteration

- current iteration: `215`
- bounded focus: `preserve one continuous center workspace during selected-thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, and the one-item transcript owner contract are already present, but the main workspace still needs its switch-continuity contract recorded as the current bounded seam. The remaining bounded risk is contract drift: future sessions could let the center pane flash a generic empty state, clear the composer dock, or leave stale ownership cues during intentional thread switches unless that continuity rule is recorded explicitly.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting intentional selected-thread switches to feel like one continuous live workspace instead of a reset or teardown.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread switch path in the main workspace and its browser verification coverage.
- Reuse the current selected-thread session authority, workspace placeholder, and composer dock datasets; do not change backend transport, polling, or broader ownership rules.
- Keep the center conversation shell and bottom-fixed composer mounted throughout intentional selected-thread switches.
- Show at most one compact transition placeholder while the target selected conversation snapshot attaches.
- Clear old-thread live ownership immediately on switch start and reserve the generic empty workspace for true no-selection idle only.
- Keep degraded fallback, restore behavior, and non-switch clears on the existing fail-open path.

## Deliverable

Expose one conversation-first selected-thread workspace where intentional thread switches preserve the mounted conversation shell and composer, show at most one compact switching placeholder, and never flash the generic empty state.
