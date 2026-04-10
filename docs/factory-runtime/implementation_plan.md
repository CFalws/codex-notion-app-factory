# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer dock, and rail ownership model unchanged.
2. Reuse the existing `threadTransition` state and selected-thread ownership clearing instead of introducing another switch-state source.
3. Keep the center workspace mounted during intentional thread switches and render at most one compact `SWITCHING` placeholder until the new snapshot attaches.
4. Limit the generic empty-state branch to true no-conversation idle so thread switches never flash a reset view.
5. Keep the focused verifier and durable docs aligned with the selected-thread switch continuity contract.
