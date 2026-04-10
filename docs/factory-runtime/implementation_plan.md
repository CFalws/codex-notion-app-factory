# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer dock, sticky active-session row, and side-panel behavior unchanged.
2. Promote the selected-thread healthy-session state into the composer-adjacent live strip so the active conversation itself carries the primary live execution signal.
3. Keep that strip chip-first and selected-thread scoped by reusing the existing selected-thread ownership helper instead of inventing another status source.
4. Hide the strip immediately on reconnect downgrade, polling fallback, thread switch, or terminal completion so degraded or stale live-owned UI never remains near the composer.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the healthy-path-only live strip contract.
