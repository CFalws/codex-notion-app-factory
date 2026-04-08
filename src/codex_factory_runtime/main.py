from __future__ import annotations

import secrets
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .agent_runtime import CodexAgentsRuntime
from .config import RuntimeSettings, load_settings
from .state import RuntimeState, utc_now


class CreateRequestBody(BaseModel):
    app_id: str = Field(..., description="Registered app id to continue.")
    title: str = Field(..., description="Short title for the requested change.")
    request_text: str = Field(..., description="Full natural-language change request.")
    source: str = Field(default="ops-console", description="Origin label for traceability.")
    execute_now: bool = Field(default=True, description="Whether to start the agent run immediately.")


def _requires_api_key(request: Request, settings: RuntimeSettings) -> bool:
    return (
        request.method != "OPTIONS"
        and request.url.path.startswith("/api/")
        and bool(settings.runtime_api_key)
    )


def create_app(settings: RuntimeSettings | None = None) -> FastAPI:
    settings = settings or load_settings()
    state = RuntimeState(settings)
    runtime = CodexAgentsRuntime(settings, state)

    app = FastAPI(
        title="Codex App Factory Runtime",
        version="0.1.0",
        summary="Stateful Codex CLI runtime for personal app maintenance.",
    )

    if settings.cors_allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allowed_origins,
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=".*",
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.middleware("http")
    async def require_api_key(request: Request, call_next):  # type: ignore[no-untyped-def]
        if not _requires_api_key(request, settings):
            return await call_next(request)

        api_key = request.headers.get("x-api-key", "")
        if not secrets.compare_digest(api_key, settings.runtime_api_key):
            return JSONResponse(status_code=401, content={"detail": "Invalid or missing X-API-Key header."})
        return await call_next(request)

    async def run_job(job_id: str, app_id: str, request_payload: dict[str, Any]) -> None:
        try:
            await runtime.run_request(app_id, job_id, request_payload)
        except Exception as exc:  # noqa: BLE001
            state.update_job(
                job_id,
                status="failed",
                completed_at=utc_now(),
                error=str(exc),
            )

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "ok": True,
            "repo_root": str(settings.repo_root),
            "codex_command": settings.codex_command,
            "codex_home": str(settings.codex_home) if settings.codex_home is not None else "(default ~/.codex)",
            "codex_profile": settings.codex_profile,
            "codex_model": settings.codex_model or "(default)",
            "api_key_required": bool(settings.runtime_api_key),
        }

    @app.get("/api/apps")
    async def list_apps() -> list[dict[str, Any]]:
        return state.list_apps()

    @app.get("/api/apps/{app_id}")
    async def get_app(app_id: str) -> dict[str, Any]:
        try:
            return state.get_app(app_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/jobs/{job_id}")
    async def get_job(job_id: str) -> dict[str, Any]:
        try:
            return state.get_job(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/proposals/{job_id}")
    async def get_proposal(job_id: str) -> dict[str, Any]:
        try:
            return state.get_proposal(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/api/proposals/{job_id}/apply")
    async def apply_proposal(job_id: str) -> dict[str, Any]:
        try:
            proposal = await runtime.apply_proposal(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return proposal

    @app.post("/api/requests")
    async def create_request(body: CreateRequestBody, background_tasks: BackgroundTasks) -> dict[str, Any]:
        try:
            state.get_app(body.app_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        request_payload = state.create_request(
            app_id=body.app_id,
            title=body.title,
            request_text=body.request_text,
            source=body.source,
        )
        job = state.create_job(
            app_id=body.app_id,
            request_id=request_payload["request_id"],
            title=body.title,
        )
        if body.execute_now and settings.auto_execute_requests:
            background_tasks.add_task(run_job, job["job_id"], body.app_id, request_payload)
        return {
            "request": request_payload,
            "job": job,
            "execute_now": bool(body.execute_now and settings.auto_execute_requests),
        }

    return app


app = create_app()
