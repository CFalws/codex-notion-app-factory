# Factory Runtime Spec

## Iteration

- current iteration: `233`
- bounded focus: `replace switch and restore placeholder ownership with one inline timeline transition item`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, and streamed autonomy identity are already present. The remaining bounded gap is the center-pane mode-switch feel during selected-thread switch and restore: the workspace should keep conversation mode and represent attach or restore through one inline transition item instead of through placeholder ownership semantics.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting selected-thread switch, restore, and attach to feel like the same conversation workspace continuing rather than a temporary dashboard or placeholder mode.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the existing selected-thread switch and restore path, current render boundaries, and matching proposal artifacts.
- Reuse the existing inline `timeline-transition` item and mounted composer shell instead of introducing a second transition transport or panel.
- Keep the center conversation timeline in conversation mode during switch or restore.
- Clear old-thread live ownership immediately and allow exactly one inline transition item to represent attach or restore state.
- Keep the composer target row and session strip synchronized to the same transition state.
- Preserve reconnect and polling downgrade as explicit degraded fallback that clears healthy ownership immediately.
- Keep handoff, live execution, and terminal clear behavior on the current intended path.

## Deliverable

Expose one conversation-first selected-thread workspace where switch and restore stay inside the canonical timeline via one compact inline transition item, the bottom composer remains mounted, and placeholder-mode ownership no longer interrupts the session flow.
