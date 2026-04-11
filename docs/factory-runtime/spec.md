# Factory Runtime Spec

## Iteration

- current iteration: `153`
- bounded focus: `collapse selected-thread center-pane realtime status surfaces into one transcript-native session timeline item`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center pane still duplicates realtime session ownership between the transcript live activity and a separate inline session block, which weakens the conversation-first session feel and forces the operator to reconcile two center-pane status surfaces.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the active conversation itself to read like one continuous live session without inferring which center-pane block is authoritative.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread center render path plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, header ownership rules, footer ownership rules, or rail mirroring beyond the center-pane convergence work.
- Reuse the existing selected-thread session, autonomy, phase, and verifier models.
- Keep the center pane transcript-native and avoid adding a second authority surface.
- Render exactly one selected-thread session timeline item for healthy, handoff, degraded, or restore states.
- Clear duplicate center-pane ownership immediately on reconnect downgrade, polling fallback, switch, terminal idle, deselection, or thread loss of authority.
- Never make a non-selected thread appear live-owned.

## Deliverable

Collapse the selected-thread center-pane realtime status surfaces into one transcript-native session timeline item so healthy, handoff, degraded, and restore session progress is expressed through a single machine-readable selected-thread session block with fail-closed clearing on degraded or lost-authority paths.
