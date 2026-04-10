# Factory Runtime Implementation Plan

1. Keep the existing selected-thread SSE ownership, inline live block, and degraded fallback behavior unchanged.
2. Reuse the selected-thread session summary, follow, and transition state as the only left-rail live-session source.
3. Tighten the sticky row so it only appears for healthy selected-thread ownership or the explicit attach transition.
4. Publish machine-readable row ownership, source, phase, and unseen-count datasets for verifier attribution.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the left-rail active-session contract.
