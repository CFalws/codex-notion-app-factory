# Factory Runtime Spec

## Iteration

- current iteration: `236`
- bounded focus: `remove the center-pane recent-thread rail so the conversation workspace stays session-first`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, and conversation-mode switch or restore continuity are already present. The remaining bounded gap is duplicated navigation chrome in the center pane: the workspace should keep thread switching owned by the left rail or mobile nav sheet so the transcript remains the dominant live session surface.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting thread navigation to live in the left rail or mobile sheet while the center pane stays focused on one continuous selected-thread session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the center-pane recent-thread rail render path, the existing left-rail and mobile-sheet navigation owners, and matching verifier or proposal artifacts.
- Remove center-pane recent-thread navigation chrome instead of introducing a replacement panel or transport.
- Preserve intentional thread switch and restore continuity through the existing inline `timeline-transition` item and mounted composer shell.
- Keep left-rail conversation cards and the mobile nav sheet as the only thread-switch owners.
- Preserve reconnect and polling downgrade as explicit degraded fallback that clears healthy ownership immediately.
- Keep handoff, live execution, switch continuity, and terminal clear behavior on the current intended path.

## Deliverable

Expose one conversation-first selected-thread workspace where the center pane contains only transcript, canonical session surfaces, and the fixed composer, while thread switching remains owned by the left rail or mobile nav sheet and switch or restore continuity still uses one inline transition item.
