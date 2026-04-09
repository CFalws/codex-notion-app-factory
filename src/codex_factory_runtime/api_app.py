from __future__ import annotations

import secrets

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .agent_runtime import CodexAgentsRuntime
from .api_routes import register_routes
from .api_runtime_context import RuntimeApiContext
from .config import RuntimeSettings, load_settings
from .state import RuntimeState


def _requires_api_key(request: Request, settings: RuntimeSettings) -> bool:
    return (
        request.method != "OPTIONS"
        and request.url.path.startswith("/api/")
        and bool(settings.runtime_api_key)
    )


def _configure_cors(app: FastAPI, settings: RuntimeSettings) -> None:
    if settings.cors_allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allowed_origins,
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        return

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app(settings: RuntimeSettings | None = None) -> FastAPI:
    settings = settings or load_settings()
    state = RuntimeState(settings)
    runtime = CodexAgentsRuntime(settings, state)
    context = RuntimeApiContext(settings=settings, state=state, runtime=runtime)

    app = FastAPI(
        title="Codex App Factory Runtime",
        version="0.2.0",
        summary="Conversation-aware Codex CLI runtime for personal app maintenance.",
    )
    _configure_cors(app, settings)

    @app.middleware("http")
    async def require_api_key(request: Request, call_next):  # type: ignore[no-untyped-def]
        if not _requires_api_key(request, settings):
            return await call_next(request)

        api_key = request.headers.get("x-api-key", "")
        if not secrets.compare_digest(api_key, settings.runtime_api_key):
            return JSONResponse(status_code=401, content={"detail": "Invalid or missing X-API-Key header."})
        return await call_next(request)

    register_routes(app, context)
    return app
