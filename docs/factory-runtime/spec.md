# Factory Runtime Spec

## Iteration

- current iteration: `275`
- bounded focus: `narrow provisional selected-thread continuity so pre-bootstrap rendering shows only ATTACH or RESUME plus one carried-forward phase chip`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, streamed autonomy identity, merged footer session-composer status, explicit attach authority, restore continuity, switch continuity, one-owner healthy timeline rendering, preserved transitional transcript continuity, phase-led footer dock presentation, and healthy-path authority gating are already present. The bounded question for this iteration is the provisional bootstrap surface itself: whether pre-bootstrap continuity still exposes too much autonomy detail instead of behaving like one sparse session lane until authoritative `session.bootstrap` or append SSE takes over.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting selected-thread attach or resume to feel continuous, with the center timeline, footer dock, and bottom composer staying on one session lane during bootstrap instead of splitting into a restore-only surface that forces inference.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to selected-thread attach or resume authority derivation, selected-thread render presentation, verifier expectations, and durable proposal artifacts.
- Preserve the existing `session_status` plus append SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the bottom-fixed composer dock, selected-thread shell, preserved transition shell, and one-owner healthy timeline behavior unchanged once authoritative ownership is reattached.
- Avoid introducing a second status source, new polling-owned healthy readiness, or new exception-path regressions.

## Deliverable

Keep selected-thread attach or resume on one canonical provisional session lane as soon as the intended EventSource is open. During that bootstrap window, the center timeline and composer-adjacent footer dock stay mounted with only ATTACH or RESUME plus one carried-forward phase chip, and healthy ownership remains withheld until authoritative `session.bootstrap` or append SSE arrives. Degraded, reconnect, restore without stream attachment, handoff, and polling fallback still keep explicit non-healthy visibility.
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
Iteration 268: healthy selected-thread drill-down is already collapsed in this branch into the canonical timeline session card; autonomy and execution detail surfaces are already suppressed on the healthy path while degraded, restore, handoff, switching, and exception paths keep explicit secondary-panel visibility.
Iteration 269: the bottom footer is already unified in this branch as one selected-thread live dock; the session strip carries footer state and datasets, the composer-owner row stays hidden as merged state whenever that dock is active, and send readiness already derives from the same selected-thread authority model without a parallel footer path.
Iteration 272: the canonical footer dock now exposes healthy selected-thread phase progression directly in this branch; the dock leads with the current SSE-owned phase, keeps explicit proposal-ready or applied cues beside it, and stays on the same selected-thread authority path instead of falling back to generic suppressed footer wording.
Iteration 273: selected-thread `sessionStatus` plus append SSE already remain the only healthy-path authority in this branch for proposal readiness, verifier acceptability, blocker reason, phase progression, and apply readiness; job or goals polling stay gated behind explicit degraded fallback and already cannot claim healthy selected-thread session ownership.
Iteration 274: healthy selected-thread header summary chrome is now suppressed in this branch whenever the center timeline is already the authoritative healthy session surface; the timeline and footer dock remain the only healthy session-owned status surfaces, while restore, degraded, handoff, and other non-healthy paths still restore explicit top-level status visibility.
Iteration 279: selected-thread provisional continuity in this branch is now intentionally sparse; before authoritative bootstrap, the center timeline and footer dock show only ATTACH or RESUME plus one carried-forward phase chip, with proposal, verifier, blocker, and apply detail withheld until `session.bootstrap` or append SSE reattaches authority.
