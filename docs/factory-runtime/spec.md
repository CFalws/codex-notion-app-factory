# Factory Runtime Spec

## Iteration

- current iteration: `148`
- bounded focus: `mirror the selected-thread healthy SSE session into one compact active-session row in the left rail`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center workspace now behaves more like one live session, but the left rail still makes operators infer whether the selected thread is the active live owner because the active-session row is rebuilt indirectly and clears too aggressively on bounded nonterminal states.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the left rail to mirror the selected thread's live ownership state without prose-heavy status panels or stale cues.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread left-rail active-session row plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, or composer ownership rules.
- Reuse the existing selected-thread session status, shell phase, follow control, and thread-transition datasets.
- Keep the row compact and chip-first instead of adding prose-heavy detail or a second authority surface.
- Show the row only for authoritative selected-thread ownership or bounded selected-thread handoff or switch states.
- Clear or demote the row immediately on reconnect downgrade, polling fallback, terminal idle, deselection, or thread loss of authority.
- Never make a non-selected thread appear live-owned.

## Deliverable

Mirror the selected-thread session into the existing left-rail active-session row so it exposes one compact rail-level live owner surface with selected-thread owner, phase, follow, handoff, and switching cues derived directly from the selected-thread session state and cleared fail-closed when authority is lost.
