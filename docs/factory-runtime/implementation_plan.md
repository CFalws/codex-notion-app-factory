# Factory Runtime Implementation Plan

1. Keep the current selected-thread SSE path, conversation shell, footer composer dock, jump-to-latest affordance, recent-thread rail, and side-panel behavior unchanged.
2. Promote the existing `liveFollow.isFollowing` state into the shared selected-thread session indicator so healthy SSE ownership can read as FOLLOWING or FOLLOW PAUSED without inventing another state source.
3. Reuse that same follow-state signal in the session summary copy, composer-adjacent session strip metadata, and jump-to-latest visibility logic so paused follow becomes explicit while the user reads history.
4. Keep the paused and following signals gated behind healthy selected-thread SSE ownership so reconnecting, polling fallback, thread switch, and terminal completion immediately clear them.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the explicit live-follow visibility contract.
