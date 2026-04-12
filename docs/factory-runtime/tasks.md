# Factory Runtime Tasks

## Iteration 239

- [x] Keep the change bounded to selected-thread autonomy/session state in `ops-conversations.js`, `ops-store.js`, `ops-render.js`, and the matching runtime session-status payload seam.
- [x] Stop using goals polling as an authority for any selected-thread live surface in the active workspace.
- [x] Preserve degraded reconnect or polling fallback as an explicit downgrade path instead of silently refreshing selected-thread autonomy identity from polling.
- [x] Leave transcript inline session ownership, footer dock behavior, left-rail cues, and switch or restore continuity unchanged.
- [x] Keep selected-thread autonomy identity, blocker, verifier, proposal, and apply state coherent from session-status bootstrap plus SSE.
- [x] Align static checks, browser checks, and proposal artifacts with the selected-thread session-status-only autonomy contract.
