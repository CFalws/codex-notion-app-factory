# Factory Runtime Spec

## Iteration

- current iteration: `170`
- bounded focus: `collapse healthy selected-thread milestone appends into the transcript-tail live activity`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center timeline still duplicates milestone progression on the healthy path. Operators can read the transcript-tail live activity, but proposal, review, verify, ready, and applied progress can still appear as separate session-event cards instead of one continuous realtime session item.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected-thread transcript to read as one authoritative live session timeline instead of a mixed live item plus milestone event feed.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread center-pane unified live timeline.
- Reuse the existing selected-thread SSE authority and transcript-tail live item; do not add a new authority source.
- Collapse selected-thread milestone session-event cards only on the healthy SSE-owned path.
- Keep degraded, restore, snapshot, switching, and terminal-cleared paths explicit and fail closed.

## Deliverable

Render exactly one healthy selected-thread primary live item in the transcript, move milestone visibility into that item's in-place milestone strip and datasets, and suppress duplicate selected-thread milestone session-event cards only on the healthy SSE-owned path.
