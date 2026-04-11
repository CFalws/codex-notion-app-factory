# Factory Runtime Tasks

## Iteration 99

- [x] Add canonical selected-thread restore attach or resume state to the store-owned session contract.
- [x] Seed saved selected-thread restore before bootstrap completion so the transcript tail, summary, and composer ownership row all share the same restore state.
- [x] Keep the transcript tail as the only live restore surface and suppress generic snapshot `READY` or `ATTACHED` presentation during restore.
- [x] Expose machine-readable restore stage, path, and provenance datasets needed by focused deployed verification.
- [x] Align focused verifiers and proposal artifacts with the iteration-99 restore-stage contract.
