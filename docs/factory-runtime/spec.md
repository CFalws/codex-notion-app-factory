# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread ownership contract is already consistent across header, transcript, and left rail, but the fixed composer still relies on a generic activity bar and a separate target row. That makes the action surface weaker than the conversation surface because the user still has to infer whether the current thread is ready, switching, handoff-bound, or degraded from nearby fragments.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread ownership, append-stream, and composer-owner contracts instead of adding a new backend or polling path.
- Keep the change bounded to the composer-adjacent session strip and its verification contract.
- Keep the footer chat-first: one compact target-and-transport strip, not a new status panel.
- Clear or downgrade the composer strip immediately on switch, reconnect, polling fallback, or terminal idle so stale ownership cannot survive.

## Deliverable

Define and verify one compact composer-adjacent session strip that names the current selected thread, exposes `READY`, `SWITCHING`, or `HANDOFF` from existing composer ownership state, mirrors healthy or degraded transport from the canonical selected-thread ownership source, and clears or downgrades immediately on ownership loss.
