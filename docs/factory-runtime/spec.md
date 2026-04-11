# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Selected-thread SSE attach and switch continuity are bounded, and iteration 68 already added a server-authored autonomy freshness contract. The remaining gap is that healthy selected-thread attach can still reopen hidden app-goals polling even when that server contract already says fallback is not allowed.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread conversation snapshot and `session.bootstrap` transport contract.
- Keep the change bounded to the selected-thread client decision boundary that consumes the existing autonomy-summary freshness envelope.
- Suppress `/api/apps/{app_id}/goals` only on the healthy selected-thread SSE-owned path where the server contract says `fallback_allowed=false`.
- Re-enable goals polling only for canonical `stale-or-missing`, reconnect downgrade, or selected-thread ownership loss cases.
- Keep freshness, source, and fallback semantics server-authored and machine-readable.
- Use one canonical `stale-or-missing` freshness marker for missing or degraded autonomy hydration cases.

## Deliverable

Consume the existing shared `autonomy_summary` freshness envelope on conversation snapshot and `session.bootstrap` so healthy selected-thread attach, resume, and switch stay on the snapshot-plus-SSE path without hidden goals polling, while degraded freshness or ownership loss explicitly reopens the goals fallback path.
