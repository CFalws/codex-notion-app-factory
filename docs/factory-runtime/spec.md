# Factory Runtime Spec

## Iteration

- current iteration: `92`
- bounded focus: `canonical selected-thread session-status contract`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread session ownership is still derived in multiple frontend surfaces with slightly different handoff, reconnect, polling, and clear conditions. That makes the header, composer-adjacent strip, inline live block, and left-rail active-session row drift apart even when they are all reflecting the same selected-thread state.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Move selected-thread session-status ownership into `ops-store.js` and treat `ops-render.js`, `ops-conversations.js`, and `ops-jobs.js` as read-only consumers.
- Reuse existing append-stream, pending-handoff, session-phase, live-follow, and thread-transition state; do not introduce a new transport or a new polling contract.
- Keep healthy SSE owner, reconnect downgrade, polling fallback, handoff, attach, and clear reasons finite and machine-readable.
- Preserve the bottom-fixed composer, center transcript card, and rail behavior already established in earlier iterations.
- Do not suppress `/api/jobs` or `/api/goals` polling in this iteration; only surface degraded ownership consistently so later iterations can tighten fallback safely.

## Deliverable

Define and verify one canonical selected-thread session-status model in `ops-store.js`, then have the center header, composer target row or strip, inline live block, and left-rail active-session row all consume that model so ownership and downgrade behavior stay consistent from bootstrap through append projection and negative cases.
