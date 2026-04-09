# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path and a clearer selected-row live-owner treatment, but the rest of the left rail still makes thread choice more inferential than it should be. The remaining friction is that non-selected rows can still look too generic, because their snapshot label precedence and preview selection do not consistently surface the most useful state and content.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only non-selected conversation-card snapshot labeling and preview selection on top of the existing rail contract.
- Leave selected-thread transport, selected-row live-owner treatment, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but normalize every non-selected conversation row to one fixed-priority snapshot state chip and one bounded recent preview line while preserving the selected row as the only live-owned lane.
