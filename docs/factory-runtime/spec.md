# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread SSE path already owns the session workspace and now exposes exact phase cues, but the header summary row, composer owner row, and composer-adjacent strip still lean on helper prose more than chip-first target-first scanning. That leaves a small but real inference cost: the operator can see the session is live, but still has to read instead of scan for owner, target, readiness, and current phase.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread ownership, liveRun, session-summary, and composer-strip contracts instead of adding a new backend or transport path.
- Keep the change bounded to healthy selected-thread phase presentation in the header and composer-adjacent strip.
- Keep the healthy path chip-first, target-first, and conversation-first: exact phase labels should appear on the existing surfaces without creating a new panel or new polling authority.
- Keep degraded reconnect, polling fallback, ownership loss, and switch states visibly non-owned so they cannot look like healthy live progression.

## Deliverable

Define and verify one healthy selected-thread SSE path where the header summary row, composer owner row, and composer-adjacent strip present owner, target, readiness, and phase in compact chip-first language, while degraded states remain clearly non-owned.
