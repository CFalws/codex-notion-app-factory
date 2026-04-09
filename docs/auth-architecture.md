# Auth Architecture

## Goal

Keep the runtime's authentication boundary portable across clouds.

The application should not depend directly on GCP IAP semantics beyond one adapter. Instead, the runtime should consume a normalized authenticated identity from a trusted front door.

## Current Model

The runtime supports a provider chain configured through `CODEX_FACTORY_AUTH_PROVIDERS`.

Supported providers:

- `loopback`
  - trusts requests that originate from `127.0.0.1`, `::1`, `localhost`, or the FastAPI `TestClient`
  - intended for local health checks and server-local smoke tests
- `api_key`
  - compatibility path for legacy direct clients
- `iap`
  - validates `x-goog-iap-jwt-assertion`
  - enforces the configured IAP audience
  - optionally enforces an allowlist of authenticated user emails

## Recommended Production Shape

On GCP, prefer:

- an HTTPS load balancer in front of the VM
- Identity-Aware Proxy enabled on the backend service
- runtime auth providers set to `loopback,iap`
- direct public access to the backend VM blocked where possible

That gives two trust boundaries:

- `loopback` for internal smoke tests that run on the VM itself
- `iap` for operator traffic that enters through the Google front door

## Portability Rule

The runtime should treat identity as:

- `subject`
- `email`
- `auth_source`
- `claims`

Cloud-specific verification should live only in the auth provider implementation.

That means a later move to another front door should only require a new adapter such as:

- `cloudflare_access`
- `oidc_proxy`
- `mtls`

The FastAPI routes and the runtime core should not need to know which cloud issued the identity.

## Required Environment Variables

For GCP IAP:

- `CODEX_FACTORY_AUTH_PROVIDERS=["loopback","iap"]`
- `CODEX_FACTORY_IAP_AUDIENCE=<iap-backend-audience>`
- `CODEX_FACTORY_ALLOWED_USER_EMAILS=["you@example.com"]`

Legacy compatibility only:

- `CODEX_FACTORY_API_KEY=<shared-secret>`

## Verification

- `make verify`
  - validates the auth abstraction locally, including the IAP adapter contract through a mocked assertion verifier
- `make verify-gce`
  - exercises the deployed runtime through server-local loopback access

When the front door is switched fully to IAP, end-user access should be verified through the load balancer path rather than direct VM access.
