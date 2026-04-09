# Factory Runtime Spec

## Request

- title: `Self-Improving Agentic Dev Environment`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Proposal-mode iterations can already record verifier `path_acceptability=disqualifying`, but the continuation blocker can still collapse to `proposal_ready`. That makes a failed intended path look like a normal review wait instead of the more conservative verifier-path failure the operator should see first.

## Target User

The primary user is the operator relying on unattended runtime self-improvement and needing durable evidence that proposal apply, restart, and continuation happened correctly.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Prefer a bounded state/verification improvement over broad supervisor automation.

## Deliverable

Make `verifier_path_disqualifying` outrank `proposal_ready` in continuation-blocker precedence so iteration state, proposer context, and the ops summary all expose the same canonical blocker when verifier evidence says the path is not acceptable.
