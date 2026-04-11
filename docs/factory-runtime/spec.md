# Factory Runtime Spec

## Iteration

- current iteration: `122`
- bounded focus: `selected-thread switch path keeps one mounted center shell and one compact transition placeholder`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership is already explicit in the rail, center lane, footer bar, and header datasets. The remaining gap is transition continuity: intentional thread switches still need a stricter contract proving the center shell stays mounted, old-thread ownership clears immediately, and the workspace does not fall back to the true empty view while the new selected thread attaches.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, center live-lane, footer session bar, header ownership surface, and polling-fallback contracts unchanged.
- Do not introduce a new transport, polling path, backend protocol, persistence layer, or a second transition surface.
- Reuse the existing selected-thread switch placeholder and mounted composer path instead of adding another transition controller.
- Keep the center conversation shell and bottom-fixed composer mounted during intentional thread switches and show exactly one compact transition placeholder until the target thread attaches.
- Clear prior-thread live ownership immediately on switch and expose machine-readable evidence that the switch placeholder owns the workspace while old ownership is cleared.
- Preserve the true empty-state path only for genuine no-selection idle, not for intentional thread switches.

## Deliverable

Define and verify one selected-thread switch continuity contract where intentional thread switches keep the center shell mounted, show exactly one compact transition placeholder, clear old ownership immediately, and avoid the true empty path until the new selected thread attaches.
