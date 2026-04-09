#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / 'src'
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

try:
    from fastapi.testclient import TestClient
except ModuleNotFoundError:
    VENV_PYTHON = Path(__file__).resolve().parent.parent / '.venv' / 'bin' / 'python'
    if VENV_PYTHON.exists() and Path(sys.executable).resolve() != VENV_PYTHON.resolve():
        os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), __file__, *sys.argv[1:]])
    raise

from codex_factory_runtime import api_app
from codex_factory_runtime.auth import IAP_JWT_HEADER, TAILSCALE_LOGIN_HEADER, TAILSCALE_NAME_HEADER, IapIdentityProvider
from codex_factory_runtime.config import RuntimeSettings
from codex_factory_runtime.state import RuntimeState, utc_now


API_KEY = "contract-test-key"


class AssertionFailed(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionFailed(message)


async def fake_run_request(self, app_id: str, job_id: str, request_payload: dict[str, Any]) -> dict[str, Any]:
    record = self.state.get_app(app_id)
    clean_summary = f"SIMULATED_OK: {request_payload['title']}"
    decision_summary = {
        "goal": request_payload["request_text"],
        "system_area": "execution, verification",
        "decision": "Simulated the runtime contract without invoking the Codex CLI.",
        "why": "Contract tests should prove API and state behavior without depending on external model execution.",
        "tradeoff": "This verifies request plumbing and proposal state, not real Codex output quality.",
        "issue_encountered": "",
        "verification": "conversation, job, proposal, and apply endpoints exercised through TestClient",
        "follow_up": "Run the deployed smoke tests before production deployment.",
    }
    record["last_summary"] = clean_summary
    self.state.save_app(record)
    self.state.append_memory(app_id, f"Contract Run {utc_now()}", clean_summary)
    self.state.append_engineering_log(
        app_id=app_id,
        title=request_payload["title"],
        job_id=job_id,
        request_id=request_payload["request_id"],
        summary=decision_summary,
    )

    extra_fields: dict[str, Any] = {}
    if str(record.get("execution_mode") or "").strip() == "proposal":
        proposal = {
            "job_id": job_id,
            "app_id": app_id,
            "request_id": request_payload["request_id"],
            "status": "ready_to_apply",
            "title": request_payload["title"],
            "branch_name": f"codex/{app_id}-{job_id[:8]}",
            "base_branch": "main",
            "base_commit": "base1234",
            "head_commit": f"head-{job_id[:8]}",
            "worktree_path": str(self.settings.worktrees_root / job_id),
            "restart_service": str(record.get("restart_service") or ""),
            "allowed_paths": record.get("allowed_paths") or [],
            "result_summary": clean_summary,
            "decision_summary": decision_summary,
            "git_status": " M src/codex_factory_runtime/api_app.py",
            "git_show_stat": "deadbeef\n Simulated proposal commit",
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }
        self.state.save_proposal(proposal)
        extra_fields["proposal"] = {
            "job_id": proposal["job_id"],
            "branch_name": proposal["branch_name"],
            "head_commit": proposal["head_commit"],
            "status": proposal["status"],
        }

    return self.state.update_job(
        job_id,
        status="completed",
        completed_at=utc_now(),
        result_summary=clean_summary,
        error="",
        decision_summary=decision_summary,
        **extra_fields,
    )


async def fake_apply_proposal(self, job_id: str) -> dict[str, Any]:
    proposal = self.state.get_proposal(job_id)
    proposal["status"] = "applied"
    proposal["applied_at"] = utc_now()
    proposal["push_status"] = "pushed"
    proposal["push_remote"] = self.settings.push_remote
    proposal["push_branch"] = self.settings.push_branch
    proposal["push_message"] = "Simulated push to origin/main."
    proposal["pushed_at"] = utc_now()
    self.state.save_proposal(proposal)
    return proposal


def build_settings(temp_root: Path) -> RuntimeSettings:
    state_root = temp_root / "state"
    runtime_root = state_root / "runtime"
    return RuntimeSettings(
        repo_root=REPO_ROOT,
        state_root=state_root,
        registry_root=state_root / "registry" / "apps",
        requests_root=state_root / "requests",
        runtime_root=runtime_root,
        jobs_root=runtime_root / "jobs",
        proposals_root=runtime_root / "proposals",
        worktrees_root=runtime_root / "worktrees",
        conversations_root=runtime_root / "conversations",
        host="127.0.0.1",
        port=8787,
        codex_command="codex",
        codex_args=[],
        codex_home=None,
        codex_profile="",
        codex_model="",
        codex_sandbox="workspace-write",
        codex_skip_git_repo_check=True,
        cors_allowed_origins=[],
        auto_execute_requests=True,
        auth_providers=["api_key"],
        runtime_api_key=API_KEY,
        allowed_user_emails=[],
        iap_expected_audience="",
        push_after_apply=True,
        push_remote="origin",
        push_branch="main",
    )




def build_iap_settings(temp_root: Path) -> RuntimeSettings:
    settings = build_settings(temp_root)
    return RuntimeSettings(
        repo_root=settings.repo_root,
        state_root=settings.state_root,
        registry_root=settings.registry_root,
        requests_root=settings.requests_root,
        runtime_root=settings.runtime_root,
        jobs_root=settings.jobs_root,
        proposals_root=settings.proposals_root,
        worktrees_root=settings.worktrees_root,
        conversations_root=settings.conversations_root,
        host=settings.host,
        port=settings.port,
        codex_command=settings.codex_command,
        codex_args=settings.codex_args,
        codex_home=settings.codex_home,
        codex_profile=settings.codex_profile,
        codex_model=settings.codex_model,
        codex_sandbox=settings.codex_sandbox,
        codex_skip_git_repo_check=settings.codex_skip_git_repo_check,
        cors_allowed_origins=settings.cors_allowed_origins,
        auto_execute_requests=settings.auto_execute_requests,
        auth_providers=["iap"],
        runtime_api_key="",
        allowed_user_emails=["owner@example.com"],
        iap_expected_audience="/projects/123/global/backendServices/456",
        push_after_apply=settings.push_after_apply,
        push_remote=settings.push_remote,
        push_branch=settings.push_branch,
    )

def seed_apps(state: RuntimeState) -> None:
    state.save_app(
        {
            "app_id": "habit-tracker-pwa",
            "title": "Habit Tracker PWA",
            "workspace_path": "workspaces/habit-tracker-pwa",
            "deployment_url": "https://example.invalid/habit-tracker-pwa/",
            "session_id": "",
            "last_summary": "",
            "allowed_paths": ["workspaces/habit-tracker-pwa"],
        }
    )
    state.save_app(
        {
            "app_id": "factory-runtime",
            "title": "Codex App Factory Runtime",
            "workspace_path": ".",
            "deployment_url": "https://example.invalid/codex-ops-console/",
            "session_id": "",
            "last_summary": "",
            "execution_mode": "proposal",
            "restart_service": "codex-factory",
            "allowed_paths": ["src", "scripts", "examples/generated_apps/codex-ops-console"],
        }
    )


def request(client: TestClient, method: str, path: str, *, api_key: bool = True, **kwargs: Any):
    headers = kwargs.pop("headers", {})
    if api_key:
        headers = {**headers, "X-API-Key": API_KEY}
    return client.request(method, path, headers=headers, **kwargs)


def main() -> None:
    original_run_request = api_app.CodexAgentsRuntime.run_request
    original_apply_proposal = api_app.CodexAgentsRuntime.apply_proposal
    api_app.CodexAgentsRuntime.run_request = fake_run_request
    api_app.CodexAgentsRuntime.apply_proposal = fake_apply_proposal

    try:
        with tempfile.TemporaryDirectory(prefix="codex-contract-") as temp_dir:
            temp_root = Path(temp_dir)
            settings = build_settings(temp_root)
            state = RuntimeState(settings)
            seed_apps(state)
            client = TestClient(api_app.create_app(settings))

            health = client.get("/health")
            require(health.status_code == 200, f"health failed: {health.text}")

            unauthorized = client.get("/api/apps")
            require(unauthorized.status_code == 401, f"expected 401 without API key, got {unauthorized.status_code}")

            apps_response = request(client, "GET", "/api/apps")
            require(apps_response.status_code == 200, f"apps failed: {apps_response.text}")
            apps = apps_response.json()
            require(len(apps) == 2, f"expected 2 seeded apps, got {len(apps)}")

            conversation_response = request(
                client,
                "POST",
                "/api/conversations",
                json={"app_id": "habit-tracker-pwa", "source": "contract-test"},
            )
            require(conversation_response.status_code == 200, f"create conversation failed: {conversation_response.text}")
            conversation = conversation_response.json()
            conversation_id = conversation["conversation_id"]

            message_response = request(
                client,
                "POST",
                f"/api/conversations/{conversation_id}/messages",
                json={"message_text": "Reply with a simulated success message.", "source": "contract-test"},
            )
            require(message_response.status_code == 200, f"message failed: {message_response.text}")
            payload = message_response.json()
            job_id = payload["job"]["job_id"]
            require(payload["job"]["status"] == "queued", "job should be queued before background execution completes")

            job_response = request(client, "GET", f"/api/jobs/{job_id}")
            job = job_response.json()
            require(job["status"] == "completed", f"expected completed job, got {job['status']}")
            require(job["result_summary"].startswith("SIMULATED_OK:"), f"unexpected job summary: {job['result_summary']}")
            require(job["decision_summary"]["verification"], "decision summary should include verification evidence")

            conversation_after = request(client, "GET", f"/api/conversations/{conversation_id}").json()
            message_types = [message["role"] for message in conversation_after["messages"]]
            event_types = [event["type"] for event in conversation_after["events"]]
            require(message_types == ["user", "assistant"], f"unexpected conversation message roles: {message_types}")
            require(
                all(name in event_types for name in ["conversation.created", "message.accepted", "job.queued", "job.running", "job.completed"]),
                f"conversation events missing expected transitions: {event_types}",
            )

            proposal_conversation = request(
                client,
                "POST",
                "/api/conversations",
                json={"app_id": "factory-runtime", "source": "contract-test"},
            ).json()
            proposal_message = request(
                client,
                "POST",
                f"/api/conversations/{proposal_conversation['conversation_id']}/messages",
                json={"message_text": "Make a self-edit proposal.", "source": "contract-test"},
            )
            proposal_payload = proposal_message.json()
            proposal_job_id = proposal_payload["job"]["job_id"]
            proposal_job = request(client, "GET", f"/api/jobs/{proposal_job_id}").json()
            require(proposal_job["status"] == "completed", f"proposal job failed: {proposal_job}")
            require("proposal" in proposal_job, "proposal metadata should be attached for proposal-mode apps")

            proposal = request(client, "GET", f"/api/proposals/{proposal_job_id}").json()
            require(proposal["status"] == "ready_to_apply", f"proposal not ready: {proposal}")

            applied = request(client, "POST", f"/api/proposals/{proposal_job_id}/apply")
            require(applied.status_code == 200, f"apply failed: {applied.text}")
            applied_payload = applied.json()
            require(applied_payload["status"] == "applied", f"proposal should be applied: {applied_payload}")
            require(applied_payload["push_status"] == "pushed", f"proposal push should be recorded: {applied_payload}")

            proposal_conversation_after = request(client, "GET", f"/api/conversations/{proposal_conversation['conversation_id']}").json()
            proposal_event_types = [event["type"] for event in proposal_conversation_after["events"]]
            require("proposal.ready" in proposal_event_types, f"missing proposal.ready event: {proposal_event_types}")
            require("proposal.applied" in proposal_event_types, f"missing proposal.applied event: {proposal_event_types}")

            app_conversations = request(client, "GET", "/api/apps/factory-runtime/conversations").json()
            require(len(app_conversations) == 1, f"expected 1 factory conversation, got {len(app_conversations)}")

            engineering_log = (settings.state_root / "engineering-log.md").read_text(encoding="utf-8")
            require("Simulated the runtime contract without invoking the Codex CLI." in engineering_log, "engineering log missing expected entry")

            tailscale_settings = RuntimeSettings(
                repo_root=settings.repo_root,
                state_root=(temp_root / "tailscale" / "state"),
                registry_root=(temp_root / "tailscale" / "state" / "registry" / "apps"),
                requests_root=(temp_root / "tailscale" / "state" / "requests"),
                runtime_root=(temp_root / "tailscale" / "state" / "runtime"),
                jobs_root=(temp_root / "tailscale" / "state" / "runtime" / "jobs"),
                proposals_root=(temp_root / "tailscale" / "state" / "runtime" / "proposals"),
                worktrees_root=(temp_root / "tailscale" / "state" / "runtime" / "worktrees"),
                conversations_root=(temp_root / "tailscale" / "state" / "runtime" / "conversations"),
                host=settings.host,
                port=settings.port,
                codex_command=settings.codex_command,
                codex_args=settings.codex_args,
                codex_home=settings.codex_home,
                codex_profile=settings.codex_profile,
                codex_model=settings.codex_model,
                codex_sandbox=settings.codex_sandbox,
                codex_skip_git_repo_check=settings.codex_skip_git_repo_check,
                cors_allowed_origins=settings.cors_allowed_origins,
                auto_execute_requests=settings.auto_execute_requests,
                auth_providers=["tailscale"],
                runtime_api_key="",
                allowed_user_emails=["owner@example.com"],
                iap_expected_audience="",
                push_after_apply=settings.push_after_apply,
                push_remote=settings.push_remote,
                push_branch=settings.push_branch,
            )
            tailscale_state = RuntimeState(tailscale_settings)
            seed_apps(tailscale_state)
            tailscale_client = TestClient(api_app.create_app(tailscale_settings))
            tailscale_unauthorized = tailscale_client.get("/api/apps")
            require(tailscale_unauthorized.status_code == 401, f"expected 401 without tailscale headers, got {tailscale_unauthorized.status_code}")
            tailscale_authorized = tailscale_client.get("/api/apps", headers={TAILSCALE_LOGIN_HEADER: "owner@example.com", TAILSCALE_NAME_HEADER: "Owner"})
            require(tailscale_authorized.status_code == 200, f"tailscale auth failed: {tailscale_authorized.text}")

            iap_settings = build_iap_settings(temp_root / "iap")
            iap_state = RuntimeState(iap_settings)
            seed_apps(iap_state)
            original_verify = IapIdentityProvider.verify_iap_assertion
            IapIdentityProvider.verify_iap_assertion = lambda self, token: {
                "iss": "https://cloud.google.com/iap",
                "aud": self.expected_audience,
                "sub": "user-123",
                "email": "owner@example.com",
            }
            try:
                iap_client = TestClient(api_app.create_app(iap_settings))
                iap_unauthorized = iap_client.get("/api/apps")
                require(iap_unauthorized.status_code == 401, f"expected 401 without IAP assertion, got {iap_unauthorized.status_code}")
                iap_authorized = iap_client.get("/api/apps", headers={IAP_JWT_HEADER: "fake-token"})
                require(iap_authorized.status_code == 200, f"IAP auth failed: {iap_authorized.text}")
                iap_rejected = iap_client.get("/api/apps", headers={IAP_JWT_HEADER: "fake-token", "x-api-key": API_KEY})
                require(iap_rejected.status_code == 200, f"IAP auth with extra headers should still pass: {iap_rejected.text}")
            finally:
                IapIdentityProvider.verify_iap_assertion = original_verify

            print("runtime contract ok")
    finally:
        api_app.CodexAgentsRuntime.run_request = original_run_request
        api_app.CodexAgentsRuntime.apply_proposal = original_apply_proposal


if __name__ == "__main__":
    main()
