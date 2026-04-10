# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread SSE stream only emits append envelopes today, so initial attach still depends on a separate conversation snapshot fetch. That forces the workspace to infer initial transcript, phase, and composer ownership from a mixed attach path instead of hydrating directly from the authoritative selected-thread stream, and it makes healthy attach versus degraded snapshot fallback harder to verify.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport and keep `conversation.append` events unchanged.
- Keep the change bounded to selected-thread bootstrap semantics, attach-mode signaling, and compatible client hydration.
- Add one versioned bootstrap event shape to the current stream instead of creating a new channel or state bus.
- Let healthy selected-thread attach hydrate transcript continuity, append cursor, live phase summary, and composer ownership from the bootstrap event alone.
- Keep degraded fallback explicit through attach-mode state so snapshot fallback cannot be mistaken for healthy realtime attach.
- Keep degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states visibly non-owned or cleared so they cannot look like stale healthy live progression.

## Deliverable

Define and verify one additive selected-thread `session.bootstrap` SSE contract with explicit versioning and attach mode, plus a compatible attach path that hydrates from that bootstrap on the healthy path and marks snapshot fallback explicitly when bootstrap is unavailable.
