# Factory Runtime Spec

## Iteration

- current iteration: `211`
- bounded focus: `preserve one continuous center workspace during selected-thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, left-rail mirroring, healthy-path SSE authority, secondary-card suppression, and the compact composer utility affordance are already present, but thread switches still need to read as one continuous live workspace rather than a drop into an empty or reset view. The remaining bounded risk is that operators may still infer the wrong state during a deliberate thread switch if the center pane or composer appears to unmount, flash empty, or leave stale ownership cues behind while the next snapshot attaches.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting intentional thread switches to feel like one continuous session workspace rather than a tear-down and rebuild.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to selected-thread switch rendering, workspace placeholders, composer continuity, and browser verification coverage.
- Reuse the current selected-thread session authority and thread-transition datasets; do not change backend transport, polling, or broader ownership rules.
- Keep the center shell and bottom-fixed composer mounted throughout an intentional selected-thread switch.
- Show at most one compact switching placeholder while the new selected-thread snapshot attaches.
- Clear old-thread live-owned cues immediately on switch start and reserve the generic empty workspace for true no-selection idle only.
- Keep reconnect downgrade, polling fallback, deselection, restore-gap loss, and terminal resolution on the existing fail-open clear path.

## Deliverable

Expose one conversation-first selected-thread workspace where intentional thread switches preserve the mounted conversation shell and composer, show at most one compact switching placeholder, and never flash the generic empty state.
