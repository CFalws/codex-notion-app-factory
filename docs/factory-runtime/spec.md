# Factory Runtime Spec

## Iteration

- current iteration: `209`
- bounded focus: `collapse footer proposal controls behind a compact utility affordance`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, switch continuity, healthy-path SSE authority, and healthy-path secondary-card suppression are already present, but the footer still reads like a request executor control cluster because apply and auto-open sit in the default composer surface. The remaining bounded risk is that those secondary controls compete visually with the chat-first composer instead of staying tucked behind a compact utility affordance.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the textarea and primary send action to remain the dominant bottom surface while secondary proposal utilities stay reachable but unobtrusive.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the bottom-fixed composer utility cluster and its browser verification coverage.
- Reuse the current selected-thread session, proposal readiness, and ownership datasets; do not change backend transport, polling, or broader ownership rules.
- Keep the live session strip as the only healthy-path live status owner.
- Collapse apply and auto-open behind a compact utility affordance that stays closed by default and closes on send, switch, app change, reconnect downgrade, polling fallback, and terminal idle.

## Deliverable

Expose one conversation-first selected-thread workspace where the bottom-fixed composer stays visually primary and proposal utilities sit behind a compact default-closed affordance without creating a second ownership surface.
