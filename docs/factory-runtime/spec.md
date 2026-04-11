# Factory Runtime Spec

## Iteration

- current iteration: `143`
- bounded focus: `make one canonical center-timeline live-session item the primary selected-thread authority and demote duplicate center-lane status prose`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already has authoritative SSE-backed session data, but the center lane still lets the header summary row, autonomy detail, and execution status prose compete with the timeline live item. That makes operators infer which surface is authoritative instead of reading one obvious session timeline item.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change presentation-only in `ops-render.js` plus focused verifier and doc updates.
- Do not introduce a new transport, polling heuristic, backend protocol, or composer contract change.
- Reuse the existing selected-thread session surface, phase progression, autonomy summary, and degraded-path rules.
- Keep non-selected threads snapshot-only.
- Preserve reconnect, polling fallback, restore, switch, deselection, and terminal states as immediate downgrade or clear paths in the same render cycle.

## Deliverable

Define one explicit center-timeline authority predicate for the selected thread and use it to demote duplicate selected-thread summary and status prose, so the center lane reads as one authoritative live-session item across healthy, degraded, restore, and handoff states.
