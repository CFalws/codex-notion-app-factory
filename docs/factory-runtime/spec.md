# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path, stronger rail clarity, and a compact live activity bar, but the active thread still flattens some realtime progression back into generic execution wording. The remaining friction is that the selected conversation should expose exact proposal, review, verify, auto-apply, ready, and applied progression directly in the center workspace instead of making the operator infer it from generic running language.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only selected-thread phase presentation inside the existing header and composer-adjacent live rail.
- Leave selected-thread transport ownership, non-selected thread rendering, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but make the selected thread header and composer-adjacent live rail present exact SSE-driven phase progression with phase-specific detail copy for proposal, review, verify, auto apply, ready, and applied states.
