# Factory Runtime Spec

## Iteration

- current iteration: `167`
- bounded focus: `mirror the canonical selected-thread session into one sticky active-session row above the conversation list`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center-pane and composer surfaces now expose selected-thread session ownership more clearly, but the left navigator still does not keep a persistent sticky active-session row during switching or handoff. Operators can still lose at-a-glance session context while scanning the conversation list.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the left rail to keep a persistent selected-thread session marker that agrees with the center pane.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the sticky active-session row above the conversation list.
- Reuse the existing selected-thread canonical session seam; do not add a new authority source or make non-selected threads look live-owned.
- Keep the row chip-first, selected-thread-only, and fail closed on idle, terminal completion, reconnect downgrade, polling fallback, deselection, lost authority, or switch resolution.
- Keep switching visible only while the intentional selected-thread switch is active.

## Deliverable

Render one sticky active-session row above the conversation list that mirrors only the selected-thread session state with compact owner, state, and follow cues, including bounded switching visibility and immediate clearing on degraded or idle paths.
