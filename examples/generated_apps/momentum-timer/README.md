# Momentum Timer

This sample app was implemented from a real structured request captured during this session.

## Source Request

- Local request snapshot: `request_snapshot.md`
- Local intake trace: `intake_trace.md`

## What It Does

- accepts a task
- returns one concrete first action
- starts a 3-minute countdown immediately
- stores recent launches locally

## Run

```bash
cd codex-notion-app-factory/examples/generated_apps/momentum-timer
python server.py
```

Then open `http://127.0.0.1:8041`.

## Main Files

- `server.py`
- `momentum.py`
- `web/index.html`
- `web/styles.css`
- `web/app.js`
- `validation_report.md`
