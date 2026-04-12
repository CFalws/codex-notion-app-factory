# Factory Runtime Spec

## Iteration

- current iteration: `242`
- bounded focus: `make the left-rail active-session row an explicit canonical mirror of selected-thread session-status plus SSE authority`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, unified header chrome, the removal of selected-thread goals-poll authority, compact chip-first session surfaces, and footer-dock-only follow ownership are already present. The remaining bounded gap is left-rail authority attribution: the sticky active-session row is visible, but healthy selected-thread ownership is not yet explicitly marked canonical even though it is already sourced from the selected-thread session-status plus SSE path.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the active selected conversation to remain visibly live while scanning the left rail, without any non-selected thread appearing live-owned.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to left-rail active-session row ownership attribution in the store and verifier artifacts.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the transcript inline session block as the only in-timeline live progress surface.
- Keep non-selected rows snapshot-only and avoid adding a second follow owner.
- Avoid adding a new transport, a new panel, or any second live-detail owner in the center pane.

## Deliverable

Expose one conversation-first selected-thread workspace where the sticky left-rail active-session row is an explicit canonical mirror of selected-thread owner, phase, and follow state from `session_status` plus SSE, while degraded and switched paths still clear it immediately and non-selected rows remain snapshot-only.
Iteration 245: the dominant selected-thread header summary is already the machine-readable live-session ownership signal, carrying owner, path, and phase from canonical session_status plus SSE authority while degrading or clearing immediately on reconnect, polling fallback, switch, or idle completion.
Iteration 248: the bottom-fixed composer keeps a visible selected-thread target row during healthy and transition states, rendering `READY`, `SWITCHING`, or `HANDOFF` from canonical selected-thread session authority and downgrading or clearing immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249: the left-rail active-session row is already the canonical mirror of the currently selected healthy SSE-owned session, exposing owned and canonical cues only for the selected thread and clearing or downgrading immediately on reconnect, polling fallback, idle, terminal, or switch paths.
