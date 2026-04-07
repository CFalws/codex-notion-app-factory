# Showcase

This file is the fastest way to inspect the end-to-end result.

## 1. Workflow Definition

- System overview: [README.md](/Users/emil/emil/python/codex-notion-app-factory/README.md)
- Execution rules: [AGENTS.md](/Users/emil/emil/python/codex-notion-app-factory/AGENTS.md)
- Operating model: [operating-model.md](/Users/emil/emil/python/codex-notion-app-factory/docs/operating-model.md)
- Request contract: [notion-request-contract.md](/Users/emil/emil/python/codex-notion-app-factory/docs/notion-request-contract.md)

## 2. Sample Intake Request

- Request snapshot: [request_snapshot.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/request_snapshot.md)
- Brief: [brief.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/brief.md)

## 3. Generated Planning Artifacts

- Product spec: [spec.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/spec.md)
- Implementation plan: [implementation_plan.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/implementation_plan.md)
- Tasks: [tasks.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/tasks.md)
- Delivery summary: [delivery_summary.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/delivery_summary.md)

## 4. Implemented App

- App README: [README.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/README.md)
- Backend logic: [launcher.py](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/launcher.py)
- HTTP server: [server.py](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/server.py)
- Frontend shell: [index.html](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/web/index.html)
- Frontend styling: [styles.css](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/web/styles.css)
- Frontend behavior: [app.js](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/web/app.js)

## 5. Verification Outputs

- Execution trace: [execution_trace.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/execution_trace.md)
- Validation report: [validation_report.md](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/validation_report.md)
- Raw validation data: [validation_results.json](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/validation_results.json)
- Local persistence example: [history.json](/Users/emil/emil/python/codex-notion-app-factory/examples/generated_apps/sample-focus-launcher/history.json)

## 6. Fast Narrative

The shortest credible story for this repository is:

1. A request is captured in Notion and tagged for execution.
2. Codex reads the request contract and produces planning artifacts.
3. Codex implements the sample app in the target workspace.
4. Validation outputs are written so the result is inspectable.
