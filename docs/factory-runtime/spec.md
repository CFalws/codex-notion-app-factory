# Factory Runtime Spec

## Iteration

- current iteration: `117`
- bounded focus: `center transcript collapses healthy selected-thread live progress into one inline session lane`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, switching continuity, detached follow behavior, and left-rail mirroring are already established. The remaining gap is the center transcript itself: healthy selected-thread progress still reads partly like a live lane plus adjacent status rendering instead of one compact session timeline surface.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, follow-state, poll-fallback, composer, and rail contracts unchanged.
- Do not introduce a new transport, polling path, backend protocol, or a second center-pane live-status surface.
- Reuse the existing transcript live activity, selected-thread phase progression, autonomy summary, and milestone helpers instead of adding another center authority model.
- Show exactly one compact selected-thread live session lane at the transcript tail on the healthy SSE-owned path.
- Carry explicit proposal or review or verify or auto-apply or ready or applied labels plus path, verifier, and blocker state on that lane through machine-readable datasets.
- Suppress duplicate prose-heavy milestone status rendering around that lane.
- Clear or downgrade the lane immediately on reconnect, polling fallback, terminal idle, restore-only, or switching paths.

## Deliverable

Define and verify one transcript-tail selected-thread live session lane contract where healthy SSE-owned progress, milestone progression, and autonomy path state read as one compact center-pane timeline surface, while degraded and non-healthy paths clear or downgrade it immediately.
