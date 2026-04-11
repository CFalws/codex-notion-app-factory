# Factory Runtime Spec

## Iteration

- current iteration: `152`
- bounded focus: `wire the existing left-rail sticky active-session row to selected-thread session authority`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center workspace now exposes the selected-thread session more directly, but the left rail still needs one immediate sticky row that mirrors current selected-thread ownership, phase, and follow or unseen state without stale switching or degraded ownership.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the left rail to show the current selected-thread live owner, phase, and follow state without inferring whether the sticky row is stale.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the left-rail sticky active-session row plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, center-pane ownership rules, footer ownership rules, or card or chip ownership models beyond the sticky row.
- Reuse the existing selected-thread session status, shell phase, and follow-control models.
- Keep the row compact and chip-first instead of adding prose-heavy detail or a second rail authority source.
- Show the row only for healthy selected-thread ownership or bounded selected-thread handoff.
- Clear the row immediately on reconnect downgrade, polling fallback, switch, terminal idle, deselection, or thread loss of authority.
- Never make a non-selected thread appear live-owned.

## Deliverable

Wire the existing left-rail sticky active-session row to selected-thread session authority so it exposes one compact owner, phase, and follow or unseen mirror derived directly from the existing selected-thread session contract while failing closed on degraded or lost-authority paths.
