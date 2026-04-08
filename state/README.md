# State

This directory stores durable app state for the maintenance loop.

Tracked:

- `registry/apps/`
- `memory/`
- `requests/.gitkeep`

Ignored:

- `gcloud/`
- `runtime/`
- per-request JSON history under `requests/`

Use `scripts/manage_app_sessions.py` to create and update app records.
