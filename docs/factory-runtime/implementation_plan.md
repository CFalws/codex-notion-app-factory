# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, composer-adjacent live strip, transcript-tail live activity turn, left rail, and live-follow behavior unchanged.
2. Normalize selected-thread handoff rendering into one bounded transcript contract: exactly one pending outbound user turn after submit, then exactly one temporary assistant placeholder after acceptance.
3. Clear that temporary handoff state on first real assistant SSE append, terminal resolution, idle reset, or thread switch, and expose the singular handoff stage through machine-readable transcript datasets.
4. Preserve transcript plus composer reachability and keep the handoff state compact on phone widths.
5. Extend the focused verifier and docs so future sessions can prove the transcript handoff stage stays singular, selected-thread-local, and cleanly cleared.
