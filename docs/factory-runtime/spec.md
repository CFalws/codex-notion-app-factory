# Factory Runtime Spec

## Request

- title: `Self-Improving Agentic Dev Environment`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Autonomous iterations now record intended-path verdicts and verifier path acceptability, but the actual reason the loop paused or could not continue is still fragmented across several fields. Operators and future weaker sessions still have to infer the blocker from raw state instead of reading one canonical explanation.

## Target User

The primary user is the operator relying on unattended runtime self-improvement and needing durable evidence that proposal apply, restart, and continuation happened correctly.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Prefer a bounded state/verification improvement over broad supervisor automation.

## Deliverable

Persist one canonical `continuation_blocker_reason` on each autonomous iteration, derive it from the existing structured autonomy signals, and surface the same field in the ops console so controller policy and operator visibility share one explanation path.
