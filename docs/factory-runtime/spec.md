# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread attach, resume, switch, and submit handoff are now bounded, but the healthy active run still lets routine `/api/jobs/{id}` polling remain eligible after the selected-thread session has already moved onto the authoritative SSE path.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE authority signals and server-authored session phase model.
- Keep the change bounded to frontend job ownership and polling behavior.
- Suppress routine `/api/jobs/{id}` polling only while the selected thread remains on the healthy SSE-owned active-session path.
- Re-enable polling only for explicit degraded conditions such as reconnect fallback, ownership loss, stale-or-missing freshness, or off-thread tracking.
- Do not introduce a new transport, new layout, or a second live-status surface.

## Deliverable

Use the existing selected-thread SSE authority and session phase signals so healthy attach, resume, and send flows stay fully SSE-owned for the active run without routine `/api/jobs/{id}` polling, while degraded conditions explicitly reopen the polling fallback path.
