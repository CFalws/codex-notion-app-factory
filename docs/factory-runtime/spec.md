# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread SSE path already owns the session workspace, but the header badge and composer-adjacent strip still rely on generic running wording in places where the exact autonomy phase is already known. That leaves a small but real inference gap: the operator can tell the session is live, but still has to inspect deeper surfaces to know whether the system is proposing, reviewing, verifying, auto-applying, ready, or applied.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread ownership, liveRun, session-summary, and composer-strip contracts instead of adding a new backend or transport path.
- Keep the change bounded to healthy selected-thread phase presentation in the header and composer-adjacent strip.
- Keep the healthy path chip-first and conversation-first: exact phase labels should appear on the existing surfaces without creating a new panel or new polling authority.
- Keep degraded reconnect, polling fallback, ownership loss, and switch states visibly non-owned so they cannot look like healthy live progression.

## Deliverable

Define and verify one healthy selected-thread SSE path where the header and composer-adjacent strip show explicit PROPOSAL, REVIEW, VERIFY, AUTO APPLY, READY, and APPLIED progression with concise detail copy, while degraded states remain clearly non-owned.
