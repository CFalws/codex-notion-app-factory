# Factory Runtime Implementation Plan

1. Reuse the existing selected-thread append SSE transport instead of adding a new session stream or polling path.
2. Promote selected-thread live append job identity into state immediately so healthy session surfaces no longer depend on snapshot-only `latest_job_id`.
3. Update the selected-thread render derivation so `liveRun`, the header summary row, the transcript live activity, the composer owner row, and the composer-adjacent strip all prefer the latest selected-thread SSE session event as their phase authority.
4. Preserve degraded reconnect, polling fallback, ownership loss, and thread-switch presentation as explicitly non-owned states.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the selected-thread SSE session-authority contract.
