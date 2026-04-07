# Momentum Timer

This sample app was implemented from a real Notion request page created and fetched through MCP during this session.

## Source Request

- Notion page: `https://www.notion.so/33a75a96562381acab11eb9a05246a0a`
- Local request snapshot: `notion_request_snapshot.md`
- Local fetch trace: `mcp_fetch_trace.md`

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
