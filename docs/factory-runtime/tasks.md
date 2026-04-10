# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript shell, footer composer dock, and rail ownership model unchanged.
- [x] Reuse the existing `threadTransition` state and selected-thread ownership clearing instead of introducing another switch-state source.
- [x] Keep the center workspace mounted during intentional thread switches and render at most one compact `SWITCHING` placeholder until the new snapshot attaches.
- [x] Limit the generic empty-state branch to true no-conversation idle so thread switches never flash a reset view.
- [x] Keep the focused verifier and iteration artifacts aligned with the selected-thread switch continuity contract.
