# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
- [x] Reuse the existing selected-thread ownership and append-stream state instead of introducing another transport source.
- [x] Make the composer-adjacent session rail expose explicit `LIVE`, `RECONNECT`, `OPEN`, and `OFFLINE` transport cues beside the current selected-thread phase.
- [x] Keep degraded transport visible only while the current selected-thread SSE owner still exists, and clear live-owned treatment on polling-only fallback, terminal idle, or thread switch.
- [x] Keep the focused verifier and iteration artifacts aligned with the compact selected-thread transport-health rail contract.
