# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, left rail, and live-follow behavior unchanged.
2. Rework the selected-thread center pane into one conversation-first session surface with the transcript and composer aligned to the same column.
3. Render one inline selected-thread session block inside the transcript flow that appears for pending-assistant handoff or active SSE-owned live progress, advances through the existing selected-thread phase state, and clears on terminal resolution.
4. Preserve anchored composer reachability on desktop and phone widths while making the secondary operator panel feel more compact and less competitive with the transcript.
5. Extend the focused verifier and docs so future sessions can prove the new inline selected-thread session block and conversation-first workspace markers remain present.
