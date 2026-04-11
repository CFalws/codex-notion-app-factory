# Factory Runtime Spec

## Iteration

- current iteration: `113`
- bounded focus: `intentional selected-thread switches preserve one compact transition workspace instead of flashing generic empty state`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, transcript session-lane visibility, and composer utility ergonomics are already established. The remaining gap is thread-switch continuity: intentional selected-thread changes still need an explicit continuity contract so operators see a deliberate attach state instead of inferring whether the workspace dropped into generic empty idle.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread session authority, transcript session lane, composer strip, and utility-menu contracts unchanged.
- Do not introduce a new transport, polling path, or backend switch protocol.
- Reuse the existing `threadTransition`, selected-thread session-status, and placeholder helpers instead of creating another switch model.
- Keep the center conversation shell and bottom-fixed composer mounted during intentional switches.
- Render exactly one compact selected-thread switching placeholder until snapshot or SSE attach for the target thread becomes authoritative.
- Distinguish intentional switch continuity from true no-selection idle through explicit datasets and copy.
- Clear old-thread live ownership immediately and keep non-selected threads from gaining live-owned treatment.
- Preserve degraded, reconnect, restore, terminal, and no-selection behavior from earlier iterations.

## Deliverable

Define and verify one selected-thread switch continuity contract where intentional switches keep the conversation shell and composer mounted, expose one compact switching placeholder with explicit datasets and summary copy, and reserve the generic empty workspace only for true no-selection idle.
