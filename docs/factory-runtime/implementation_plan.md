# Factory Runtime Implementation Plan

1. Keep the existing healthy selected-thread inline live block and selected-thread-only ownership rules unchanged.
2. Extend the inline session-state helper so it can render one degraded-session marker for reconnecting or polling-backed selected-thread transitions.
3. Source degraded reason and path attribution from the existing selected-thread live-session indicator instead of introducing a new transport path.
4. Clear the degraded marker on the same ownership transition that reattaches, idles, completes terminally, or switches threads.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the inline degraded-session marker contract.
