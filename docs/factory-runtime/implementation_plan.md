# Factory Runtime Implementation Plan

## Iteration 167

Mirror the canonical selected-thread session into one sticky active-session row above the conversation list.

1. Keep the change read-only over the existing selected-thread session and follow seam.
2. Reuse the sticky active-session row above the conversation list instead of adding a new navigator surface.
3. Make the row visible for healthy live, handoff, paused or unseen follow, and bounded switching states only.
4. Keep the row selected-thread-only and clear it immediately on reconnect downgrade, polling fallback, terminal completion, deselection, lost authority, or switch resolution.
5. Make the row machine-readable so verification can distinguish healthy selected-thread ownership from switching or cleared states.
6. Align focused verification and proposal artifacts with the iteration-167 sticky active-session contract.
