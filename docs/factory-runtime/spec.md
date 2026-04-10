# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread SSE path now drives the center timeline and related phase chips accurately, but the side panel still presents the same autonomy blocker, path, and verifier state as a concurrent healthy-path surface. That duplicates authority instead of leaving one conversation-first live session item in the center workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport, ownership, `liveRun`, transcript live activity, and `autonomySummary` data instead of adding a new backend or transport path.
- Keep the change bounded to healthy selected-thread presentation and side-panel reduction.
- Make the center timeline live item the only healthy autonomy authority surface.
- Keep degraded reconnect, polling fallback, ownership loss, and switch states visibly non-owned so they cannot look like healthy live progression.

## Deliverable

Define and verify one healthy selected-thread SSE path where the center timeline shows the only autonomy authority item and the side-panel autonomy detail stays secondary-only outside that healthy state, while degraded states remain clearly non-owned.
