# Factory Runtime Spec

## Iteration

- current iteration: `240`
- bounded focus: `compress selected-thread helper prose into one compact chip-first session surface without changing session-status-plus-SSE authority`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, streamed autonomy identity, unified header chrome, and the removal of selected-thread goals-poll authority are already present. The remaining bounded gap is presentation density: sentence-style helper copy still makes the selected-thread workspace feel less like one compact Codex-style session surface during handoff, switch, restore, and degraded paths.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the active selected conversation to behave like one live session whose ownership and phase cues are immediately readable without sentence-style helper text.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to selected-thread workspace presentation in `ops-render.js` and matching stylesheet and verifier artifacts.
- Preserve the existing `session_status` plus SSE authority path and explicit degraded fallback behavior unchanged.
- Keep the transcript inline session block as the only in-timeline live progress surface.
- Leave footer dock behavior, left-rail cues, and switch or restore continuity unchanged.
- Avoid adding a new transport, a new panel, or any second live-detail owner in the center pane.

## Deliverable

Expose one conversation-first selected-thread workspace where the header summary, transition placeholder, inline session block, and composer-adjacent strip use compact chip-first owner, phase, and target cues while the existing selected-thread `session_status` plus SSE authority path and degraded downgrade behavior remain intact.
