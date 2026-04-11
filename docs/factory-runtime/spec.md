# Factory Runtime Spec

## Iteration

- current iteration: `116`
- bounded focus: `left-rail active-session row mirrors selected-thread switching, handoff, and healthy live follow state`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, switching continuity, transcript session-lane visibility, and composer utility ergonomics are already established. The remaining gap is left-rail session mirroring: operators still have to infer which selected thread is actively switching, handed off, or live-owned from the center pane instead of seeing one compact selected-thread mirror above the thread list.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread session authority, transcript session lane, composer strip, detached follow, and polling-fallback contracts unchanged.
- Do not introduce a new transport, polling path, backend switch protocol, or a second live-status surface.
- Reuse the existing `threadTransition`, selected-thread session-status, summary-row, and follow-state datasets instead of creating another rail authority source.
- Show at most one sticky active-session row above the thread list for the selected thread only.
- Mirror switching or attach, handoff, and healthy live follow states through chip-first row text and datasets.
- Clear the row immediately on reconnect downgrade, polling fallback, terminal idle, deselection, or any non-selected context.
- Keep non-selected rows snapshot-only and preserve degraded, restore, and empty behavior from earlier iterations.

## Deliverable

Define and verify one sticky active-session rail contract where the selected thread alone mirrors switching or attach, handoff, and healthy live follow state above the thread list through existing selected-thread datasets, while degraded and non-selected paths clear that mirror immediately.
