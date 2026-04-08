# Factory Runtime Spec

## Request

- title: `런타임 URL은 고정하자`
- source: `mobile-ops-console`
- execution mode: `build`

## Problem

The Codex Ops Console currently asks the operator to type the runtime URL before loading apps or sending a request. For this runtime lane the backend IP is stable, so repeating that step adds friction on phone.

## Target User

The primary user is the phone operator maintaining apps through the personal app factory runtime.

## Constraints

- Preserve continuity of the existing `factory-runtime` lane.
- Keep the web app deployable as a static GitHub Pages-compatible app.
- Limit edits to the allowed proposal paths.

## Deliverable

Update the Codex Ops Console so it uses a fixed runtime base URL by default and no longer depends on re-entering the backend endpoint for each session.
