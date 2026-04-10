# Factory Runtime Implementation Plan

1. Keep the existing selected-thread switch render path, bottom-fixed composer dock, and degraded polling fallback behavior unchanged.
2. Reuse the existing `threadTransition` state as the single switch-handoff owner for the center pane.
3. Preserve the current attach placeholder path so the center workspace stays mounted, the composer owner and session summary switch to the incoming target, and the generic empty view remains limited to the true no-conversation path.
4. Clear old-thread live ownership before the new snapshot attaches and reset selected-thread follow ownership to the target thread during the handoff.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the explicit switch-continuity contract.
