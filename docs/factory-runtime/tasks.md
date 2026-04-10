# Factory Runtime Tasks

- [x] Keep the existing healthy selected-thread inline live block and selected-thread-only ownership rules unchanged.
- [x] Extend the inline session-state helper so reconnect and polling-backed selected-thread downgrades render one compact degraded-session marker in the timeline.
- [x] Reuse the existing selected-thread live-session indicator for degraded path and reason attribution instead of adding a new transport path.
- [x] Clear the degraded marker immediately on reattach, idle, terminal completion, ownership loss, or thread switch.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the inline degraded-session marker contract.
