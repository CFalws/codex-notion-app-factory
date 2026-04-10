# Factory Runtime Implementation Plan

1. Reuse the existing selected-thread header ownership datasets as the sole authority for left-rail live-session visibility.
2. Restrict the left-rail active-session row to one healthy SSE-owned mirror for the currently selected thread.
3. Remove rail-specific switching, handoff, and backlog signaling so the rail cannot outgrow the canonical ownership source.
4. Prove that reconnect, polling fallback, terminal idle, and thread switch clear the rail mirror immediately.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the single-source rail mirror contract.
