# GitHub Pages Automation

## Goal

Deploy generated phone-facing apps to a phone-accessible URL automatically after a push to `main`.

## How It Works

The repository contains:

- `.github/workflows/deploy-generated-apps-pages.yml`
- `scripts/build_pages_site.py`

The workflow runs on pushes that affect generated apps or Pages build scripts.

## Build Strategy

GitHub Pages gives the repository one Pages site.

Because of that, the deployment does not publish one app at a time. It assembles all generated apps into a single static site:

- the root index lists generated apps
- each app is copied to `/<slug>/`
- each PWA uses relative asset paths so it works under a subpath
- a launcher manifest and service worker make the root app bundle installable

This automation only covers the static web surfaces.

It does not deploy the stateful Python runtime. The runtime is expected to run separately on a VPS or another always-on machine.

When self-edit proposals are applied on the VPS runtime, the local server checkout can optionally push `main` back to GitHub so Pages redeploys automatically. That requires Git credentials to be configured on the server-side checkout.

## Required Repository Setup

1. Push the repository to GitHub.
2. Open repository settings.
3. Enable GitHub Pages and choose GitHub Actions as the source.
4. Push changes to `main` or run the workflow manually.

## Output Shape

The build script writes `.pages-dist/` with:

- `index.html`
- `manifest.webmanifest`
- `service-worker.js`
- one folder per generated app slug
- `.nojekyll`

## Expected Result

After deployment, the site should look like:

- `/` for the generated apps index
- `/habit-tracker-pwa/` for the habit tracker example
- `/codex-ops-console/` for the runtime operator console

The exact hostname depends on the repository's GitHub Pages URL.
