# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread attach and reconnect now come from the SSE stream, but phase rendering still synthesizes proposal, review, verify, ready, applied, and other states from mixed latest-event heuristics. That lets non-authoritative or partial signals look like real live progression, which raises operator inference again and breaks the intended-path guarantee for a Codex-style session workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport and keep `conversation.append` events unchanged.
- Keep the change bounded to one additive authoritative phase payload on selected-thread bootstrap and append envelopes.
- Limit authoritative phase values to `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, `APPLIED`, and `FAILED`.
- When phase is missing, stale, non-authoritative, or outside that subset, render a neutral `LIVE` or `UNKNOWN` state instead of inferring progression from event heuristics.
- Keep degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states visibly non-owned or cleared so they cannot look like stale healthy live progression.

## Deliverable

Define and verify one additive selected-thread authoritative phase contract so the healthy SSE path exposes one machine-readable phase model across bootstrap, append updates, session strip, thread scroller, and inline live block, while all non-authoritative cases degrade to `LIVE` or `UNKNOWN`.
