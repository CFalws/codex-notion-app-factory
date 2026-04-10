# Factory Runtime Implementation Plan

1. Keep the existing conversation-first shell, selected-thread header ownership chip, transcript timeline, footer composer dock, and side-panel behavior unchanged.
2. Reuse `deriveLiveRunState` as the single phase source and extend its render snapshot with terminal event append and time metadata.
3. Add one inline terminal-retention helper for the selected-thread live phase item that permits retained `READY` or `APPLIED` only while the thread remains healthy SSE-owned, no newer append has arrived, and the event is still inside a short deterministic window.
4. Keep the inline phase item unique by reusing the existing selected-thread inline block instead of introducing a second timeline status surface.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the explicit terminal-retention contract.
