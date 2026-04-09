# Factory Runtime Implementation Plan

1. Treat degraded proposal auto-apply continuation as the single bounded hypothesis for this iteration.
2. Inspect proposal apply result fields after auto-apply instead of assuming job completion is enough.
3. Pause the goal immediately when auto-apply ends with failed push or another non-healthy apply status.
4. Emit a distinct degraded auto-apply event and persist the degraded reason into the iteration record.
5. Prove both the healthy pushed path and the failed-push path in the runtime contract test.
