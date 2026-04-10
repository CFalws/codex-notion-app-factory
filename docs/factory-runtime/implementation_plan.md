# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, session strip ownership, bottom follow control, footer composer, and non-selected snapshot rows unchanged.
2. Reuse the existing `threadTransition` state so the center conversation shell remains attached during intentional thread switches.
3. Clear old-thread live ownership and follow state immediately when a different selected thread is chosen.
4. Render exactly one compact selected-thread transition placeholder until the incoming snapshot attaches.
5. Keep the focused verifier and durable docs aligned with the center-workspace thread-switch continuity contract.
