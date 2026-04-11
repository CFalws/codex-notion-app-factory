# Factory Runtime Implementation Plan

## Iteration 99

Make selected-thread restore a first-class machine-readable session stage without changing transport or polling behavior.

1. Reuse the selected-thread store as the owning boundary for restore attach or resume state.
2. Seed saved selected-thread restore before bootstrap completion so the transcript tail, summary, and composer can all read the same restore stage immediately.
3. Keep the transcript tail as the only live restore surface while the compact header and composer ownership row expose the same machine-readable restore datasets without flashing generic `READY` or `ATTACHED`.
4. Preserve immediate thread-switch clearing, explicit degraded `RECONNECT` or `POLLING` markers, and fixed composer continuity.
5. Extend the focused verifier layer and proposal artifacts so the deployed verifier can prove healthy resume succeeded without conversation refetch or polling-owned success.
