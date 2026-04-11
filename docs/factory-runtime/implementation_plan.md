# Factory Runtime Implementation Plan

## Iteration 162

Render canonical `session_status` as one inline selected-thread timeline lane.

1. Keep `appendStream.sessionStatus` as the only selected-thread source for the inline session lane.
2. Expand the selected-thread strip model to expose proposal or apply state and latest job id from canonical `session_status`.
3. Render that canonical state as one inline timeline lane inside the conversation timeline instead of a visually separate strip.
4. Keep it single-instance, fail closed on switch, deselection, terminal completion, and lost authority, and keep degraded reconnect or polling explicitly demoted.
5. Continue collapsing duplicate SSE session-event cards while the canonical inline lane is visible.
6. Align focused verification and proposal artifacts with the iteration-162 canonical inline timeline-lane contract.
