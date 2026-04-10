# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
2. Reuse the existing `pendingOutgoing` and selected-thread ownership state instead of introducing another handoff source.
3. Keep the transcript limited to one pending outbound user turn before acceptance and one temporary assistant placeholder after acceptance, never both at once.
4. Make the composer-adjacent handoff bar match that single selected-thread stage and clear accepted state immediately on first assistant append, terminal failure, polling-only fallback, idle reset, or thread switch.
5. Keep the focused verifier and durable docs aligned with the single-stage selected-thread handoff contract.
