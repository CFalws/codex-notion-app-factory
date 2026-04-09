# Factory Runtime Spec

## Request

- title: `Unattended Runtime Supervisor`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Proposal-mode auto-apply can currently look successful even when the local merge succeeded but the remote push failed. That degraded deployment path must not count as healthy unattended progress.

## Target User

The primary user is the operator relying on unattended runtime self-improvement and needing durable evidence that proposal apply, restart, and continuation happened correctly.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Prefer a bounded state/verification improvement over broad supervisor automation.

## Deliverable

Pause unattended continuation on failed-push auto-apply results, emit an explicit degraded event and stop reason, and verify both the healthy pushed path and the push-failed path.
