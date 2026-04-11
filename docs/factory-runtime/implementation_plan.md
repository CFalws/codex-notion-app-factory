# Factory Runtime Implementation Plan

## Iteration 122

Tighten selected-thread switch continuity so the center workspace stays mounted and verifiable through intentional thread changes.

1. Reuse the existing selected-thread switch placeholder and null-conversation render path rather than adding a second transition flow.
2. Keep the center conversation shell and fixed composer mounted during intentional thread switches and render exactly one compact transition placeholder.
3. Expose explicit machine-readable ownership-cleared datasets on the transition placeholder and mounted shell so verification can prove prior-thread ownership was cleared in the same render cycle.
4. Preserve reconnect downgrade, polling fallback, and true no-selection idle behavior without introducing a new transport or polling owner.
5. Extend the focused verifier layer and proposal artifacts so iteration 122 proves mounted switch continuity, immediate ownership clearing, and absence of generic empty-state flashes on the intended path.
