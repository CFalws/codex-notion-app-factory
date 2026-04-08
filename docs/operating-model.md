# Operating Model

## End-to-End Loop

1. Capture a new app request through the runtime console or another HTTP client
2. Record the execution mode, primary device, and launch surface
3. Resolve the request to an existing app workspace when possible
4. Load the app's stored session record and memory snapshot
5. Open Codex in the target workspace
6. Codex reads the request payload from the runtime layer
7. Codex creates or updates planning artifacts
8. Codex selects the smallest mobile-usable delivery target
9. Codex implements the requested app or change
10. Codex updates the app session record, memory, and deployment notes

The repository can also run a persistent HTTP runtime. In that mode, a phone-facing web console submits a request to a Python API, the API resolves the app id, reuses the stored session id, and runs the task through the local Codex CLI with `exec` or `exec resume`.

## Why This Loop Works

- intake is simple
- execution is structured
- output is inspectable
- the system can be reused for multiple small personal products
- the delivery target is chosen for real usage, not only for local demo quality

## Practical Usage

This workflow is especially useful for:

- small productivity tools
- automation utilities
- quick internal dashboards
- single-purpose web tools
- installable mobile utilities
- personal trackers and check-in apps

## Failure Modes

The workflow becomes weak if:

- requests are too vague
- tags are inconsistent
- existing app updates are treated like brand-new work every time
- artifacts are not saved
- the implementation environment is not documented
- the output only works while the development computer is running

## What Makes It Portfolio-Ready

A strong portfolio entry should show:

- the intake contract
- the execution rules
- the generated artifacts
- at least one real project produced by the loop
- a clear path from idea to phone-usable deployment
