# Factory Runtime Spec

## Iteration

- current iteration: `267`
- bounded focus: `prove selected-thread session-scoped realtime ownership end to end through one deployed browser scenario matrix`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, streamed autonomy identity, unified header chrome, merged footer session-composer status, explicit attach authority, restore continuity, switch continuity, and the one-owner healthy timeline are already present. The bounded question for this iteration is intended-path proof completeness: whether the deployed browser verifier already covers the selected thread as one session-scoped realtime owner across healthy streaming, switch transition, restore or resume, pending handoff, and degraded fallback without leaving blind spots where polling-owned success or hidden degraded recovery could still masquerade as correct success.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the runtime to prove, not merely claim, that the selected-thread conversation behaves like one Codex-style live session owner across healthy streaming, restore, switch, handoff, and degraded paths.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to deployed verification coverage and durable proposal artifacts.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the bottom-fixed composer dock, selected-thread shell, and one-owner healthy timeline behavior unchanged.
- Avoid widening transport or UI ownership just to satisfy verification; the verifier must prove the existing intended path.

## Deliverable

Keep one deployed browser scenario matrix that proves selected-thread realtime ownership across healthy streaming, restore or resume, degraded fallback, intentional thread switch, and cancelled switch, with explicit negative assertions that polling-owned authority, stale ownership, hidden degraded recovery, or generic empty-state flashes do not pass as healthy success.
Iteration 245: the dominant selected-thread header summary is already the machine-readable live-session ownership signal, carrying owner, path, and phase from canonical session_status plus SSE authority while degrading or clearing immediately on reconnect, polling fallback, switch, or idle completion.
Iteration 248: the bottom-fixed composer keeps a visible selected-thread target row during healthy and transition states, rendering `READY`, `SWITCHING`, or `HANDOFF` from canonical selected-thread session authority and downgrading or clearing immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249: the left-rail active-session row is already the canonical mirror of the currently selected healthy SSE-owned session, exposing owned and canonical cues only for the selected thread and clearing or downgrading immediately on reconnect, polling fallback, idle, terminal, or switch paths.
Iteration 252: the healthy selected-thread runtime path is already session-scoped; deployed verification now terminates on selected-thread `proposal.ready` and SSE phase ordering instead of waiting on `/api/jobs/{id}` or `latest_job_id`.
Iteration 253: the selected-thread footer dock now exposes one merged session-composer bar, with the session strip carrying target, transport, phase, proposal, and follow cues while the separate composer owner row stays hidden as merged state.
Iteration 254: intentional thread switches already keep the selected-thread workspace mounted in this branch, using one compact transition placeholder, preserved composer dock continuity, immediate old-owner clearing, and explicit browser assertions that no generic empty-state flash occurs.
Iteration 259: healthy selected-thread phase progression is already collapsed onto one canonical inline session owner in the transcript timeline, and active SSE session-event cards for those phases are already suppressed while that owner is present.
Iteration 260: selected-thread restore and reselect are already session-scoped in this branch; restore enters explicit `awaiting-bootstrap` or `sse-resume`, keeps the selected-thread shell and composer mounted, resolves healthy ownership through `session.bootstrap` or append SSE, and already rejects early current-thread job or goals polling in the deployed browser gate.
Iteration 262: healthy selected-thread composer-adjacent session chrome is now suppressed in this branch; the fixed composer remains attached to the selected session, but the adjacent strip no longer renders duplicate healthy ownership, transport, phase, or detail state while degraded, restore, handoff, terminal, and follow-only exception paths still retain explicit strip visibility.
Iteration 265: intentional thread switches are already preserved in this branch as one compact selected-thread switching placeholder with a mounted composer dock, immediate stale-owner clearing, and explicit deployed negative assertions against generic empty-state flashes or hidden composer continuity loss.
Iteration 266: selected-thread session-status and append SSE already remain authoritative in this branch for healthy and restore paths; job polling and goals polling are already gated behind explicit loss of selected-thread ownership, and deployed/static verification already asserts that polling-owned authority does not silently reappear before degradation is explicit.
Iteration 267: the deployed browser gate already exercises healthy streaming, restore or resume, degraded fallback, intentional switch, and cancelled switch as one selected-thread scenario matrix, and already rejects early polling authority, stale ownership, hidden degraded recovery, or generic empty-state flashes before they can qualify as correct success.
