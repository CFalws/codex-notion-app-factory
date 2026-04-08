# Factory Runtime Spec

## Request

- title: `대화 세션 기준으로 요청 제목 제거`
- source: `mobile-ops-console`
- execution mode: `build`

## Problem

The Codex Ops Console still asks the operator to provide a request title for each message. In a conversation-driven maintenance flow that extra field adds friction on phone and duplicates the role of the conversation session itself.

## Target User

The primary user is the phone operator maintaining apps through the personal app factory runtime.

## Constraints

- Preserve continuity of the existing `factory-runtime` lane.
- Keep the web app deployable as a static GitHub Pages-compatible app.
- Limit edits to the allowed proposal paths.

## Deliverable

Update the Codex Ops Console and runtime request handling so operators can send a message without a separate request title while preserving conversation continuity and proposal-mode compatibility.
