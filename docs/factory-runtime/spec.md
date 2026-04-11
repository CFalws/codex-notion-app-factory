# Factory Runtime Spec

## Iteration

- current iteration: `193`
- bounded focus: `collapse healthy selected-thread proposal, review, verify, ready, and applied progress into one transcript-tail live session block`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already has healthy SSE-owned live activity and session-event rendering, but the center timeline still risks reading like multiple competing session surfaces unless the healthy path clearly collapses duplicate selected-thread session events into the transcript-tail live block.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation to read like one continuous live Codex-style session rather than a live strip plus duplicate session-event cards.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the existing selected-thread transcript-tail live activity and session-event seams.
- Reuse the existing selected-thread SSE and session model already driving transcript-tail live activity, append provenance, and session-event projection; do not change transport ownership rules.
- On the healthy selected-thread SSE-owned path, expose at most one compact transcript-tail live session block that updates through `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, and `APPLIED`.
- Suppress duplicate selected-thread session-event cards only while that healthy transcript-tail live block is authoritative.
- Restore or fail open immediately on degraded, reconnect, polling fallback, restore-gap, deselected, switched, and terminal paths.

## Deliverable

Expose one continuous conversation-first selected-thread timeline where healthy SSE-owned phase progression stays inside one transcript-tail live session block, duplicate selected-thread session-event cards disappear on that path, and degraded or non-authoritative paths immediately restore or clear those event surfaces.
