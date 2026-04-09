# Factory Runtime Spec

## Request

- title: `Unattended Runtime Supervisor`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Unattended proposal-mode improvement already has auto-apply and startup resume hooks, but the restart-resume path is too implicit. A goal can remain `running` while actually waiting for service restart, which weakens observability and makes it hard to verify whether continuation happened through the intended path.

## Target User

The primary user is the operator relying on unattended runtime self-improvement and needing durable evidence that proposal apply, restart, and continuation happened correctly.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Prefer a bounded state/verification improvement over broad supervisor automation.

## Deliverable

Make restart-resume explicit in goal state, surface why a goal resumed after startup, and verify that unattended proposal loops continue through the intended restart-recovery path.
