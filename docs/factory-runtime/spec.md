# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread timeline is now the canonical healthy live surface, but surrounding visible status still falls back to polled job or goal state too often. That lag makes proposal, verify, apply, and recent activity feel less like one live session even when the selected thread is already healthy and SSE-owned.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append-stream ownership, conversation events, live-run phase derivation, and single timeline session surface instead of introducing a new runtime state source.
- Keep polling as an explicit degraded fallback for reconnect, polling mode, thread switch, ownership loss, or non-selected threads.
- Keep the bottom-fixed composer and selected-thread workspace structure unchanged.

## Deliverable

Promote healthy selected-thread SSE events to the canonical owner for visible phase chips, proposal/apply readiness, and recent activity so those surfaces update from the selected conversation event stream immediately while healthy SSE ownership holds, and fall back to the existing polled path only when ownership is lost or degraded.
