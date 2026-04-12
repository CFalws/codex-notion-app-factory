# Factory Runtime Spec

## Iteration

- current iteration: `228`
- bounded focus: `preserve one continuous workspace during intentional selected-thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, handoff continuity, restore continuity, the selected-thread session-stream contract, and deployed single-authority proof are already present. The remaining bounded gap is durable switch continuity: intentional selected-thread changes must keep one mounted workspace surface, clear old-thread ownership immediately, and avoid any empty-state or duplicate-owner flash while the next snapshot attaches.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting thread changes to feel like one continuous Codex-style session surface instead of a reset, stall, or ambiguous empty workspace.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread switch path in the conversation-first workspace.
- Reuse the current thread-transition placeholder, selected-thread ownership datasets, and mounted composer shell; do not broaden transport, store logic, or multi-surface ownership rules.
- Keep the center conversation shell and bottom-fixed composer mounted through the full switch path.
- Clear prior thread live, phase, proposal, and follow ownership immediately when switching starts.
- Show exactly one compact selected-thread transition placeholder until the target snapshot attaches.
- Keep reconnect, polling fallback, deselection, restore, and terminal behavior on the current fail-open path.

## Deliverable

Expose one conversation-first selected-thread workspace where intentional thread switches preserve the mounted shell and composer, clear old-thread ownership immediately, and show only one compact transition placeholder before the new snapshot attaches.
