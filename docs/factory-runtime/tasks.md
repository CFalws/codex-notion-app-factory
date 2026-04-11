# Factory Runtime Tasks

## Iteration 162

- [x] Keep canonical `appendStream.sessionStatus` as the only selected-thread source for the inline session lane.
- [x] Expose proposal or apply state and latest job id from canonical `session_status` in that lane.
- [x] Render the canonical selected-thread status lane inside the conversation timeline instead of as a separate strip surface.
- [x] Keep the lane single-instance and fail closed on switch, deselection, terminal completion, and lost authority.
- [x] Keep degraded reconnect and polling fallback visibly demoted rather than silently primary.
- [x] Align focused docs and verification with the iteration-162 canonical inline timeline-lane contract.
