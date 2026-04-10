# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread timeline state is already converging into the conversation surface, but intentional thread switches still depend on proving that the center shell stays mounted and never flashes the generic empty workspace. Without that continuity, the live-session illusion breaks exactly when the operator changes focus.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread transition state, composer shell, and thread-switch placeholder instead of changing backend transport or state schema.
- Keep the change bounded to the selected-thread switch path and its verification contract.
- Preserve true empty-state rendering for no-selection idle only.

## Deliverable

Define and verify one compact selected-thread switch placeholder path so intentional switches keep the same center workspace shell and bottom-fixed composer visible, clear old live ownership immediately, and reserve the generic empty state for true no-selection idle only.
