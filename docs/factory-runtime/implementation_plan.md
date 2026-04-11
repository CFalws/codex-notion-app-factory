# Factory Runtime Implementation Plan

## Iteration 159

Promote canonical selected-thread `session_status` into one compact center-pane live session strip.

1. Restore the missing canonical `session_status` payload in the append-SSE bootstrap, replay, and live append envelopes inside `api_runtime_context.py`.
2. Hydrate `appendStream.sessionStatus` in `ops-conversations.js` and keep reconnect or polling fallback explicit there without changing other UI ownership.
3. Add one store-owned selected-thread session strip model in `ops-store.js` that reads from `appendStream.sessionStatus` and fails closed on switch, terminal, deselection, or lost authority.
4. Render one compact inline session strip above the transcript in `ops-render.js` and suppress the older transcript live card whenever that strip is visible.
5. Extend focused runtime-contract, static, and deployed verification so the canonical `session_status` seam and the single center-pane strip are both required.
6. Align proposal artifacts with the iteration-159 session-status strip contract.
