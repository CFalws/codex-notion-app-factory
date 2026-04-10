# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread attach, reconnect, and phase ownership are now bounded, but intentional thread switches still need explicit continuity evidence. The workspace should keep one mounted shell and composer during switch, clear old-thread live ownership immediately, and carry a single compact switching placeholder without letting stale phase datasets or empty-state fallback leak into the selected-thread experience.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread switch, attach, and authoritative phase datasets.
- Keep the change bounded to intentional selected-thread switching in the existing conversation-first shell.
- Do not add new inferred phases or parallel status panels.
- Keep the center conversation shell and bottom-fixed composer mounted through switch.
- Clear old-thread live ownership immediately and mark switching state as non-authoritative.
- Use one compact switch placeholder and clear it as soon as the new selected thread attaches or degrades.

## Deliverable

Define and verify one compact selected-thread switch continuity contract so intentional thread changes keep the shell mounted, preserve the composer dock, expose one switching placeholder, and explicitly reset phase ownership to non-authoritative `UNKNOWN` until the new selected thread attaches.
