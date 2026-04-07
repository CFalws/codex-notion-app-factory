# Operating Model

## End-to-End Loop

1. Capture a new app request in Notion
2. Add the appropriate Codex execution tag
3. Open Codex in the target workspace
4. Let Codex fetch the tagged request through MCP
5. Codex creates planning artifacts
6. Codex implements the requested app or change
7. Codex leaves a delivery summary
8. Request is moved or retagged in Notion after completion

## Why This Loop Works

- intake is simple
- execution is structured
- output is inspectable
- the system can be reused for multiple small personal products

## Practical Usage

This workflow is especially useful for:

- small productivity tools
- automation utilities
- quick internal dashboards
- personal CLI apps
- single-purpose web tools

## Failure Modes

The workflow becomes weak if:

- requests are too vague
- tags are inconsistent
- artifacts are not saved
- the implementation environment is not documented

## What Makes It Portfolio-Ready

A strong portfolio entry should show:

- the intake contract
- the execution rules
- the generated artifacts
- at least one real project produced by the loop
