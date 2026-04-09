# Factory Runtime Implementation Plan

1. Treat proposer-input quality as the single bounded hypothesis for this iteration.
2. Extend the proposer prompt builder to include prior iteration `continuation_blocker_reason`, intended-path verdict, degraded signals, verifier verdicts, and verifier path-acceptability.
3. Keep the change read-only with respect to controller and apply behavior; only proposer input should change.
4. Add contract coverage that proves healthy and degraded histories are both rendered into the proposer prompt.
5. Update the app docs so future sessions know the proposer is expected to consume structured prior-iteration failure context.
