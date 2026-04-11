# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread execution visibility now stays on the intended central SSE-owned surface, but the remaining session chrome still uses helper-style summary text that makes the operator read prose instead of fixed session vocabulary.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to read like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership signals and server-authored session phase datasets.
- Keep the change bounded to the session summary row, composer owner row, and composer-adjacent session strip.
- Replace healthy-path helper copy with fixed chip-first, target-first vocabulary for owner, path, phase, follow, and proposal readiness.
- Preserve explicit short degraded copy for reconnect, polling fallback, session rotation, and thread-switch states.
- Keep existing machine-readable datasets available for browser-proof assertions.
- Do not introduce new transport, new status surfaces, or new polling dependencies.

## Deliverable

Use the existing selected-thread SSE ownership and phase signals so healthy attach, resume, send, proposal, review, verify, ready, and applied flows read through fixed session tokens in the center chrome, while degraded and switching states remain explicit through short downgrade vocabulary.
