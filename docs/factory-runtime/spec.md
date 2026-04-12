# Factory Runtime Spec

## Iteration

- current iteration: `252`
- bounded focus: `prove healthy selected-thread phase and proposal readiness through session-scoped SSE authority without selected-thread job polling`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, unified header chrome, the removal of selected-thread goals-poll authority, compact chip-first session surfaces, footer-dock-only follow ownership, and a unified selected-thread timeline block are already present. The remaining bounded gap for this iteration is proof-path fidelity: the healthy selected-thread runtime path is already session-scoped, but the deployed verifier still waits on job polling instead of terminating on the same selected-thread SSE authority path.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation to feel fully realtime, with healthy phase progression and proposal readiness attributable to the selected-thread SSE session itself rather than to hidden job polling.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to selected-thread session-scoped transport proof and matching verifier artifacts.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the transcript inline session block as the only in-timeline live progress surface.
- Keep non-selected rows snapshot-only and avoid adding a second follow owner.
- Avoid adding a new transport, a new panel, or any second live-detail owner in the center pane.

## Deliverable

Expose one conversation-first selected-thread workspace where healthy selected-thread phase progression and proposal readiness remain sourced from session-status plus append SSE, while deployed verification proves that path directly and no selected-thread job polling or poll-driven refresh is required on the healthy path.
Iteration 245: the dominant selected-thread header summary is already the machine-readable live-session ownership signal, carrying owner, path, and phase from canonical session_status plus SSE authority while degrading or clearing immediately on reconnect, polling fallback, switch, or idle completion.
Iteration 248: the bottom-fixed composer keeps a visible selected-thread target row during healthy and transition states, rendering `READY`, `SWITCHING`, or `HANDOFF` from canonical selected-thread session authority and downgrading or clearing immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249: the left-rail active-session row is already the canonical mirror of the currently selected healthy SSE-owned session, exposing owned and canonical cues only for the selected thread and clearing or downgrading immediately on reconnect, polling fallback, idle, terminal, or switch paths.
Iteration 252: the healthy selected-thread runtime path is already session-scoped; deployed verification now terminates on selected-thread `proposal.ready` and SSE phase ordering instead of waiting on `/api/jobs/{id}` or `latest_job_id`.
