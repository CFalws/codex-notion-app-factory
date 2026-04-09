from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name: str) -> list[str]:
    raw = os.getenv(name, "").strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return [item.strip() for item in raw.split(",") if item.strip()]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    raise ValueError(f"{name} must be a JSON array or comma-separated list.")


def _env_path(name: str) -> Path | None:
    raw = os.getenv(name, "").strip()
    if not raw:
        return None
    return Path(raw).expanduser().resolve()


@dataclass(frozen=True)
class RuntimeSettings:
    repo_root: Path
    state_root: Path
    registry_root: Path
    requests_root: Path
    runtime_root: Path
    attachments_root: Path
    jobs_root: Path
    proposals_root: Path
    worktrees_root: Path
    conversations_root: Path
    goals_root: Path
    host: str
    port: int
    codex_command: str
    codex_args: list[str]
    codex_home: Path | None
    codex_profile: str
    codex_model: str
    codex_sandbox: str
    codex_skip_git_repo_check: bool
    cors_allowed_origins: list[str]
    auto_execute_requests: bool
    auth_providers: list[str]
    runtime_api_key: str
    allowed_user_emails: list[str]
    iap_expected_audience: str
    operator_base_url: str
    github_pages_base_url: str
    push_after_apply: bool
    push_remote: str
    push_branch: str


def load_settings() -> RuntimeSettings:
    repo_root = Path(os.getenv("CODEX_FACTORY_REPO_ROOT", Path(__file__).resolve().parents[2])).resolve()
    state_root = Path(os.getenv("CODEX_FACTORY_STATE_ROOT", repo_root / "state")).expanduser().resolve()
    runtime_root = state_root / "runtime"
    codex_home = _env_path("CODEX_HOME")
    runtime_api_key = os.getenv("CODEX_FACTORY_API_KEY", "").strip()
    auth_providers = _env_list("CODEX_FACTORY_AUTH_PROVIDERS")
    if not auth_providers and runtime_api_key:
        auth_providers = ["api_key"]
    return RuntimeSettings(
        repo_root=repo_root,
        state_root=state_root,
        registry_root=state_root / "registry" / "apps",
        requests_root=state_root / "requests",
        runtime_root=runtime_root,
        attachments_root=runtime_root / "attachments",
        jobs_root=runtime_root / "jobs",
        proposals_root=runtime_root / "proposals",
        worktrees_root=runtime_root / "worktrees",
        conversations_root=runtime_root / "conversations",
        goals_root=runtime_root / "goals",
        host=os.getenv("CODEX_FACTORY_HOST", "0.0.0.0"),
        port=int(os.getenv("CODEX_FACTORY_PORT", "8787")),
        codex_command=os.getenv("CODEX_COMMAND", "codex").strip(),
        codex_args=_env_list("CODEX_ARGS_JSON"),
        codex_home=codex_home,
        codex_profile=os.getenv("CODEX_PROFILE", "").strip(),
        codex_model=os.getenv("CODEX_MODEL", "").strip(),
        codex_sandbox=os.getenv("CODEX_SANDBOX", "workspace-write").strip(),
        codex_skip_git_repo_check=_env_bool("CODEX_SKIP_GIT_REPO_CHECK", True),
        cors_allowed_origins=_env_list("CODEX_FACTORY_CORS_ALLOWED_ORIGINS"),
        auto_execute_requests=_env_bool("CODEX_FACTORY_AUTO_EXECUTE", True),
        auth_providers=auth_providers,
        runtime_api_key=runtime_api_key,
        allowed_user_emails=_env_list("CODEX_FACTORY_ALLOWED_USER_EMAILS"),
        iap_expected_audience=os.getenv("CODEX_FACTORY_IAP_AUDIENCE", "").strip(),
        operator_base_url=os.getenv("CODEX_FACTORY_OPERATOR_BASE_URL", "https://codex-factory-vm.tail1b6dd1.ts.net").strip(),
        github_pages_base_url=os.getenv("CODEX_FACTORY_GITHUB_PAGES_BASE_URL", "https://cfalws.github.io/codex-app-factory").strip(),
        push_after_apply=_env_bool("CODEX_FACTORY_PUSH_AFTER_APPLY", True),
        push_remote=os.getenv("CODEX_FACTORY_PUSH_REMOTE", "origin").strip() or "origin",
        push_branch=os.getenv("CODEX_FACTORY_PUSH_BRANCH", "main").strip() or "main",
    )
