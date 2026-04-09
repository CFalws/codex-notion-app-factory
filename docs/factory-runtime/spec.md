# Factory Runtime Spec

## Request

- title: `Self-Improving Agentic Dev Environment`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Autonomous iterations now record structured intended-path verdicts, but verifier reviews still leave path acceptability implicit. Operators can see that a degraded signal occurred, yet verifier evidence does not explicitly say whether that path was acceptable or disqualifying.

## Target User

The primary user is the operator relying on unattended runtime self-improvement and needing durable evidence that proposal apply, restart, and continuation happened correctly.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Prefer a bounded state/verification improvement over broad supervisor automation.

## Deliverable

Pass the structured intended-path verdict into autonomous verifier prompts, persist an explicit verifier `path_acceptability` judgment in review state, and verify that healthy and degraded iterations leave clearly different verification evidence.
