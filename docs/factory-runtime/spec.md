# Factory Runtime Spec

## Iteration

- current iteration: `231`
- bounded focus: `collapse selected-thread live execution into one canonical transcript-tail session block`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, switch continuity, restore continuity, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, and selected-thread session-status authority are already present. The remaining bounded gap is operator inference caused by duplicated live-detail surfaces: the healthy selected-thread workspace should read as one realtime session centered on the transcript-tail session block while mirrors stay compact and passive.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting live handoff, phase, proposal, review, verify, ready, and applied progression to read as one continuous conversation session instead of separate status panels that require inference.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the existing selected-thread append SSE ownership path, current render boundaries, and matching proposal artifacts.
- Reuse the inline session block, selected-thread session-status helper, handoff state, and current mirror datasets instead of adding new transport or backend seams.
- Keep the transcript-tail session block as the only healthy live-owned surface for handoff and live execution progression.
- Keep the bottom-fixed composer mounted and chat-first with only target and send controls; do not let it become a second live status surface.
- Keep header and rail mirrors compact and passive.
- Preserve reconnect and polling downgrade as explicit degraded fallback that clears canonical live ownership immediately.
- Keep restore, switch, and terminal clear behavior on the current intended path.

## Deliverable

Expose one conversation-first selected-thread workspace where healthy live handoff and autonomy progression converge into one compact transcript-tail session block, while header, rail, and composer-adjacent surfaces remain passive mirrors and polling stays explicit degraded fallback.
