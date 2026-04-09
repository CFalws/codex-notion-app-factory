# Factory Runtime Deploy Plan

## Deployment Impact

This changes backend proposer input only. Controller behavior, proposal/apply behavior, and GitHub Pages assets are unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Run a goal where iteration N is rejected before implementation with `proposal_not_approved`.
3. Trigger iteration N+1 and inspect the proposer prompt or saved proposer context for `proposal_review_blocking_issues` and `proposal_review_suggested_adjustments`.
4. Confirm the next bounded hypothesis addresses the rejected shape rather than repeating it verbatim.
