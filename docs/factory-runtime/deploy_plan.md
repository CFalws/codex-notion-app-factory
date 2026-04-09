# Factory Runtime Deploy Plan

## Deployment Impact

This changes backend runtime proposer input only. Runtime controller behavior, proposal apply policy, and GitHub Pages assets are unchanged. The visible impact is that future autonomous proposals are grounded in structured blocker and path evidence from the previous iteration.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Trigger one goal iteration after a healthy prior iteration and inspect the proposer prompt or saved proposal request for `blocker=none`, `intended_path=expected`, and acceptable verifier evidence.
3. Trigger one goal iteration after a degraded or rejected prior iteration and inspect the proposer prompt or saved proposal request for the stored blocker reason, degraded signals, and disqualifying verifier evidence.
4. Confirm proposal/apply behavior is unchanged apart from better proposer context.
