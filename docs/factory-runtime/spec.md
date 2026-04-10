# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership, polling suppression, and switch continuity are now in place, but adjacent session state still partially waits on the polling loop. The append stream is live while goal-summary and job-meta refresh can still lag behind, which weakens the single-session realtime feel.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE path and selected-thread-only ownership guardrails instead of extending realtime semantics beyond the active conversation.
- Keep the change bounded to immediate selected-session synchronization across append handling and polling fallback ownership.
- Preserve polling as an explicit degraded fallback whenever SSE ownership is absent, reconnecting, or lost.

## Deliverable

Define and verify that healthy selected-thread append events immediately refresh visible job phase, proposal readiness, verifier progress, and autonomy summary state without waiting for the 3-second polling loop.
