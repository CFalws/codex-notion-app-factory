# Autonomy Contract

This repository should be able to continue improving toward a user goal while the user is away.

The goal is not blind infinite execution. The goal is open-ended autonomy with explicit policy checks on every iteration.

## Core Model

An autonomous goal loop should:

1. persist a higher-level user objective
2. generate one bounded hypothesis per iteration
3. have at least two independent reviewers approve that hypothesis before implementation
4. execute that approved hypothesis through the normal app-lane runtime
5. have at least two independent verifiers approve the implementation before merge/apply
6. compare the result to previous iterations
7. decide whether to continue, pause, or stop

## Open-Ended Rule

`max_iterations = 0` means the loop is open-ended.

Open-ended does **not** mean ungoverned. The loop should still pause or stop when:

- a job fails
- a proposal becomes ready and auto-apply is disabled
- the safety assessment is negative
- the alignment assessment is negative
- the goal review says to stop
- an explicit halt is requested

Review or verification rejection should not automatically end the goal.

If policy allows continued exploration, the controller should:

- record the rejected iteration explicitly
- keep the goal `running`
- move on to a different bounded hypothesis
- only pause when the policy says the failure is terminal or the loop can no longer continue safely

## Supervisor Rule

For unattended self-improvement, the goal policy may auto-apply proposal-mode iterations.

When auto-apply is enabled:

- the proposal must still go through the normal proposal/apply path
- the proposal should only auto-apply after both verification reviewers pass
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

## Intended-Path Verdict Contract

Each autonomous iteration should also persist a machine-readable intended-path verdict with:

- `expected_path`
- `degraded_signals`
- `verdict`

This contract answers a different question than `goal_review`.

- `goal_review` says whether the iteration recommends continuing.
- `intended_path` says whether the iteration succeeded through the expected execution path or only through a degraded fallback.

Continuation policy should consume both contracts. A positive review is not enough if the iteration only succeeded through a degraded path.

## Continuation Blocker Contract

Each autonomous iteration should also persist one canonical blocker reason:

- `continuation_blocker_reason`

Recommended values include:

- `none`
- `proposal_ready`
- `intended_path_incomplete`
- `intended_path_degraded`
- `verifier_path_disqualifying`
- `safety_not_passed`
- `alignment_not_passed`
- `goal_review_stop`

This gives the controller, operator console, and future sessions one shared explanation for why the loop paused, stopped, or could not continue.

## Verifier Path-Acceptability Contract

Each autonomous verifier review should also state whether the observed intended path was acceptable:

- `path_acceptability`

Allowed values:

- `acceptable`
- `disqualifying`

This keeps verifier evidence aligned with the iteration's structured intended-path verdict instead of leaving that judgment implicit in prose.

## Iteration Failure Contract

Iteration failure and goal failure are different things.

The controller should distinguish:

- `iteration_rejected`
- `verification_failed`
- `verification_rejected`
- `goal_paused`
- `goal_stopped`

The first three may be recoverable. When policy marks them recoverable, the correct behavior is to explore a different bounded option instead of ending the goal immediately.

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
