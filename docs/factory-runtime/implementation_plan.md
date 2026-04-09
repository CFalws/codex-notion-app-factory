# Factory Runtime Implementation Plan

1. Treat continuation-blocker precedence as the single bounded hypothesis for this iteration.
2. Change `runtime_goals.continuation_blocker_reason()` so verifier `path_acceptability=disqualifying` outranks `proposal_ready`.
3. Keep proposal/apply behavior unchanged; only the canonical blocker chosen for state and summaries should change.
4. Add contract coverage for both the negative case where proposal-ready plus disqualifying verifier evidence must yield `verifier_path_disqualifying` and the healthy proposal-ready case that should stay `proposal_ready`.
5. Update the app docs so future sessions know verifier disqualification is the more conservative blocker when both signals are present.
