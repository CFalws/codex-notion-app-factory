# Factory Runtime Spec

## Iteration

- current iteration: `159`
- bounded focus: `promote canonical selected-thread session_status into one compact center-pane live session strip`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The runtime now needs one selected-thread session strip in the center workspace that reads directly from canonical append-SSE `session_status` instead of mixing phase and autonomy inference across multiple UI helpers.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation pane to expose one compact live session strip that immediately shows phase and path state through the intended append-SSE path.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to canonical append-SSE `session_status` transport plus one selected-thread center-pane strip, focused verifier updates, and doc updates.
- Keep `api_runtime_context.py` as the sole producer of canonical `session_status`.
- Do not change composer docking, transcript append ownership, footer ownership rules, rail mirroring, or secondary-panel behavior.
- Reuse existing selected-thread session switch, restore, and authority clearing rules.
- Render one compact center-pane live session strip above the transcript for the selected thread only.
- Demote reconnect and polling fallback explicitly instead of looking healthy.
- Clear stale selected-thread ownership immediately on switch, terminal completion, deselection, or thread loss of authority.
- Never make a non-selected thread appear live-owned.

## Deliverable

Emit canonical selected-thread `session_status` over append SSE and render one compact center-pane live session strip from that payload without moving transcript or composer ownership.
