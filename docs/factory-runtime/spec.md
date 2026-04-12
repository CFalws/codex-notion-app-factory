# Factory Runtime Spec

## Iteration

- current iteration: `259`
- bounded focus: `collapse healthy selected-thread phase progress into one canonical in-timeline live owner`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, streamed autonomy identity, unified header chrome, merged footer session-composer status, explicit attach authority, and switch continuity are already present. The bounded question for this iteration is center-timeline convergence: whether healthy selected-thread proposal, review, verify, auto-apply, ready, and applied progress still fragment across a live owner plus duplicate session-event cards instead of reading as one canonical live session item.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting healthy selected-thread progress to read as one continuous live session item in the conversation timeline, not as a live owner that must be mentally reconciled with duplicate active-phase session events.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to selected-thread center-timeline convergence and matching verifier artifacts.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the bottom-fixed composer dock and selected-thread shell behavior unchanged.
- Avoid adding a new transport, a new panel, or any second live-detail owner in the center pane.

## Deliverable

Keep healthy selected-thread proposal, review, verify, auto-apply, ready, and applied progress on exactly one canonical in-timeline live owner while suppressing duplicate active-phase session-event cards until terminal or degraded resolution.
Iteration 245: the dominant selected-thread header summary is already the machine-readable live-session ownership signal, carrying owner, path, and phase from canonical session_status plus SSE authority while degrading or clearing immediately on reconnect, polling fallback, switch, or idle completion.
Iteration 248: the bottom-fixed composer keeps a visible selected-thread target row during healthy and transition states, rendering `READY`, `SWITCHING`, or `HANDOFF` from canonical selected-thread session authority and downgrading or clearing immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249: the left-rail active-session row is already the canonical mirror of the currently selected healthy SSE-owned session, exposing owned and canonical cues only for the selected thread and clearing or downgrading immediately on reconnect, polling fallback, idle, terminal, or switch paths.
Iteration 252: the healthy selected-thread runtime path is already session-scoped; deployed verification now terminates on selected-thread `proposal.ready` and SSE phase ordering instead of waiting on `/api/jobs/{id}` or `latest_job_id`.
Iteration 253: the selected-thread footer dock now exposes one merged session-composer bar, with the session strip carrying target, transport, phase, proposal, and follow cues while the separate composer owner row stays hidden as merged state.
Iteration 254: intentional thread switches already keep the selected-thread workspace mounted in this branch, using one compact transition placeholder, preserved composer dock continuity, immediate old-owner clearing, and explicit browser assertions that no generic empty-state flash occurs.
Iteration 259: healthy selected-thread phase progression is already collapsed onto one canonical inline session owner in the transcript timeline, and active SSE session-event cards for those phases are already suppressed while that owner is present.
