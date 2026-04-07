# Habit Tracker PWA

This app was generated as a mobile-first PWA scaffold from a single idea statement.

## What It Is

Habit Tracker PWA is a phone-ready personal tracker generated from your idea: A habit tracker for my phone that lets me add daily habits, check them off quickly, and see streaks without needing my laptop runtime.

## Why This Shape

- installable from a phone home screen
- works as a static deployment
- stores data locally by default
- does not require your development machine to stay awake

## Files

- `web/index.html`
- `web/styles.css`
- `web/app.js`
- `web/manifest.webmanifest`
- `web/service-worker.js`
- `preview.py`
- `deploy_plan.md`

## Local Preview

```bash
cd codex-notion-app-factory/examples/generated_apps/habit-tracker-pwa
python preview.py
```

Then open `http://127.0.0.1:4173`.

## Phone Install

1. Commit and push this repository to GitHub.
2. Enable GitHub Pages for the repository and let the `Deploy Generated Apps To GitHub Pages` workflow run.
3. Open the generated Pages URL for `/habit-tracker-pwa/` on your phone.
4. Use the browser's add-to-home-screen flow.

## Notes

This scaffold is local-first. If you want cross-device sync later, add a small authenticated backend without changing the mobile shell.

## GitHub Pages

The repository includes a workflow at `.github/workflows/deploy-generated-apps-pages.yml` that builds a Pages site from all generated apps.
