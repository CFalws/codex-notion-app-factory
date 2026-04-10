# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread ownership contract is already consistent across header, rail, and composer footer, but healthy live autonomy progress still sits in a separate inline session block instead of the conversation timeline itself. That keeps the center workspace less session-like than the other surfaces because the operator still has to look outside the transcript tail to understand the current live phase.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread ownership, append-stream, live-run, and autonomy-summary contracts instead of adding a new backend or polling path.
- Keep the change bounded to the transcript-tail live activity item and its verification contract.
- Keep the healthy path conversation-first: one current live activity item in the transcript tail, not a new parallel status surface.
- Clear the transcript-tail live item immediately on reconnect downgrade, polling fallback, terminal idle, or thread switch so stale ownership cannot survive.

## Deliverable

Define and verify one compact transcript-tail live activity item that carries the healthy selected-thread autonomy and phase progression inside the conversation timeline, updates in place from the existing SSE-owned session path, and leaves the separate inline session block for degraded or handoff-only states.
