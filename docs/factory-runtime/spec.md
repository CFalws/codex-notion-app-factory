# Factory Runtime Spec

## Iteration

- current iteration: `225`
- bounded focus: `drive selected-thread live status from one session-scoped append SSE stream`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, switch continuity, handoff continuity, and restore continuity are already present, but this branch still records the older restore-only seam instead of the selected-thread session-stream contract that now drives live phase, proposal, verifier, and apply state. The remaining bounded risk is contract drift: future sessions could let polling or job-panel inference reclaim ownership unless the selected-thread append SSE path is recorded as the intended source of truth.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting one selected-thread SSE session stream to drive the visible session timeline without polling-owned phase or proposal inference.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread append SSE session-status path and its existing frontend ownership surfaces.
- Reuse the current conversation append stream, session-status envelopes, inline timeline owner, and polling fallback gates; do not broaden transport scope beyond the existing append SSE channel.
- Keep header, composer-adjacent context, transcript timeline, and rail markers derived from the same selected-thread session authority.
- Keep polling fallback explicit and degraded-only when the selected-thread SSE path is not authoritative.
- Preserve reconnect, offline, switch, deselection, and restore behavior on the current fail-open path.

## Deliverable

Expose one conversation-first selected-thread workspace where healthy live phase, proposal, verifier, and apply state are attributable to the selected-thread append SSE session stream rather than polling-owned job refresh, while fallback paths remain explicit and degraded.
