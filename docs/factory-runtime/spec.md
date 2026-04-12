# Factory Runtime Spec

## Iteration

- current iteration: `230`
- bounded focus: `promote selected-thread session status to the single healthy-path realtime authority`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, switch continuity, restore continuity, the selected-thread session-stream contract, deployed single-authority proof, and the selected-thread handoff path are already present. The remaining bounded gap is operator inference around polled phase and proposal state: the healthy selected-thread workspace should treat selected-thread session status as the sole visible live authority and leave `/api/jobs/{id}` and `/api/apps/{appId}/goals` reads in explicit fallback-only territory.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting live phase, proposal, review, verify, and apply progression to arrive through one selected-thread realtime session surface rather than through hidden polling-owned state.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the existing selected-thread append SSE ownership path and matching proposal artifacts.
- Reuse `appendStream.sessionStatus`, the canonical selected-thread session-status helper, and existing selected-thread render boundaries instead of adding new transport.
- Keep the transcript-centered session surface as the only healthy live-owned authority while header and composer-adjacent mirrors remain passive.
- Prevent healthy `/api/jobs/{id}` and `/api/apps/{appId}/goals` polling reads from becoming visible owners in the selected-thread workspace.
- Preserve reconnect and polling downgrade as explicit degraded fallback that clears live ownership immediately.
- Keep restore, switch, and handoff behavior on the current intended path.

## Deliverable

Expose one conversation-first selected-thread workspace where healthy live phase and proposal progression come from selected-thread session status on the append SSE path, while polling remains explicit degraded fallback instead of a healthy visible owner.
