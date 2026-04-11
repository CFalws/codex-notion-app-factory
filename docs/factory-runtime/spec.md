# Factory Runtime Spec

## Iteration

- current iteration: `112`
- bounded focus: `composer utility controls collapse into one explicit closed-by-default utility affordance`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, switching continuity, and transcript session-lane visibility are already established. The remaining gap is composer ergonomics: apply and auto-open controls still risk reading like a second footer surface instead of a collapsed-by-default utility affordance beneath one always-ready chat composer.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread session authority, transcript session lane, and composer strip contracts unchanged.
- Do not introduce a new transport, polling path, or footer status surface.
- Keep the utility menu collapsed by default on desktop and phone widths.
- Reuse the existing composer utility controls and footer DOM instead of creating another panel.
- Keep machine-readable open or closed datasets and aria state in sync from one helper.
- Close the utility affordance on selected-thread switches, app changes, and send transitions.
- Prevent live session updates from reopening or restyling the utility affordance as session-status chrome.
- Preserve degraded, reconnect, restore, switching, terminal, and no-selection selected-thread behavior from earlier iterations.

## Deliverable

Define and verify one composer utility-menu contract where apply and auto-open controls stay collapsed behind a compact toggle by default, expose explicit open or closed datasets and aria state, and close immediately on selected-thread and send transitions without becoming part of the live session status surface.
