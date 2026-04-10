# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center pane is now more session-like, but the left rail still does not make the active live thread unmistakable enough. The selected row needs a stronger live-owner treatment so users can identify the running conversation immediately, while every non-selected row remains strictly snapshot-only.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the left conversation rail.
- Keep non-selected thread behavior snapshot-only.
- Leave selected-thread transport ownership, dock behavior, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and overall shell ownership, but refine the selected conversation row so it alone exposes compact live-owner cues for handoff, active SSE ownership, and follow or unread state, then clears those markers immediately on terminal resolution, polling-only fallback, or thread switch.
