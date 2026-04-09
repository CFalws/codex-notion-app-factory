# Factory Runtime Deploy Plan

## Deployment Impact

This changes backend runtime autonomy state and the static ops console summary. The visible impact is that each autonomous iteration now carries one canonical `continuation_blocker_reason`, and the console surfaces the same reason directly.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Verify that a healthy proposal-mode iteration records `continuation_blocker_reason=none`.
3. Verify that a degraded intended-path iteration records `continuation_blocker_reason=intended_path_degraded`.
4. Verify that a verifier-disqualifying iteration records `continuation_blocker_reason=verifier_path_disqualifying`.
5. Confirm the ops console shows the same blocker reason without requiring raw state inspection.
