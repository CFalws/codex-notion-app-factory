# Factory Runtime Deploy Plan

## Deployment Impact

This changes backend runtime behavior for unattended proposal-mode goals. GitHub Pages assets are unchanged. The visible impact is in goal state and conversation events when auto-apply push succeeds versus when it fails after local apply.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Let the normal proposal apply flow continue into restart only after a healthy pushed apply outcome.
3. Verify that a healthy auto-applied proposal still reaches restart handoff and later normal continuation.
4. Verify that a failed-push auto-applied proposal emits `goal.proposal.auto_apply.degraded`, pauses the goal, and never enters restart-resume continuation.
