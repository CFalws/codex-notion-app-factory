# Factory Runtime Spec

## Iteration

- current iteration: `204`
- bounded focus: `extend the selected-thread live timeline into one explicit autonomy progression lane`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread path now has a stable authority contract and a composer-authoritative session bar, but the center timeline still compresses autonomy progression too aggressively. `AUTO APPLY` is not explicit in the milestone lane, so proposal, review, verify, apply, ready, and applied progression still requires some inference instead of reading one compact live lane.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected-thread center timeline to explain live proposal progression at a glance without reading prose-heavy side panels.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread live timeline lane, the existing shared selected-thread authority model, and the focused verification seam.
- Reuse the current selected-thread autonomy and milestone helpers; do not change transport or broaden session ownership scope.
- On the healthy selected-thread path, expose explicit `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED` milestone states in the center timeline lane.
- Keep degraded, handoff, reconnect, polling fallback, switch, deselection, restore-gap loss, and terminal-clear behavior unchanged.

## Deliverable

Expose one conversation-first selected-thread workspace where the healthy selected-thread center timeline includes one explicit machine-readable autonomy progression lane with all major proposal phases visible in realtime.
