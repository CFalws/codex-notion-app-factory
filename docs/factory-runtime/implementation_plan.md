# Factory Runtime Implementation Plan

1. Keep the selected-conversation SSE path and inline live-run row unchanged.
2. Remove the large autonomy summary card from the scrollable thread body and re-home it in a compact rail directly below the thread header.
3. Preserve blocker, intended-path, and verifier state as machine-readable attributes so verifier tooling still finds the same data after the move.
4. Keep the center scroll region focused on the timeline and leave the composer immediately reachable below it.
5. Extend the static verifier and docs so future sessions can prove the autonomy summary no longer competes with thread history.
