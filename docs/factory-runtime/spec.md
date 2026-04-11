# Factory Runtime Spec

## Iteration

- current iteration: `169`
- bounded focus: `collapse the selected-thread center-pane live header into one compact machine-readable session summary row`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center pane still shows too much selected-thread live-status chrome above the transcript. Operators can see the transcript-tail live activity, but they still have to reconcile a second live-owner surface in the header instead of reading the conversation as one realtime session timeline.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected-thread transcript to remain the dominant realtime surface without duplicate status chrome above it.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread center-pane header summary and live-status rendering.
- Reuse the existing selected-thread SSE authority and transcript-tail live item; do not add a new authority source.
- Keep the header surface chip-first, compact, and fail closed on switching, reconnect downgrade, polling fallback, deselection, lost authority, or terminal resolution.
- Keep the transcript-tail live activity as the only primary live session item on the healthy selected-thread path.

## Deliverable

Render at most one compact selected-thread session summary row above the transcript on the healthy path, suppress duplicate live-owner chrome there, and leave the transcript-tail live activity as the only primary live session surface.
