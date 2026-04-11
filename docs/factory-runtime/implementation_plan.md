# Factory Runtime Implementation Plan

1. Reuse the existing thread transition placeholder and mounted composer shell instead of introducing a new switch UI.
2. Add one request-scoped transition guard in `ops-conversations.js` so stale async switch results cannot clear or render over a newer selected-thread target.
3. Start a new thread transition not only from an active selected conversation, but also when a second intentional click replaces an already-pending switch target.
4. Keep degraded and attach behavior unchanged except for scoped clearing, so the transition placeholder still resolves through the existing attach or fallback path.
5. Extend focused browser-proof verifiers and iteration artifacts around the bounded switch-cancellation continuity contract.
