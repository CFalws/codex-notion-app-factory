# Factory Runtime Deploy Plan

## Deployment Impact

This changes backend runtime blocker precedence only. Proposal/apply behavior and GitHub Pages assets are unchanged, but paused proposal-mode iterations will now prefer the more conservative `verifier_path_disqualifying` blocker over `proposal_ready` when both signals are present.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Run one healthy proposal-ready iteration and confirm its latest iteration keeps `continuation_blocker_reason=proposal_ready`.
3. Run one proposal-ready iteration whose verifier reviews record `path_acceptability=disqualifying` and confirm its latest iteration, proposer context, and ops summary all show `verifier_path_disqualifying`.
4. Confirm no broader proposal/apply behavior changed beyond the blocker explanation path.
