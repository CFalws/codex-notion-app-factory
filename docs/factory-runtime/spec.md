# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread attach now hydrates from `session.bootstrap`, but transient disconnects still degrade immediately into snapshot-fallback and polling. That breaks the live-session illusion during reconnect, forces the operator to infer whether the selected session actually survived, and makes healthy resume versus degraded takeover harder to verify.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport and keep `conversation.append` events unchanged.
- Keep the change bounded to selected-thread reconnect and resume semantics on top of the existing bootstrap contract.
- Extend the current bootstrap event shape additively instead of creating a new channel or state bus.
- Let healthy selected-thread reconnect resume transcript continuity from the last append cursor on the authoritative stream alone.
- Keep degraded fallback explicit through attach-mode and resume-mode state so snapshot fallback cannot be mistaken for healthy realtime resume.
- Keep degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states visibly non-owned or cleared so they cannot look like stale healthy live progression.

## Deliverable

Define and verify one additive selected-thread SSE resume contract with explicit cursor-based reopen metadata, so healthy reconnect resumes from `session.bootstrap` plus append cursor on the authoritative stream while degraded fallback remains explicit and observable.
