# UX Feedback Loop

This repository should not expect Codex to discover UI discomfort from code alone.

To improve UI fit over time, the runtime uses a three-step loop:

1. capture friction explicitly
2. force the runtime prompt to interpret that friction
3. persist a structured UX review after the change

## Capture

The operator console may send an optional `ux_context` with:

- `affected_surface`
- `pain_points`
- `note`
- `desired_feel`

This turns "the UI feels bad" into inspectable state.

## Prompting

When a request is UI-oriented or carries `ux_context`, the runtime prompt should:

- include the user-reported UX friction
- treat discomfort as a real bug
- ask Codex to identify the primary user journey
- ask Codex to simplify rather than add more controls
- require a machine-readable `ux_review` block in the final answer

## Persistence

When a job completes, the runtime should preserve:

- `intent_summary`
- `ux_context`
- `ux_review`

This lets later sessions see not only what changed, but what discomfort the change was supposed to remove.

## Meta-Improvement Rule

If a UI change technically works but still feels worse or equally confusing, that is a UX interpretation failure.

Follow-up improvement should then target at least one of:

- better `ux_context` capture in the console
- better prompt instructions for UI work
- better rendering of `ux_review`
- better verification prompts for mobile flow and clarity
