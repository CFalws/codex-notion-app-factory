# Factory Runtime Spec

## Iteration

- current iteration: `262`
- bounded focus: `collapse healthy selected-thread composer-adjacent session chrome behind the canonical center timeline owner`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, streamed autonomy identity, unified header chrome, merged footer session-composer status, explicit attach authority, switch continuity, restore continuity, and the one-owner healthy timeline are already present. The bounded question for this iteration is composer-adjacent duplication: whether the healthy selected-thread footer strip still shows duplicate ownership, transport, phase, and autonomy chrome beside the fixed composer even though the center timeline is already the canonical live session surface.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected-thread conversation timeline to read as the one canonical live session surface, with the bottom-fixed composer remaining attached and usable without a second healthy status strip competing for attention beside it.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to the selected-thread presentation boundary between the center live timeline and the composer-adjacent strip.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the bottom-fixed composer dock, selected-thread shell, and one-owner timeline behavior unchanged.
- Avoid adding a new transport, a new panel, or a second healthy live-detail owner beside the composer.

## Deliverable

Keep the healthy selected-thread center timeline as the sole visible live session owner while suppressing duplicate healthy session-strip chrome beside the composer, and preserve explicit strip visibility only for degraded, restore, handoff, terminal, or follow-only exception paths.
Iteration 245: the dominant selected-thread header summary is already the machine-readable live-session ownership signal, carrying owner, path, and phase from canonical session_status plus SSE authority while degrading or clearing immediately on reconnect, polling fallback, switch, or idle completion.
Iteration 248: the bottom-fixed composer keeps a visible selected-thread target row during healthy and transition states, rendering `READY`, `SWITCHING`, or `HANDOFF` from canonical selected-thread session authority and downgrading or clearing immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249: the left-rail active-session row is already the canonical mirror of the currently selected healthy SSE-owned session, exposing owned and canonical cues only for the selected thread and clearing or downgrading immediately on reconnect, polling fallback, idle, terminal, or switch paths.
Iteration 252: the healthy selected-thread runtime path is already session-scoped; deployed verification now terminates on selected-thread `proposal.ready` and SSE phase ordering instead of waiting on `/api/jobs/{id}` or `latest_job_id`.
Iteration 253: the selected-thread footer dock now exposes one merged session-composer bar, with the session strip carrying target, transport, phase, proposal, and follow cues while the separate composer owner row stays hidden as merged state.
Iteration 254: intentional thread switches already keep the selected-thread workspace mounted in this branch, using one compact transition placeholder, preserved composer dock continuity, immediate old-owner clearing, and explicit browser assertions that no generic empty-state flash occurs.
Iteration 259: healthy selected-thread phase progression is already collapsed onto one canonical inline session owner in the transcript timeline, and active SSE session-event cards for those phases are already suppressed while that owner is present.
Iteration 260: selected-thread restore and reselect are already session-scoped in this branch; restore enters explicit `awaiting-bootstrap` or `sse-resume`, keeps the selected-thread shell and composer mounted, resolves healthy ownership through `session.bootstrap` or append SSE, and already rejects early current-thread job or goals polling in the deployed browser gate.
Iteration 262: healthy selected-thread composer-adjacent session chrome is now suppressed in this branch; the fixed composer remains attached to the selected session, but the adjacent strip no longer renders duplicate healthy ownership, transport, phase, or detail state while degraded, restore, handoff, terminal, and follow-only exception paths still retain explicit strip visibility.
