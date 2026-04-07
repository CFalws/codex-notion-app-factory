# Mobile-First Operating Model

## Objective

Turn an idea captured in Notion into a personal app that is actually usable from a phone.

The default assumption is:

- the primary user is you
- the app should open quickly on mobile
- the app should survive without your laptop being awake
- the app should be deployable with the smallest reliable surface area

## Default Delivery Rule

If a request does not explicitly require native APIs, the default target is an installable PWA.

That means the generated app should usually have:

- responsive mobile UI
- manifest file
- service worker
- offline or local-first behavior where possible
- static-host-friendly build output

## Why PWA First

For personal tools, PWA is usually the best tradeoff:

- faster to generate than React Native or Flutter
- one codebase
- easy to deploy on Cloudflare Pages, Vercel, or GitHub Pages
- easy to add to the home screen
- no app store review loop

## Escalation Rule

Only escalate past PWA when the request clearly needs one of these:

- health or sensor APIs not viable in the browser
- native notifications that must be guaranteed beyond web support
- background execution constraints the browser cannot satisfy
- app store distribution
- camera, files, or hardware integrations that are materially better natively

In that case:

1. keep the product brief the same
2. preserve the mobile-first UX
3. wrap with Capacitor if possible
4. choose full native only if wrapping is insufficient

## Persistence Rule

Choose persistence in this order:

1. local-first storage in browser
2. optional authenticated sync
3. server-backed primary storage only when local-first is inadequate

For personal apps, this keeps deployment simple and reduces maintenance.

## Agentic Build Loop

1. Capture the app request in Notion
2. Infer the smallest mobile-usable delivery target
3. Generate `spec.md`, `implementation_plan.md`, and `tasks.md`
4. Scaffold the app with installability and deployment in mind
5. Produce a runnable preview
6. Produce deployment instructions or config
7. Leave a delivery summary that includes phone install steps

## Recommended Output Contract

Each mobile-oriented build should leave behind:

- `brief.md`
- `spec.md`
- `implementation_plan.md`
- `tasks.md`
- app source code
- `deploy_plan.md`
- `README.md` with phone install steps

## Deployment Default

Use static hosting first.

Recommended order:

1. Cloudflare Pages
2. Vercel
3. GitHub Pages

If the app needs a backend:

- add the thinnest possible API layer
- prefer serverless or edge functions
- keep the mobile client usable even if sync is unavailable

## Example

For a habit tracker:

- delivery target: installable PWA
- storage: localStorage or IndexedDB
- deployment: static hosting
- phone access: home screen install
- optional sync later: Supabase or a tiny authenticated API
