# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread SSE path already owns the session workspace shell and exact phase wording, but the selected conversation still risks deriving some phase and readiness authority from `currentJobId`, `latest_job_id`, or polled snapshots rather than from the same live append stream that drives the transcript. That weakens the intended-path guarantee: the workspace can look realtime while still depending on snapshot-backed job identity for part of the live session state.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport, ownership, `liveRun`, session-summary, transcript-tail, and composer-strip contracts instead of adding a new backend or transport path.
- Keep the change bounded to selected-thread session authority on the healthy path.
- Make the same selected-thread append SSE stream authoritative for proposal, review, verify, ready, and applied progression across the header, transcript live activity, composer owner row, and composer-adjacent strip.
- Keep degraded reconnect, polling fallback, ownership loss, and switch states visibly non-owned so they cannot look like healthy live progression.

## Deliverable

Define and verify one healthy selected-thread SSE path where proposal, review, verify, ready, and applied progression are rendered from the same append-driven session authority as the live transcript, while degraded states remain clearly non-owned and polling stays fallback-only.
