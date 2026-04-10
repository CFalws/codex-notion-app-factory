# Factory Runtime Implementation Plan

1. Reuse the existing selected-thread inline session state and autonomy summary projection as the sole authority for the healthy transcript-tail live item.
2. Move healthy selected-thread live autonomy progress into one compact transcript-tail activity item that updates in place through the existing SSE-owned path.
3. Keep the separate inline session block for degraded or handoff-only states so reconnect, polling fallback, and first-append handoff remain explicit without duplicating healthy live ownership.
4. Clear the transcript-tail live item immediately on reconnect downgrade, polling fallback, terminal idle, and thread switch.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the transcript-tail live activity contract.
