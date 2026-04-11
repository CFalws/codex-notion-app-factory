# Factory Runtime Spec

## Iteration

- current iteration: `151`
- bounded focus: `restore one compact inline selected-thread session block in the center conversation workspace`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center timeline already has a canonical selected-thread live activity item, but the conversation workspace still lacks the compact inline session anchor that makes the selected thread read like one continuous realtime session instead of a timeline plus peripheral mirrors.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation itself to show the current live session state without relying only on the header, rail, or footer mirrors.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the center-pane inline session block plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, footer ownership rules, or left-rail ownership rules.
- Reuse the existing selected-thread session surface, phase progression, live autonomy, and pending-handoff models.
- Keep the block compact and chip-first instead of adding prose-heavy detail or a second authority source.
- Show the block only for pending assistant handoff or healthy selected-thread SSE-owned live progress.
- Clear the block immediately on reconnect downgrade, polling fallback, terminal idle, deselection, switch, or thread loss of authority.
- Never make a non-selected thread appear live-owned.

## Deliverable

Restore one compact inline selected-thread session block in the conversation workspace so the selected thread exposes machine-readable transport, phase, path, verifier, and blocker state directly from the existing selected-thread session contract while failing closed on degraded or lost-authority paths.
