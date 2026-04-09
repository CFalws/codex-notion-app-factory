# Factory Runtime Spec

## Request

- title: `Self-Improving Agentic Dev Environment`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Autonomous iterations still rely too much on prose to tell whether success happened through the intended path or only through a degraded fallback. That makes continuation policy and later inspection less trustworthy than they should be.

## Target User

The primary user is the operator relying on unattended runtime self-improvement and needing durable evidence that proposal apply, restart, and continuation happened correctly.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Prefer a bounded state/verification improvement over broad supervisor automation.

## Deliverable

Persist one iteration-level intended-path verdict containing the expected execution path, degraded signals, and final verdict, then make autonomous continuation consume that structured contract instead of inferring path health from prose alone.
