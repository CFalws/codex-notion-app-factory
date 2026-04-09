# Factory Runtime Implementation Plan

1. Treat review-rejection recovery context as the single bounded hypothesis for this iteration.
2. Extend proposer prompt summarization so `rejected_before_implementation` iterations include reviewer `blocking_issue` and `suggested_adjustment` fields alongside `proposal_not_approved`.
3. Keep controller, proposal/apply, and verifier behavior unchanged; only proposer input quality should change.
4. Add contract coverage that proves rejected review evidence survives into proposer input as labeled context.
5. Update the app docs so future sessions know review rejection recovery should use structured reviewer evidence instead of prose-only summary.
