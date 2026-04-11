# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread attach, resume, and send flows now stay on the intended SSE-owned session path without routine `/api/jobs/{id}` polling, but the operator still has to reconcile duplicate live execution-state rendering between the central conversation surface and the secondary execution-status panel.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to read like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership signals and server-authored session phase model.
- Keep the change bounded to frontend render and layout ownership between the conversation surface and the secondary execution-status panel.
- Let the central live timeline plus composer-adjacent session strip carry healthy selected-thread execution visibility.
- Hide or neutralize duplicate execution-state rendering in the secondary panel only on the healthy selected-thread path.
- Preserve explicit degraded markers when ownership is lost, fallback is active, or the selected thread is no longer on the intended path.
- Do not introduce new polling, new transport, or a second authoritative live-session surface.

## Deliverable

Use the existing selected-thread SSE ownership and session phase signals so healthy attach, resume, send, proposal, review, verify, ready, and applied flows are understandable from the central conversation surface alone, while the secondary execution-status panel only reappears as an explicit degraded or non-owned detail surface.
