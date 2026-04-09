# Factory Runtime Deploy Plan

## Deployment Impact

This changes backend runtime behavior for unattended proposal-mode goals. GitHub Pages assets are unchanged. The visible impact is in goal state and conversation events after proposal apply and restart recovery.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Let the normal proposal apply flow schedule the service restart if the app record requests it.
3. Verify that a proposal-mode autonomous goal records `awaiting_restart_resume` before restart and later emits `goal.resumed` with `resume_reason=restart_resume` after startup recovery.
