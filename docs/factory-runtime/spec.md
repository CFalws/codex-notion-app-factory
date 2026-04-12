# Factory Runtime Spec

## Iteration

- current iteration: `254`
- bounded focus: `keep the selected-thread workspace mounted during intentional thread switches`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, unified header chrome, the removal of selected-thread goals-poll authority, a unified selected-thread timeline block, deployed SSE proof, and the merged footer session-composer bar are already present. The bounded question for this iteration is switch continuity: whether an intentional thread change still drops the selected workspace to a generic empty reset instead of preserving one continuous selected-thread shell until the incoming snapshot binds.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting an intentional thread change to preserve one continuous selected-thread shell, center timeline, and bottom-fixed composer instead of flashing a generic empty reset.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to selected-thread switch continuity and matching verifier artifacts.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the center timeline switch placeholder compact and canonical.
- Keep the bottom-fixed composer dock mounted through the transition.
- Avoid adding a new transport, a new panel, or any second live-detail owner in the center pane.

## Deliverable

Keep the selected-thread workspace mounted during intentional thread switches so the center conversation and bottom-fixed composer remain one continuous realtime session surface, with exactly one compact canonical switch placeholder and no generic empty-state reset.
Iteration 245: the dominant selected-thread header summary is already the machine-readable live-session ownership signal, carrying owner, path, and phase from canonical session_status plus SSE authority while degrading or clearing immediately on reconnect, polling fallback, switch, or idle completion.
Iteration 248: the bottom-fixed composer keeps a visible selected-thread target row during healthy and transition states, rendering `READY`, `SWITCHING`, or `HANDOFF` from canonical selected-thread session authority and downgrading or clearing immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249: the left-rail active-session row is already the canonical mirror of the currently selected healthy SSE-owned session, exposing owned and canonical cues only for the selected thread and clearing or downgrading immediately on reconnect, polling fallback, idle, terminal, or switch paths.
Iteration 252: the healthy selected-thread runtime path is already session-scoped; deployed verification now terminates on selected-thread `proposal.ready` and SSE phase ordering instead of waiting on `/api/jobs/{id}` or `latest_job_id`.
Iteration 253: the selected-thread footer dock now exposes one merged session-composer bar, with the session strip carrying target, transport, phase, proposal, and follow cues while the separate composer owner row stays hidden as merged state.
Iteration 254: intentional thread switches already keep the selected-thread workspace mounted in this branch, using one compact transition placeholder, preserved composer dock continuity, immediate old-owner clearing, and explicit browser assertions that no generic empty-state flash occurs.
