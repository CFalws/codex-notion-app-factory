# Factory Runtime Spec

## Iteration

- current iteration: `200`
- bounded focus: `make the center transcript own one authoritative healthy selected-thread live session-progress item`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already has healthy-path SSE ownership and switch continuity, but the realtime session still reads as multiple parallel status surfaces unless the center transcript is treated as the one authoritative healthy selected-thread session-progress item and duplicate session-event storytelling stays suppressed on that path.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation to read like one continuous live Codex-style session rather than a live strip plus duplicate session-event cards.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the healthy selected-thread center-pane timeline and existing browser verification seam.
- Reuse the existing selected-thread SSE-owned phase and authority datasets already driving the transcript live item; do not change transport ownership rules.
- On the healthy selected-thread path, expose exactly one authoritative live session-progress item in the center transcript and suppress duplicate SSE session-event cards on that path.
- Preserve in-place progression through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
- Clear or fail open immediately on reconnect, polling fallback, switch, deselection, restore-gap, and terminal completion.

## Deliverable

Expose one conversation-first selected-thread workspace where the healthy SSE-owned center transcript carries exactly one authoritative live session-progress item, duplicate parallel session-progress surfaces stay suppressed on that path, and non-authoritative transitions clear or restore immediately.
