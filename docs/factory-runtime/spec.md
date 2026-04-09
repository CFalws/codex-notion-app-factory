# Factory Runtime Spec

## Request

- title: `Self-Improving Agentic Dev Environment`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Autonomous iterations now persist canonical blocker reasons, intended-path verdicts, and verifier path-acceptability, but the proposer still sees prior history mostly as freeform summary plus `next_focus`. That leaves the next bounded hypothesis under-informed when the previous iteration paused, degraded, or was rejected.

## Target User

The primary user is the operator relying on unattended runtime self-improvement and needing durable evidence that proposal apply, restart, and continuation happened correctly.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Prefer a bounded state/verification improvement over broad supervisor automation.

## Deliverable

Feed the latest structured blocker and path evidence back into the proposer prompt so the next bounded hypothesis is explicitly grounded in why the previous iteration could not safely continue.
