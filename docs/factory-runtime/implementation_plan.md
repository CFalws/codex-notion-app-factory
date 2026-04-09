# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, left rail, collapsed secondary panel, mobile drawer, and pending outbound user bubble unchanged.
2. Extend the existing pending handoff owner so it can move from local user submit into an awaiting-assistant placeholder state after acceptance.
3. Render one temporary assistant placeholder directly in the transcript while the first assistant append has not yet arrived.
4. Clear or replace that placeholder on first assistant append, terminal failure, idle reset, or thread switch so no stale assistant stub remains.
5. Extend the focused verifier and docs so future sessions can prove the assistant handoff stays inside the conversation pane rather than reverting to status-chrome-only feedback.
