# Factory Runtime Spec

## Iteration

- current iteration: `101`
- bounded focus: `selected-thread autonomy authority from healthy SSE session state`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread restore stage and single healthy center-pane live surface are now canonical, but autonomy blocker, path, verifier, and apply state can still refresh from `/api/goals` even when the selected thread already owns healthy SSE session authority. That weakens the conversation-first session model because healthy success can still look polling-backed instead of session-backed.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session-status, live-autonomy, phase-progression, restore-stage, and handoff helpers in the frontend store.
- Do not introduce a new transport or a new polling contract.
- Keep exactly one live-owned center-pane session surface during healthy selected-thread SSE progress.
- Preserve the bottom-fixed composer, restore stage, thread-switch clearing, degraded reconnect or polling markers, and rail behavior already established in earlier iterations.
- Do not change transport contracts or the render layout in this iteration.
- Allow `/api/goals` refresh only after explicit degraded transport, missing selected-thread session authority, or stale-or-missing bootstrap autonomy data.

## Deliverable

Define and verify one selected-thread autonomy authority contract where healthy session bootstrap plus live append events own blocker, path, verifier, and apply progress, and `/api/goals` remains a degraded fallback only when the selected-thread SSE path is missing, stale, or explicitly downgraded.
