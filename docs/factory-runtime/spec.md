# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread workspace now updates phase and proposal/apply state from SSE-owned events, but the detached-tail state still requires inference because the bottom follow control only appears after backlog arrives. The operator should see immediately when the active live session is paused from the tail, then watch that same control upgrade in place to `NEW` when unseen appends accumulate.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership source, bottom follow control location, and live-follow datasets.
- Keep the change bounded to the detached-tail follow control render contract.
- Clear immediately on jump-to-latest, reconnect downgrade, polling fallback, terminal idle, thread switch, or ownership loss.

## Deliverable

Expose the bottom follow control as the single explicit detached-tail session indicator so healthy selected-thread SSE ownership shows `PAUSED` immediately when detached, upgrades to `NEW` with unseen-count metadata when backlog arrives, and clears deterministically on any ownership or session loss.
