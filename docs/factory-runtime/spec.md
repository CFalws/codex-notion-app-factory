# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread inline live and degraded markers are now in place, but deployed verification still proves the session surface mostly through static asset inspection plus API and SSE capture. That leaves the browser-visible intended path under-proven.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session datasets and deployed verifier path instead of adding a new transport or runtime API.
- Keep the change bounded to browser-driven deployed verification for the selected-thread session workspace.
- Preserve the current selected-thread-only ownership rules and fail when the browser-visible session surface succeeds only through degraded fallback.

## Deliverable

Define and verify a browser-runtime deployed workspace check that opens the operator console, submits through the composer, and proves healthy SSE ownership, degraded transition markers, bottom-fixed composer continuity, and thread-switch placeholder behavior through the actual selected-thread DOM.
