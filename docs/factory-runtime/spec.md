# Factory Runtime Spec

## Iteration

- current iteration: `210`
- bounded focus: `mirror the selected-thread live session into the left rail sticky row`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, switch continuity, healthy-path SSE authority, secondary-card suppression, and the compact composer utility affordance are already present, but the left rail still under-mirrors the active session during the healthy selected-thread path. The remaining bounded risk is that operators still have to infer which thread is actively live from the center pane and composer alone because the sticky rail row is still treated as degraded-only in verifier and durable-contract terms.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the navigation rail to mirror the currently live selected session without becoming a second authority surface.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the sticky active-session row, selected-thread rail rendering, and browser verification coverage.
- Reuse the current selected-thread session authority, phase, and follow or unseen datasets; do not change backend transport, polling, or broader ownership rules.
- Keep the rail row non-authoritative and chip-first even when it mirrors the healthy selected-thread session.
- Show exactly one sticky active-session row for the selected thread on healthy live, handoff, switching, new, or paused states.
- Clear the sticky row immediately on reconnect downgrade, polling fallback, thread switch, deselection, idle, or terminal resolution, and never let a non-selected row gain live-owned treatment.

## Deliverable

Expose one conversation-first selected-thread workspace where the left rail shows exactly one compact sticky row for the selected live thread without creating a second authoritative session surface.
