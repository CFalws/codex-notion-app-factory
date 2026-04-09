# Factory Runtime Implementation Plan

1. Treat unattended restart-resume observability as the single bounded hypothesis for this iteration.
2. Extend the goal state payload with explicit restart-resume markers instead of overloading plain `running`.
3. Mark those fields when auto-applied proposals schedule restart and automatic continuation is enabled.
4. Clear and annotate that state when startup recovery reattaches the loop.
5. Prove the intended path with a runtime contract test that simulates restart by creating a fresh app instance against the same state root.
