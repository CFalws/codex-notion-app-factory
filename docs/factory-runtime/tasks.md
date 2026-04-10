# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
- [x] Reuse the existing `pendingOutgoing` and selected-thread ownership state instead of introducing another handoff source.
- [x] Limit the transcript to exactly one pending outbound user turn before acceptance and exactly one temporary assistant placeholder after acceptance.
- [x] Keep the composer-adjacent handoff bar aligned with that single selected-thread stage and clear accepted state on assistant append, terminal failure, idle reset, polling-only fallback, or thread switch.
- [x] Keep the focused verifier and iteration artifacts aligned with the single-stage selected-thread handoff contract.
