# Factory Runtime Spec

## Iteration

- current iteration: `238`
- bounded focus: `collapse the selected-thread center header into one compact session capsule`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, and conversation-mode switch or restore continuity are already present. The remaining bounded gap is duplicated live-status chrome in the center header: the workspace should expose one compact selected-thread session capsule instead of splitting ownership across a summary row and a separate phase badge.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation header to expose one authoritative live-session state without reconciling multiple header surfaces.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the existing header render seam, selected-thread authority model, and matching verifier or proposal artifacts.
- Use the existing chip-first `thread-session-summary` as the only visible center-header session surface.
- Force the legacy `thread-phase-chip` out of the visible header path so it can no longer act as a second live-status owner.
- Preserve transcript inline session ownership, footer dock behavior, left-rail cues, and switch or restore continuity on the current intended path.
- Keep degraded reconnect or polling fallback and terminal clear transitions explicit in the single header capsule.
- Avoid adding a new header panel, new transport, or any second live-detail owner in the center pane.

## Deliverable

Expose one conversation-first selected-thread workspace where the center header shows one compact selected-thread session capsule carrying scope, path, owner, and phase together, while the transcript inline session block remains the canonical live session surface and all degraded transitions clear or downgrade the header immediately.
