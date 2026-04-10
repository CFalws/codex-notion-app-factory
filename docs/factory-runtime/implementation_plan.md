# Factory Runtime Implementation Plan

1. Keep the existing selected-thread SSE ownership, inline live block, and degraded fallback behavior unchanged.
2. Reuse selected-thread `conversation.append` events to trigger immediate job-meta and autonomy-summary refresh.
3. Suppress recurring polling while the selected thread is healthy and SSE-owned, and resume it immediately on reconnect or ownership loss.
4. Keep proposal readiness and central live phase synchronized through the same selected-thread append path.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the append-driven synchronization contract.
