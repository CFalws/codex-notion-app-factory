# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The desktop workspace is materially closer to a conversation-first session now, but on phone widths the sidebar still owns the first visible surface. That means users reach app and thread controls before the active conversation and composer, which breaks the intended live-session feel.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

On narrow screens, keep the conversation workspace visible first and move the existing app and thread navigation into a one-tap drawer or sheet, while preserving the current autonomy rail, live run row, and append provenance markers in the active conversation pane.
