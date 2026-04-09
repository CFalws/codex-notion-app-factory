# Autonomy Contract

This repository should be able to continue improving toward a user goal while the user is away.

The goal is not blind infinite execution. The goal is open-ended autonomy with explicit policy checks on every iteration.

## Core Model

An autonomous goal loop should:

1. persist a higher-level user objective
2. generate one bounded hypothesis per iteration
3. execute that hypothesis through the normal app-lane runtime
4. verify the result
5. compare the result to previous iterations
6. decide whether to continue, pause, or stop

## Open-Ended Rule

`max_iterations = 0` means the loop is open-ended.

Open-ended does **not** mean ungoverned. The loop should still pause or stop when:

- a job fails
- a proposal becomes ready and auto-apply is disabled
- the safety assessment is negative
- the alignment assessment is negative
- the goal review says to stop
- an explicit halt is requested

## Supervisor Rule

For unattended self-improvement, the goal policy may auto-apply proposal-mode iterations.

When auto-apply is enabled:

- the proposal must still go through the normal proposal/apply path
- apply and push status must be recorded in state
- if apply schedules a service restart, the goal should remain `running`
- a goal waiting for restart-resume should record that pending state explicitly
- the runtime should resume any `running` goals on startup so unattended loops survive restarts

## Goal Review Contract

Autonomous iterations should emit a machine-readable `goal_review` with:

- `hypothesis`
- `verification_result`
- `comparison_to_previous`
- `continue_recommended`
- `alignment_assessment`
- `safety_assessment`
- `next_focus`

This lets the controller decide based on structured review instead of guessing from prose.

## Safety Principle

The controller should never treat "still making changes" as enough reason to continue.

The continuation signal must be backed by:

- a positive alignment assessment
- a positive safety assessment
- an explicit recommendation to continue

## Meta-Improvement Principle

If the loop chooses the wrong next step, misses the user's real objective, or keeps iterating when it should stop, that is not only a runtime bug.

It is also feedback that should improve at least one of:

- intent interpretation
- prompt structure
- verification gates
- continuation policy
- operator visibility
