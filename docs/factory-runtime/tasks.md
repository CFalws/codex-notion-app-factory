# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
- [x] Reuse the existing selected-thread ownership, handoff, and live-strip datasets instead of introducing another session source.
- [x] Compress the session summary row into compact target, path, state, and hint chips.
- [x] Compress the composer owner row and live strip into target-first compact chips without changing their ownership semantics.
- [x] Keep the focused verifier and iteration artifacts aligned with the compact selected-thread session chrome contract.
