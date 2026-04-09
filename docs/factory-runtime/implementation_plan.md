# Factory Runtime Implementation Plan

1. Treat one canonical continuation-blocker field as the single bounded hypothesis for this iteration.
2. Derive `continuation_blocker_reason` from proposal readiness, intended-path verdicts, verifier path acceptability, and goal-review governance outcomes.
3. Persist that blocker reason into iteration state and final iteration events so controller policy and durable state agree.
4. Surface the same stored blocker reason in the ops console without adding new frontend inference.
5. Prove healthy, degraded, and verifier-disqualifying paths leave the expected blocker reason in the runtime contract test.
