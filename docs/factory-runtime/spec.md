# Factory Runtime Spec

## Iteration

- current iteration: `239`
- bounded focus: `retire goals-poll authority for the selected conversation so active autonomy state stays session-status-driven`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, and unified header chrome are already present. The remaining bounded gap is hidden goals-poll dependence for selected-thread autonomy state: blocker, verifier, proposal, and apply progress in the active workspace should come only from selected-thread session-status bootstrap plus SSE, with degraded transport explicitly downgrading instead of silently refreshing those fields from polling.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the active selected conversation to behave like one live session whose autonomy state stays coherent without hidden goals polling.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to selected-thread autonomy/session state in `ops-conversations.js`, `ops-store.js`, `ops-render.js`, and the matching runtime session-status payload seam.
- Stop using goals polling as an authority for any selected-thread live surface in the active workspace.
- Preserve degraded reconnect or polling fallback as an explicit downgrade path instead of silently refreshing selected-thread autonomy identity from polling.
- Leave transcript inline session ownership, footer dock behavior, left-rail cues, and switch or restore continuity unchanged.
- Avoid adding a new transport, a new panel, or any second live-detail owner in the center pane.

## Deliverable

Expose one conversation-first selected-thread workspace where selected-thread blocker, verifier, proposal, and apply state are sourced only from session-status bootstrap plus SSE while the conversation is active, and degraded transport visibly downgrades that workspace instead of silently falling back to goals-poll authority.
