# Deploy Plan

## Default Target

Deploy `Habit Tracker PWA` as a static PWA.

Recommended order:

1. GitHub Pages
2. Cloudflare Pages
3. Vercel

## Deployment Steps

1. Commit and push the repository to GitHub.
2. Enable GitHub Pages on the repository.
3. Let the GitHub Actions workflow build `.pages-dist` from `examples/generated_apps`.
4. Open the deployed `/habit-tracker-pwa/` URL on a phone.
5. Add it to the home screen.

## When To Add A Backend

Add a backend only if one of these becomes necessary:

- authenticated sync across devices
- shared data between users
- notifications or scheduled jobs
- AI calls or secret-bearing APIs
