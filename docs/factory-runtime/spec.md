# Factory Runtime Spec

## Request

- title: `앱의 사용성의 극대화`
- source: `mobile-ops-console`
- execution mode: `build`

## Problem

The Codex Ops Console works functionally, but it still feels like a thin admin page rather than a polished Codex Desktop-style workspace. Operators need better context retention, lower-friction message composition, and clearer sense of the active app lane without sacrificing phone usability.

## Target User

The primary user is the phone operator maintaining apps through the personal app factory runtime, with a secondary need for a denser desktop-grade control surface.

## Constraints

- Preserve continuity of the existing `factory-runtime` lane.
- Keep the web app deployable as a static GitHub Pages-compatible app.
- Limit edits to the allowed proposal paths.

## Deliverable

Upgrade the Codex Ops Console into a more desktop-like conversation workspace by improving composition flow, context visibility, and session continuity using the existing runtime API.
