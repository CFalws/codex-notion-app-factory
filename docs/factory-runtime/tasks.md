# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript shell, footer composer dock, sticky active-session row, and side-panel behavior unchanged.
- [x] Reuse the existing `threadTransition`, selected-thread ownership clearing, and composer target state instead of introducing another switch-state source.
- [x] Preserve the center workspace during intentional thread switches and render exactly one compact `SWITCHING` placeholder until the new snapshot attaches.
- [x] Limit the generic empty-state branch to true no-conversation idle and clear stale old-thread live or follow ownership as soon as switching begins.
- [x] Keep the focused verifier and iteration artifacts aligned with the selected-thread switch continuity contract.
