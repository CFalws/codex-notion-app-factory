# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has compact header, rail, and footer cues, but live progress still reads like chrome around the conversation instead of part of the conversation itself. That leaves the transcript feeling passive even when the selected thread is actively handing off or streaming through the intended SSE path.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append-stream, pending handoff, live-follow, and live-run selectors instead of adding a new runtime state source.
- Constrain this iteration to one compact inline transcript-tail live session block in the selected conversation pane.
- Keep the left rail, runtime APIs, side-panel behavior, SSE transport, and broader workspace layout unchanged.
- Clear the inline block immediately on first real assistant append, terminal completion, reconnect downgrade, polling fallback, or thread switch.

## Deliverable

Render exactly one compact inline live session block at the transcript tail for the selected thread only, showing HANDOFF before the first assistant append and LIVE during healthy SSE-owned progress, with immediate clearing on degraded, switched, or terminal paths.
