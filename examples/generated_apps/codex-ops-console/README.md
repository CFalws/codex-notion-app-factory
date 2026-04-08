# Codex Ops Console

Phone-first web console for the stateful Codex CLI runtime.

## Purpose

This app is the operator surface for the backend runtime:

- choose an existing app lane
- submit a new maintenance request
- poll the runtime job status
- open the deployed app after the job completes

## Runtime Dependency

The console is static and deploys to GitHub Pages, but it expects the Python runtime to be reachable over HTTP.

Set these values inside the app before sending a request:

- runtime URL
- `X-API-Key` value configured on the server

The console stores both values locally on the phone, lets you choose an existing app lane, sends a maintenance request, polls the job, and keeps the target app link ready so you can open the updated PWA immediately after the job completes.
