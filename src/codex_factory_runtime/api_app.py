from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .agent_runtime import CodexAgentsRuntime
from .api_routes import register_routes
from .api_runtime_context import RuntimeApiContext
from .auth import Authenticator
from .config import RuntimeSettings, load_settings
from .runtime_goals import GoalRuntime
from .state import RuntimeState


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
    context = RuntimeApiContext(settings=settings, state=state, runtime=runtime, goals=GoalRuntime())
    authenticator = Authenticator(settings)

    app = FastAPI(
        title="Codex App Factory Runtime",
        version="0.3.0",
        summary="Conversation-aware Codex CLI runtime for personal app maintenance.",
    )
    _configure_cors(app, settings)

    @app.middleware("http")
    async def require_identity(request: Request, call_next):  # type: ignore[no-untyped-def]
        if not authenticator.requires_auth(request):
            return await call_next(request)

        try:
            identity = authenticator.authenticate(request)
        except PermissionError as exc:
            return JSONResponse(status_code=403, content={"detail": str(exc)})
        except RuntimeError as exc:
            return JSONResponse(status_code=500, content={"detail": str(exc)})

        if identity is None:
            return JSONResponse(status_code=401, content={"detail": "Request did not satisfy any configured authentication provider."})

        request.state.identity = identity
        return await call_next(request)

    register_routes(app, context)
    return app
