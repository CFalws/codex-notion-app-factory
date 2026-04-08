# Sample Focus Launcher

This is a real sample app produced from the example structured request in this repository.

For request provenance and execution notes, see:

- `request_snapshot.md`
- `execution_trace.md`

## What It Does

- accepts a vague chore or task
- converts it into one concrete first action
- stores recent launches locally
- provides a minimal interface optimized for immediate action

## Run

```bash
cd codex-notion-app-factory/examples/generated_apps/sample-focus-launcher
python server.py
```

Then open `http://127.0.0.1:8031`.

## Files

- `server.py`
  Tiny Python web server and API.
- `launcher.py`
  Task normalization and first-action generation logic.
- `web/index.html`
  Frontend UI.
- `web/styles.css`
  Frontend styling.
- `web/app.js`
  Frontend interaction logic.
- `request_snapshot.md`
  Simulated structured intake request content.
- `execution_trace.md`
  Build and validation trace for this sample.
