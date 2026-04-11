# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread SSE attach and switch continuity are bounded, but autonomy freshness is still inferred from a separate goals fetch. The client needs one server-authored contract that tells it whether the autonomy summary is fresh, bootstrap-only, or stale-or-missing before it falls back to app-goals polling.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread conversation snapshot and `session.bootstrap` transport contract.
- Keep the change bounded to one additive autonomy-summary freshness envelope.
- Do not suppress existing `/api/apps/{app_id}/goals` fallback behavior in this iteration.
- Keep freshness, source, and fallback semantics server-authored and machine-readable.
- Use one canonical `stale-or-missing` freshness marker for missing or degraded autonomy hydration cases.

## Deliverable

Define and verify one minimal `autonomy_summary` envelope on both conversation snapshot and `session.bootstrap`, with shared summary fields plus `source`, `generated_at`, `freshness_state`, and `fallback_allowed`, then hydrate the selected-thread autonomy state from that envelope before the existing goals fallback path runs.
