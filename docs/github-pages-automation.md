# GitHub Pages Automation

## Goal

Deploy generated apps to a phone-accessible URL automatically after a push to `main`.

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

## Required Repository Setup

1. Push the repository to GitHub.
2. Open repository settings.
3. Enable GitHub Pages and choose GitHub Actions as the source.
4. Push changes to `main` or run the workflow manually.

## Output Shape

The build script writes `.pages-dist/` with:

- `index.html`
- one folder per generated app slug
- `.nojekyll`

## Expected Result

After deployment, the site should look like:

- `/` for the generated apps index
- `/habit-tracker-pwa/` for the habit tracker example

The exact hostname depends on the repository's GitHub Pages URL.
