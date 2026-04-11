# Factory Runtime Spec

## Iteration

- current iteration: `155`
- bounded focus: `collapse the selected-thread header into a conversation-first identity surface with one live phase badge`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The transcript, footer, rail, and secondary drawer now mirror the same selected-thread session contract, but the center header still renders a separate session-summary strip above the conversation. That leaves a second status path in the most visible part of the workspace.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the conversation title area to identify the selected thread while exposing at most one compact live phase badge above the transcript.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread center-header render path plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, transcript ownership rules, footer ownership rules, rail mirroring, or secondary-panel behavior.
- Reuse the existing selected-thread session ownership, transport, phase, verifier, blocker, and timeline-authority models.
- Keep the transcript and composer as the primary live session surfaces and remove the standalone summary strip above the transcript.
- Render selected-thread identity through the title area and at most one compact live badge.
- Migrate any required selected-thread datasets from the removed summary strip onto the single header badge.
- Clear stale selected-thread ownership immediately on reconnect downgrade, polling fallback, switch, terminal idle, deselection, or thread loss of authority.
- Never make a non-selected thread appear live-owned.

## Deliverable

Collapse the selected-thread header into a conversation-first identity surface with one compact live phase badge so the center pane no longer presents a second status strip above the transcript.
