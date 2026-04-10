# Factory Runtime Implementation Plan

1. Reuse the existing composer owner state and selected-thread ownership datasets as the sole authority for the footer strip.
2. Convert the composer-adjacent strip into one compact target-and-transport surface that shows `READY`, `SWITCHING`, or `HANDOFF` plus healthy or degraded transport.
3. Keep the strip visible for selected-thread ready and switch paths, but downgrade or clear transport ownership immediately on reconnect, polling fallback, terminal idle, or thread switch.
4. Preserve the bottom-fixed composer and collapsed utility controls so the footer remains conversation-first instead of becoming a new status panel.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the composer-adjacent session strip contract.
