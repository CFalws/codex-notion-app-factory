# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has a healthy selected-thread ownership signal in the header, but the left rail still carries its own live-session taxonomy. That duplication makes ownership ambiguous because the rail can out-signal the canonical selected-thread SSE owner state instead of mirroring it.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing `selectedThreadLiveSessionIndicator` ownership contract instead of adding a new rail-only state machine.
- Keep the change bounded to left-rail ownership presentation and its verification contract.
- Do not add new polling behavior, phase vocabulary, or a secondary rail-only status taxonomy.
- Clear the rail mirror immediately on switch, reconnect, polling fallback, or terminal idle so stale ownership cannot survive.

## Deliverable

Define and verify one compact healthy-only left-rail mirror that appears only when the selected thread is the active SSE-owned live session, derives its state from the same canonical ownership source as the header, and clears immediately on any ownership loss or degraded path.
