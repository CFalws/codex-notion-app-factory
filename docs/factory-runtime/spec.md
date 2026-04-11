# Factory Runtime Spec

## Iteration

- current iteration: `216`
- bounded focus: `preserve one continuous workspace during selected-thread restore/resume`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, switch continuity, and the one-item transcript owner contract are already present, but the restore or resume path still needs its continuity contract recorded as the current bounded seam. The remaining bounded risk is contract drift: future sessions could let reopen or reselect flows regress into snapshot-plus-recovery behavior unless the restore or resume continuity rule is recorded explicitly.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting a saved selected-thread conversation to reopen as the same live workspace rather than a snapshot that later recovers.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread restore or resume path in the main workspace and its browser verification coverage.
- Reuse the current selected-thread session authority, restore or attach placeholder, active-session row, and composer dock datasets; do not change backend transport, polling, or broader ownership rules.
- Keep the center conversation shell and bottom-fixed composer mounted throughout saved-session restore or resume.
- Show exactly one compact restore or attach placeholder until authoritative SSE ownership returns.
- Clear stale live ownership immediately before any fallback or degraded rendering appears.
- Keep degraded fallback, switch behavior, and non-restore clears on the existing fail-open path.

## Deliverable

Expose one conversation-first selected-thread workspace where saved-session restore or resume preserves the mounted conversation shell and composer, shows one compact restore or attach placeholder, and never falls back to a generic empty or duplicated recovery surface.
