# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer dock, sticky active-session row, and side-panel behavior unchanged.
2. Reuse the existing `threadTransition`, selected-thread ownership clearing, and composer target state instead of introducing another switch-state source.
3. Preserve the center workspace during intentional thread switches and render exactly one compact `SWITCHING` placeholder until the new snapshot attaches.
4. Limit the generic empty-state branch to true no-conversation idle and clear stale old-thread live or follow ownership as soon as switching begins.
5. Keep the focused verifier and durable docs aligned with the selected-thread switch continuity contract.
