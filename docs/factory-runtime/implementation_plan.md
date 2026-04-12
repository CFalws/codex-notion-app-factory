# Factory Runtime Implementation Plan

## Iteration 239

Retire goals-poll authority for the selected conversation so active autonomy state stays session-status-driven.

1. Keep the change bounded to selected-thread autonomy/session state in `ops-conversations.js`, `ops-store.js`, `ops-render.js`, and the matching runtime session-status payload seam.
2. Stop using goals polling as an authority for any selected-thread live surface in the active workspace.
3. Preserve degraded reconnect or polling fallback as an explicit downgrade path instead of silently refreshing selected-thread autonomy identity from polling.
4. Leave transcript inline session ownership, footer dock behavior, left-rail cues, and switch or restore continuity unchanged.
5. Keep selected-thread autonomy identity, blocker, verifier, proposal, and apply state coherent from session-status bootstrap plus SSE.
6. Align static checks, browser checks, and proposal artifacts with the selected-thread session-status-only autonomy contract.
