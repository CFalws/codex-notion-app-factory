# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, composer-adjacent live strip, transcript-tail live activity turn, left rail, and live-follow behavior unchanged.
- [x] Normalize the selected-thread handoff flow to exactly one pending outbound user turn after submit and exactly one temporary assistant placeholder after acceptance.
- [x] Clear that temporary handoff state on first real assistant SSE append, terminal resolution, idle reset, or thread switch without leaving duplicate synthetic turns behind.
- [x] Preserve transcript plus composer reachability on desktop and phone widths while the temporary handoff state is visible.
- [x] Extend focused verification so future sessions can prove the transcript publishes a single selected-thread handoff stage with exact pending-user and pending-assistant counts.
