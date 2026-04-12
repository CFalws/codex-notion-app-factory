# Factory Runtime Implementation Plan

## Iteration 241

Absorb selected-thread NEW or PAUSED follow affordance into the footer dock without changing authority.

1. Keep the change bounded to footer-dock follow presentation, DOM wiring, and verifier artifacts.
2. Preserve the existing selected-thread `session_status` plus SSE authority path.
3. Remove the separate floating jump-to-latest surface.
4. Render NEW or PAUSED follow state and unseen-count metadata only through the footer-dock action affordance.
5. Preserve immediate clear or downgrade behavior on switch, terminal, reconnect, and polling fallback paths.
6. Align proposal artifacts with the single-owner footer follow contract.
