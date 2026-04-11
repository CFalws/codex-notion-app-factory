# Factory Runtime Spec

## Iteration

- current iteration: `156`
- bounded focus: `refine the selected-thread header badge so it carries both phase and live path state`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center header is now down to one compact badge, but that badge still makes users infer whether the selected-thread session is healthy SSE-owned or degraded from lower surfaces. The badge needs to carry both phase and path state directly.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the conversation title area to identify the selected thread while exposing one compact badge that immediately says both what phase the session is in and whether it is healthy, degraded, restoring, or switching.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread center-header badge mapping plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, transcript ownership rules, footer ownership rules, rail mirroring, or secondary-panel behavior.
- Reuse the existing selected-thread session ownership, transport, phase, verifier, blocker, and timeline-authority models.
- Keep the transcript and composer as the primary live session surfaces and preserve the one-badge-only header contract.
- Render selected-thread identity through the title area and one compact live badge that combines phase with path state.
- Keep all required selected-thread datasets on the single header badge.
- Clear stale selected-thread ownership immediately on reconnect downgrade, polling fallback, switch, terminal idle, deselection, or thread loss of authority.
- Never make a non-selected thread appear live-owned.

## Deliverable

Refine the selected-thread header badge so it remains the only header status surface while directly showing selected-thread phase plus live ownership or degraded path state.
