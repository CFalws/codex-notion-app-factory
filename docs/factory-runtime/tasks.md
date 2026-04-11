# Factory Runtime Tasks

## Iteration 159

- [x] Restore the canonical selected-thread `session_status` payload in append-SSE bootstrap, replay, and live append envelopes.
- [x] Hydrate `appendStream.sessionStatus` in the operator console without transferring composer or transcript ownership.
- [x] Add one selected-thread center-pane live session strip derived from canonical `session_status`.
- [x] Demote reconnect and polling fallback explicitly in that strip and clear it on switch or terminal completion.
- [x] Suppress the older transcript live card while the new strip is visible so the center pane exposes one compact selected-thread status surface.
- [x] Extend focused runtime-contract, static, and deployed verification to require the canonical payload plus the new strip contract.
- [x] Align proposal artifacts with the iteration-159 session-status strip contract.
