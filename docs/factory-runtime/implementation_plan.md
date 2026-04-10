# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
2. Reuse the existing selected-thread ownership and append-stream state instead of introducing another transport source.
3. Keep the composer-adjacent session rail chip-first, but make its transport chip and provenance explicitly distinguish healthy `LIVE` from `RECONNECT`, `OPEN`, and `OFFLINE`.
4. Keep degraded reconnect or offline transport visible in the same selected-thread rail only while the current selected-thread SSE path still owns the conversation, and clear live-owned treatment immediately on polling-only fallback, terminal idle, or thread switch.
5. Keep the focused verifier and durable docs aligned with the compact selected-thread transport-health rail contract.
