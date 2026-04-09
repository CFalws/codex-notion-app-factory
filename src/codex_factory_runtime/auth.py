from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Any

from fastapi import Request

from .config import RuntimeSettings

IAP_JWT_HEADER = "x-goog-iap-jwt-assertion"
IAP_ISSUERS = {"https://cloud.google.com/iap"}
LOOPBACK_HOSTS = {"127.0.0.1", "::1", "localhost", "testclient"}
TAILSCALE_LOGIN_HEADER = "tailscale-user-login"
TAILSCALE_NAME_HEADER = "tailscale-user-name"


@dataclass(frozen=True)
class AuthenticatedIdentity:
    subject: str
    email: str
    auth_source: str
    claims: dict[str, Any]


class Authenticator:
    def __init__(self, settings: RuntimeSettings) -> None:
        self.settings = settings
        self.providers = self._build_providers(settings)

    def _build_providers(self, settings: RuntimeSettings) -> list[IdentityProvider]:
        providers: list[IdentityProvider] = []
        for name in settings.auth_providers:
            normalized = name.strip().lower()
            if normalized == "loopback":
                providers.append(LoopbackIdentityProvider())
            elif normalized == "api_key":
                providers.append(ApiKeyIdentityProvider(settings))
            elif normalized == "iap":
                providers.append(IapIdentityProvider(settings))
            elif normalized == "tailscale":
                providers.append(TailscaleIdentityProvider())
            else:
                raise ValueError(f"Unsupported auth provider: {name}")
        return providers

    def requires_auth(self, request: Request) -> bool:
        return request.method != "OPTIONS" and request.url.path.startswith("/api/") and bool(self.providers)

    def authenticate(self, request: Request) -> AuthenticatedIdentity | None:
        for provider in self.providers:
            identity = provider.authenticate(request)
            if identity is None:
                continue
            self._authorize(identity)
            return identity
        return None

    def _authorize(self, identity: AuthenticatedIdentity) -> None:
        if identity.auth_source == "loopback":
            return
        allowed = self.settings.allowed_user_emails
        if allowed and identity.email not in allowed:
            raise PermissionError("Authenticated user is not allowed to access this runtime.")


class IdentityProvider:
    name = "provider"

    def authenticate(self, request: Request) -> AuthenticatedIdentity | None:
        raise NotImplementedError


class LoopbackIdentityProvider(IdentityProvider):
    name = "loopback"

    def authenticate(self, request: Request) -> AuthenticatedIdentity | None:
        host = (request.client.host if request.client else "").strip().lower()
        if host not in LOOPBACK_HOSTS:
            return None
        return AuthenticatedIdentity(
            subject=f"loopback:{host}",
            email="",
            auth_source=self.name,
            claims={"host": host},
        )


class ApiKeyIdentityProvider(IdentityProvider):
    name = "api_key"

    def __init__(self, settings: RuntimeSettings) -> None:
        self.api_key = settings.runtime_api_key

    def authenticate(self, request: Request) -> AuthenticatedIdentity | None:
        if not self.api_key:
            return None
        presented = request.headers.get("x-api-key", "")
        if not presented or not secrets.compare_digest(presented, self.api_key):
            return None
        return AuthenticatedIdentity(
            subject="api-key",
            email="",
            auth_source=self.name,
            claims={},
        )


class TailscaleIdentityProvider(IdentityProvider):
    name = "tailscale"

    def authenticate(self, request: Request) -> AuthenticatedIdentity | None:
        login = request.headers.get(TAILSCALE_LOGIN_HEADER, "").strip()
        if not login:
            return None
        display_name = request.headers.get(TAILSCALE_NAME_HEADER, "").strip()
        return AuthenticatedIdentity(
            subject=login,
            email=login,
            auth_source=self.name,
            claims={
                "login": login,
                "name": display_name,
            },
        )


class IapIdentityProvider(IdentityProvider):
    name = "iap"

    def __init__(self, settings: RuntimeSettings) -> None:
        self.expected_audience = settings.iap_expected_audience

    def authenticate(self, request: Request) -> AuthenticatedIdentity | None:
        token = request.headers.get(IAP_JWT_HEADER, "").strip()
        if not token:
            return None
        if not self.expected_audience:
            raise RuntimeError("CODEX_FACTORY_IAP_AUDIENCE must be configured when the iap auth provider is enabled.")
        claims = self.verify_iap_assertion(token)
        issuer = str(claims.get("iss") or "").strip()
        if issuer not in IAP_ISSUERS:
            raise PermissionError("Untrusted IAP issuer.")
        audience = str(claims.get("aud") or "").strip()
        if audience != self.expected_audience:
            raise PermissionError("Unexpected IAP audience.")
        subject = str(claims.get("sub") or "").strip()
        email = str(claims.get("email") or "").strip()
        if not subject:
            raise PermissionError("IAP assertion is missing a subject.")
        return AuthenticatedIdentity(
            subject=subject,
            email=email,
            auth_source=self.name,
            claims=claims,
        )

    def verify_iap_assertion(self, token: str) -> dict[str, Any]:
        try:
            from google.auth.transport.requests import Request as GoogleAuthRequest
            from google.oauth2.id_token import verify_token
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "google-auth is required when the iap auth provider is enabled. Install project dependencies first."
            ) from exc

        claims = verify_token(token, GoogleAuthRequest(), audience=self.expected_audience)
        if not isinstance(claims, dict):
            raise PermissionError("Invalid IAP assertion payload.")
        return claims
