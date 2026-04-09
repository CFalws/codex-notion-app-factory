# Intent Contract

This runtime should not treat the user's latest sentence as the whole task. It should persist a compact interpretation of the user's likely intent and carry that interpretation through execution and review.

## Goal

The system should move from:

- "implement the literal request text"

to:

- "implement the user's intended outcome, while making the smallest reasonable assumptions explicit"

## Persisted Interpretation

Every runtime request and job should carry an `intent_summary` with these fields:

- `explicit_request`
- `interpreted_outcome`
- `assumptions`
- `ambiguity`
- `success_signal`

Requests may also carry an optional `ux_context` when the user is describing discomfort in the interface rather than only asking for a feature change.

This summary is not a model-grade plan. It is a compact runtime contract that makes the agent's interpretation inspectable and reviewable.

## Meanings

### `explicit_request`

The shortest durable statement of what the user directly asked for.

### `interpreted_outcome`

The concrete result the system believes the user wants, even if the wording was incomplete.

### `assumptions`

The smallest assumptions the runtime is making in order to proceed without blocking on clarification.

### `ambiguity`

A short statement of how much uncertainty remains and why.

### `success_signal`

The user-visible or operator-visible condition that should hold if the intent was interpreted correctly.

## Runtime Expectations

- User request messages should preserve the interpreted intent in message metadata.
- Request records should store the same `intent_summary`.
- Job records should store the same `intent_summary`.
- When present, `ux_context` should be preserved onto request, job, and user-message metadata.
- Runtime prompts should include the interpreted intent so Codex sees both the raw request and the current interpretation.
- UI-oriented prompts should also include the structured UX discomfort signal and require a UX review block in the final response.
- Conversation events should record that intent interpretation happened.

## Meta-Improvement Rule

If a job completes but misses the user's real intent, that is not only an implementation error. It is also an intent interpretation failure.

When that happens, follow-up improvement should target at least one of:

- intent extraction heuristics
- clarification rules
- verification gates
- conversation UX
- engineering log prompts

The repository should evolve so future sessions make fewer of the same interpretation mistakes.
