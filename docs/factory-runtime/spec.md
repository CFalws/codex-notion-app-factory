# Factory Runtime Spec

## Iteration

- current iteration: `179`
- bounded focus: `show one healthy selected-thread header session row beside the active conversation title`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center pane already has live timeline and footer-strip signals, but the header still falls back to a hidden summary row and a badge-only fallback. That makes the operator infer current scope, path, ownership, and phase from other surfaces instead of seeing one immediate header-level session summary.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the active conversation header to state the current session ownership at a glance.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread center-header summary seam in the operator console.
- Reuse the existing selected-thread SSE and session model already driving transcript and footer surfaces; do not change transport ownership rules.
- Render exactly one compact chip-first header row for scope, path, ownership, and phase on the healthy selected-thread path.
- Keep the old phase badge as the degraded, reconnect, restore, switch, and non-authoritative fallback.
- Fail closed on degraded, reconnect, polling fallback, restore-gap, deselected, switched, and no-selection states.

## Deliverable

Expose one compact authoritative header session row beside the active conversation title so the operator can read selected-thread scope, path, ownership, and phase without relying on prose-heavy secondary surfaces.
