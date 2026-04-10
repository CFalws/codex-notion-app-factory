# Factory Runtime Tasks

- [x] Keep the existing selected-thread SSE ownership, inline live block, and degraded fallback behavior unchanged.
- [x] Reuse selected-thread `conversation.append` events to trigger immediate job-meta and autonomy-summary refresh.
- [x] Suppress recurring polling while the selected thread is healthy and SSE-owned, and resume it on reconnect or ownership loss.
- [x] Keep proposal readiness and central live phase synchronized through the same selected-thread append path.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the append-driven synchronization contract.
