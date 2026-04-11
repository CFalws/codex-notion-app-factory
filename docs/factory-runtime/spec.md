# Factory Runtime Spec

## Iteration

- current iteration: `174`
- bounded focus: `make the transcript live item the single healthy selected-thread realtime session surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace now has authoritative healthy session state from `session_status`, but operators still see it split across the transcript, header summary, and secondary facts surfaces. That duplication weakens the conversation-first realtime session feel even when the healthy selected-thread SSE path is correct.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the central transcript to read as one canonical live session timeline without reconciling duplicate summary surfaces.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread render boundary in the operator console.
- Reuse the existing selected-thread SSE and `appendStream.sessionStatus` authority; do not add a new live session source.
- Promote the transcript-bound live activity item to carry the healthy phase, proposal, verifier, blocker, and intended-path contract.
- Suppress competing header summary and secondary facts surfaces on that same healthy path.
- Fail closed on degraded, restore, handoff, deselected, and no-selection states.

## Deliverable

Expose one obvious healthy selected-thread transcript live session item with the canonical `session_status` contract, while duplicate thread summary and secondary facts surfaces suppress themselves on that path and degraded or restore states remain explicit and non-authoritative.
