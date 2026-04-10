# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace now presents one consistent live session across transcript, header, rail, and footer, but the submit handoff still triggers an eager healthy-path state poll before the append stream takes over. That snapshot refresh weakens the Codex-like realtime feel because startup can still depend on polling even when the intended selected-thread SSE path is healthy and already connecting.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread ownership, append-stream, handoff, live-run, and composer-owner contracts instead of adding a new backend or transport path.
- Keep the change bounded to the submit handoff and degraded-only polling boundary.
- Keep the healthy path conversation-first: local pending user turn, pending assistant placeholder, composer owner row, and transcript-tail live activity should be enough to carry startup without a snapshot refresh.
- Only start or resume polling when EventSource is unavailable, reconnect begins, ownership is lost, or the append stream downgrades away from selected-thread SSE authority.

## Deliverable

Define and verify one healthy submit path where the selected-thread session stays on handoff plus append-SSE startup without an eager poll, while degraded reconnect, unavailable EventSource, ownership loss, and polling fallback still activate the existing recovery path explicitly.
