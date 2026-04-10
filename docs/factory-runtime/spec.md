# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace still feels too much like a context reset during thread switches. Moving between conversations currently drops the center pane to a blank or empty-state render before the next snapshot attaches, which breaks the live-session feel even when the selected-thread SSE path itself is correct.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the selected-thread switch path in the center workspace.
- Keep non-selected thread behavior snapshot-only.
- Leave selected-thread transport ownership, dock behavior, selected-row live ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and overall shell ownership, but replace the hard reset on intentional thread switch with one compact in-place session handoff state inside the center workspace. The composer and transcript shell should stay visually anchored, prior-thread live ownership should clear immediately, and the transition placeholder should disappear as soon as the new snapshot and selected-thread SSE ownership attach.
