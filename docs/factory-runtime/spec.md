# Factory Runtime Spec

## Iteration

- current iteration: `253`
- bounded focus: `unify the selected-thread footer dock into one canonical session-composer bar`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, unified header chrome, the removal of selected-thread goals-poll authority, a unified selected-thread timeline block, and deployed SSE proof are already present. The remaining bounded gap for this iteration is footer inference: the selected-thread composer area still shows a visible owner row plus a separate session strip, which forces the operator to reconcile two bottom surfaces instead of reading one canonical session-composer bar.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation’s typing surface to read like one fixed live session footer, without split owner-row versus strip inference.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to selected-thread footer dock rendering and matching verifier artifacts.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the transcript inline session block as the only in-timeline live progress surface.
- Keep non-selected rows snapshot-only and avoid adding a second follow owner.
- Avoid adding a new transport, a new panel, or any second live-detail owner in the center pane.

## Deliverable

Expose one conversation-first selected-thread workspace where the bottom composer keeps one canonical session-composer bar carrying target, transport, phase, proposal readiness, and follow state, while the old owner row remains hidden as merged state and no duplicate footer live surface survives healthy, degraded, switching, handoff, or idle paths.
Iteration 245: the dominant selected-thread header summary is already the machine-readable live-session ownership signal, carrying owner, path, and phase from canonical session_status plus SSE authority while degrading or clearing immediately on reconnect, polling fallback, switch, or idle completion.
Iteration 248: the bottom-fixed composer keeps a visible selected-thread target row during healthy and transition states, rendering `READY`, `SWITCHING`, or `HANDOFF` from canonical selected-thread session authority and downgrading or clearing immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249: the left-rail active-session row is already the canonical mirror of the currently selected healthy SSE-owned session, exposing owned and canonical cues only for the selected thread and clearing or downgrading immediately on reconnect, polling fallback, idle, terminal, or switch paths.
Iteration 252: the healthy selected-thread runtime path is already session-scoped; deployed verification now terminates on selected-thread `proposal.ready` and SSE phase ordering instead of waiting on `/api/jobs/{id}` or `latest_job_id`.
Iteration 253: the selected-thread footer dock now exposes one merged session-composer bar, with the session strip carrying target, transport, phase, proposal, and follow cues while the separate composer owner row stays hidden as merged state.
