# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, left rail, collapsed secondary panel, and mobile drawer unchanged.
2. Add one temporary pending outbound message to the active conversation timeline at submit time using local selected-thread state.
3. Reuse the existing composer-adjacent activity bar to expose a short sending handoff state until the first accepted or live signal arrives.
4. Clear the pending item on accepted response, live append, failure, idle, or thread switch so no stale local artifact remains.
5. Extend the focused verifier and docs so future sessions can prove the active send handoff stays inside the transcript and composer path rather than relying on new fallback surfaces.
