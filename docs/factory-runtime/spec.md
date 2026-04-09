# Factory Runtime Spec

## Request

- title: `Self-Improving Agentic Dev Environment`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Rejected-before-implementation iterations already persist `proposal_not_approved` plus reviewer `blocking_issue` and `suggested_adjustment`, but the next proposer prompt still reduces that to generic summary text. That makes recovery from review rejection weaker than it should be and increases the chance of repeating the same weak hypothesis.

## Target User

The primary user is the operator relying on unattended runtime self-improvement and needing durable evidence that proposal apply, restart, and continuation happened correctly.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Prefer a bounded state/verification improvement over broad supervisor automation.

## Deliverable

Carry reviewer rejection evidence into proposer input as labeled context alongside `proposal_not_approved`, so the next bounded hypothesis can react to the explicit blocking issue and suggested adjustment instead of relying on prose-only memory.
