# Auth Architecture

## Goal

Keep the runtime's authentication boundary portable across clouds while optimizing the default operator path for private personal use.

The application should not depend directly on one front door. It should consume a normalized authenticated identity from a trusted proxy or network path.

## Current Model

The runtime supports a provider chain configured through `CODEX_FACTORY_AUTH_PROVIDERS`.

Supported providers:

- `loopback`
  - trusts requests that originate from `127.0.0.1`, `::1`, `localhost`, or the FastAPI `TestClient`
  - intended for local health checks and server-local smoke tests
- `tailscale`
  - trusts Tailscale Serve identity headers such as `Tailscale-User-Login`
  - intended for operator traffic that reaches the runtime through a tailnet HTTPS URL
- `api_key`
  - compatibility path for legacy direct clients
- `iap`
  - validates `x-goog-iap-jwt-assertion`
  - enforces the configured IAP audience
  - optionally enforces an allowlist of authenticated user emails

## Recommended Production Shape

For a personal operator workflow, prefer:

- Tailscale installed on the VM and operator devices
- `tailscale serve` publishing `http://127.0.0.1:8787` to a tailnet HTTPS URL
- runtime auth providers set to `loopback,tailscale`
- public VM ingress on ports 80 and 443 disabled

That gives two trust boundaries:

- `loopback` for internal smoke tests that run on the VM itself
- `tailscale` for operator traffic that enters through the tailnet URL

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
- `iap`

The FastAPI routes and runtime core should not need to know which platform issued the identity.

## Required Environment Variables

For Tailscale production:

- `CODEX_FACTORY_AUTH_PROVIDERS=["loopback","tailscale"]`
- `CODEX_FACTORY_ALLOWED_USER_EMAILS=["akdlzmf1123@gmail.com"]`

Optional alternatives:

- `CODEX_FACTORY_AUTH_PROVIDERS=["loopback","iap"]`
- `CODEX_FACTORY_IAP_AUDIENCE=<iap-backend-audience>`
- `CODEX_FACTORY_ALLOWED_USER_EMAILS=["you@example.com"]`

## Verification

- `make verify`
  - validates the auth abstraction locally, including mocked IAP and Tailscale provider coverage
- `make verify-gce`
  - exercises the deployed runtime through server-local loopback access
- `scripts/verify_deployed_console.sh`
  - exercises the tailnet HTTPS URL from an operator device

When the front door is switched fully to Tailscale, end-user access should be verified through the tailnet HTTPS URL rather than the VM public IP.
