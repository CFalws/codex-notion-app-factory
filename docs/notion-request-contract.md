# Notion Request Contract

Each implementation request should follow a stable structure so Codex can act on it with minimal clarification.

## Required Fields

- `Project Name`
- `Problem`
- `Desired Outcome`
- `Primary User`
- `Primary Device`
- `Tag`

## Recommended Fields

- `Preferred Stack`
- `Constraints`
- `References`
- `Definition of Done`
- `Notes`
- `Launch Surface`
- `Offline Requirement`
- `Data Model`
- `Deployment Target`

## Tag Semantics

- `codex-build`
  Build or modify the app directly
- `codex-spec`
  Create planning artifacts only
- `codex-review`
  Review an implementation or code change

## Minimum Viable Request Example

- Project Name: Focus Launcher
- Problem: I procrastinate when starting small chores
- Desired Outcome: A tiny tool that gives me one concrete first action
- Primary User: Me
- Primary Device: iPhone
- Tag: codex-build

## Why The Contract Exists

The contract reduces ambiguity and makes the pipeline more reliable.

Without a structured request shape, the workflow becomes a loose prompt chain.
With a contract, it becomes an execution system.
