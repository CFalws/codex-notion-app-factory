# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread footer can still feel more like a request form than a conversation composer if secondary controls sit too close to the primary send path. Apply and auto-open should remain reachable, but only through one compact, default-closed utility affordance so the textarea and send action stay dominant on desktop and phone widths.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing composer footer structure, utility toggle state, and selected-thread ownership datasets instead of widening transport scope.
- Constrain this iteration to footer utility ergonomics in the selected-thread workspace.
- Keep the selected-thread SSE path, footer live strip, side-panel behavior, and rail snapshot behavior unchanged.
- Leave transport scope, runtime APIs, polling fallback rules, and proposal flow unchanged while tightening the footer control layout.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but preserve a compact footer utility cluster: keep the textarea and primary send action visually dominant, hold apply and auto-open behind one default-closed utility toggle with explicit open or closed state, and avoid introducing a second footer status surface or a form-like control row.
