# Factory Runtime Spec

## Iteration

- current iteration: `241`
- bounded focus: `absorb selected-thread follow affordance into the footer dock so the composer-adjacent strip becomes the sole follow owner`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, unified header chrome, the removal of selected-thread goals-poll authority, and compact chip-first session surfaces are already present. The remaining bounded gap is the detached follow control: the floating jump-to-latest button still competes with the footer dock instead of letting the composer-adjacent strip own NEW and PAUSED follow state on the selected thread.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the active selected conversation to behave like one live session whose follow state, owner, phase, and composer controls stay attached to the same bottom-fixed surface.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to selected-thread follow presentation in the footer dock, DOM wiring, and verifier artifacts.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the transcript inline session block as the only in-timeline live progress surface.
- Remove the separate floating follow control instead of adding another owner.
- Avoid adding a new transport, a new panel, or any second live-detail owner in the center pane.

## Deliverable

Expose one conversation-first selected-thread workspace where the footer dock is the sole selected-thread follow owner, carrying NEW or PAUSED follow state and unseen-count metadata next to the fixed composer while the existing selected-thread `session_status` plus SSE authority path and degraded downgrade behavior remain intact.
