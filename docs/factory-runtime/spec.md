# Factory Runtime Spec

## Iteration

- current iteration: `205`
- bounded focus: `preserve one mounted selected-thread workspace during intentional thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership and explicit autonomy milestones are already present, but a Codex-desktop-style realtime session still depends on thread switches feeling continuous. The remaining bounded risk is that an intentional switch could appear to drop the session shell, flash a generic empty workspace, or leave stale owner residue instead of behaving like one mounted session surface bridging to the next thread.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting thread switches to preserve the same mounted conversation shell and fixed composer instead of looking like the session disappeared.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread switch path, the existing workspace placeholder and transition helpers, and the focused browser verification seam.
- Reuse the current selected-thread session status, thread transition, and mounted composer shell behavior; do not change transport or broader multi-thread ownership rules.
- During an intentional selected-thread switch, keep the conversation shell and bottom-fixed composer mounted, clear old ownership immediately, and show at most one compact switching placeholder until the new snapshot attaches.
- Reserve the generic empty workspace for true no-conversation idle only.

## Deliverable

Expose one conversation-first selected-thread workspace where intentional thread switches preserve the mounted shell and fixed composer, clear stale owner chrome immediately, and bridge with one compact switching placeholder instead of an empty-state flash.
