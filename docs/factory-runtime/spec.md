# Factory Runtime Spec

## Iteration

- current iteration: `212`
- bounded focus: `activate the inline selected-thread session block in the center transcript`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, left-rail mirroring, switch continuity, and healthy-path SSE authority are already present, but the center transcript still keeps the prepared inline session block suppressed and leaves healthy live ownership expressed through adjacent strips rather than the conversation surface itself. The remaining bounded risk is that operators still have to look outside the transcript to understand the current selected-thread session state even though the render path for a compact inline owner block already exists.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the center transcript itself to read like the active realtime session rather than a passive history beside separate status surfaces.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the inline selected-thread session block in the center transcript and its browser verification coverage.
- Reuse the current selected-thread authority, handoff, and phase datasets; do not change backend transport, polling, or broader ownership rules.
- Show exactly one compact inline session block only for healthy selected-thread SSE ownership or pending assistant handoff.
- Clear that block immediately on reconnect downgrade, polling fallback, terminal resolution, deselection, or thread switch.
- Keep degraded fallback, switch placeholders, and restore behavior on the existing fail-open path.
- Keep duplicate live-owner treatment out of competing surfaces on the same healthy path.

## Deliverable

Expose one conversation-first selected-thread workspace where the center transcript shows one compact inline session owner block for healthy or handoff selected-thread progress without introducing duplicate live-owner surfaces.
