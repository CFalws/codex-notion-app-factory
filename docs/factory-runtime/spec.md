# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The desktop workspace is now conversation-first, but the selected-thread footer rail still mixes its compact chips with sentence-level status copy. The remaining friction is live-progress legibility: the composer-adjacent rail should read at a glance through compact transport, phase, and proposal signals instead of asking the operator to parse explanatory text while reading the transcript.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the selected-thread composer-adjacent live rail render contract and its focused verification artifacts.
- Leave the selected-thread timeline, header minimization, submit handoff, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and footer dock, but convert the selected-thread session strip into a chip-first live rail with compact transport, phase, proposal, provenance, and action cues while leaving richer autonomy detail in the existing secondary panel.
