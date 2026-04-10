# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
2. Reuse the existing `threadTransition` state and selected-thread owner path instead of introducing a second switch-status source.
3. Keep the old thread from retaining live-owner treatment once a switch starts by clearing current conversation ownership before the new snapshot attaches.
4. Render exactly one compact transition placeholder in the timeline until the new selected-thread snapshot or live path binds.
5. Keep the focused verifier and durable docs aligned with the continuous thread-switch shell contract.
