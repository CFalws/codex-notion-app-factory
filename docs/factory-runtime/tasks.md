# Factory Runtime Tasks

- [x] Confirm the inline session block already owns handoff and degraded selected-thread rendering while healthy live still uses a separate transcript-tail activity.
- [x] Route healthy selected-thread live progress through the existing inline session block instead of a separate transcript-tail live item.
- [x] Suppress the duplicate transcript-tail live activity whenever the unified inline block is active.
- [x] Preserve degraded and switched states as explicitly non-owned or cleared session states.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the single-inline-session-block contract.
