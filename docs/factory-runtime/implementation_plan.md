# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
2. Reuse the existing selected-thread ownership, handoff, and live-strip datasets instead of introducing another session source.
3. Compress the session summary row so target, path, state, and supporting hint read as compact chips instead of sentence-style helper copy.
4. Compress the composer owner row and live strip so target, attach, transport, and phase cues stay short, target-first, and machine-readable without changing their ownership semantics.
5. Keep the focused verifier and durable docs aligned with the compact selected-thread session chrome contract.
