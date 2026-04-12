# Factory Runtime Spec

## Iteration

- current iteration: `229`
- bounded focus: `resolve the selected-thread submit-to-first-append handoff gap`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, switch continuity, restore continuity, the selected-thread session-stream contract, and deployed single-authority proof are already present. The remaining bounded gap is the submit-to-first-append handoff window: the selected-thread workspace must show one explicit handoff owner at a time so the user never has to infer whether the request was accepted, generating, or stalled.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting composer submit to flow directly into one visible realtime handoff state rather than a silent gap between request acceptance and first assistant output.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread submit-to-first-append handoff path in the active workspace.
- Reuse the current pending outgoing state, inline session block, composer-adjacent activity bar, and selected-thread SSE ownership datasets; do not broaden transport, store logic, or multi-surface ownership rules.
- Keep the center conversation shell and bottom-fixed composer mounted through the full handoff path.
- Allow exactly one temporary pending outbound user turn or exactly one temporary assistant placeholder at a time, never both.
- Clear the handoff owner immediately on first real assistant SSE append, terminal failure, idle reset, polling fallback, reconnect downgrade, or intentional thread switch.
- Keep degraded fallback, restore, and switch behavior on the current fail-open path.

## Deliverable

Expose one conversation-first selected-thread workspace where the submit-to-first-append interval is represented by one explicit handoff owner at a time and clears cleanly when real assistant SSE content arrives.
