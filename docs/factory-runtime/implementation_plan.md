# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, rail behavior, and center-pane live surface unchanged.
2. Reuse the existing jump-to-latest control as one explicit bottom-anchored transcript follow indicator for the selected conversation only.
3. Show `NEW` when healthy off-screen selected-thread SSE appends arrive, and show `PAUSED` when detached follow state is visible through a degraded render source.
4. Clear the follow indicator immediately when the operator jumps back to latest or re-engages the composer, while leaving it hidden when already following.
5. Extend the focused verifier and docs so future sessions can prove selected-thread-only visibility, explicit `NEW` or `PAUSED` state, unseen-count metadata, and absence during healthy tail-following.
