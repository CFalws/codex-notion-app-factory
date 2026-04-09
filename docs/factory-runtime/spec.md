# Factory Runtime Spec

## Request

- title: `앱의 사용성의 극대화`
- source: `mobile-ops-console`
- execution mode: `build`

## Problem

The previous UX pass added more UI, but not better flow. The console still feels like a collection of admin panels instead of a Codex-style conversation workspace. Dropdown-based conversation selection and fragmented action panels keep slowing down the main loop of read context, type, send, and verify.

## Target User

The primary user is the phone operator maintaining apps through the personal app factory runtime, with a secondary need for a denser desktop-grade control surface.

## Constraints

- Preserve continuity of the existing `factory-runtime` lane.
- Keep the web app deployable as a static GitHub Pages-compatible app.
- Limit edits to the allowed proposal paths.

## Deliverable

Reshape the Codex Ops Console into a chat-first workspace: remove low-value prompt scaffolding, make conversation browsing direct, keep the timeline central, and keep composition fast on both phone and desktop.
