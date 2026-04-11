# Factory Runtime Spec

## Iteration

- current iteration: `190`
- bounded focus: `prove the selected-thread switch path stays inside one mounted conversation workspace`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already derives switch continuity through the existing thread-transition and workspace-placeholder seams, but the high-value remaining question is whether the intended switch path is explicit and verifier-acceptable rather than merely working through fallback inference.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting intentional thread switches to feel like one continuous live session instead of a drop to idle or empty state.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the existing selected-thread switch placeholder, workspace placeholder, and composer-target continuity seam.
- Reuse the existing selected-thread SSE and session model already driving workspace placeholder, transition, and composer surfaces; do not change transport ownership rules.
- Keep the transcript shell and bottom-fixed composer mounted during intentional thread switches.
- Require exactly one compact switching placeholder while the incoming selected thread snapshot or live authority attaches.
- Fail closed on degraded, reconnect, polling fallback, restore-gap, deselected, switched, and terminal paths.

## Deliverable

Expose one continuous conversation-first switch path where old-thread live ownership clears immediately, the generic empty workspace never flashes during intentional switches, and the incoming selected thread stays visible through one compact transition placeholder until attach completes.
