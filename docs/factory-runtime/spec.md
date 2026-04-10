# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread inline session block now has deterministic terminal retention, but the composer-adjacent live strip still duplicates the same healthy session state. That duplication makes the center workspace feel more like a dashboard with repeated chrome than one live session timeline.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership, pending handoff, live phase, and inline terminal-retention selectors instead of introducing a new runtime state source.
- Keep the change bounded to the selected-thread timeline block and composer-adjacent strip visibility contract.
- Keep the composer owner row and thread-switch context surfaces intact.
- Clear or downgrade immediately on reconnect, polling fallback, thread switch, or ownership loss.

## Deliverable

Promote the selected-thread inline session block to the single canonical healthy live-progress surface in the center timeline, suppress the duplicate healthy composer-adjacent strip for the same selected-thread states, and preserve machine-readable ownership datasets so follow and bottom-fixed composer behavior continue to work.
