#!/usr/bin/env python3
from __future__ import annotations

import base64
import asyncio
import os
import sys
import tempfile
import time
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
from codex_factory_runtime.api_runtime_context import RuntimeApiContext
from codex_factory_runtime.auth import IAP_JWT_HEADER, TAILSCALE_LOGIN_HEADER, TAILSCALE_NAME_HEADER, IapIdentityProvider
from codex_factory_runtime.config import RuntimeSettings
from codex_factory_runtime.runtime_cli import CodexCliRunner
from codex_factory_runtime.runtime_autonomy import (
    AUTONOMY_PROPOSAL_END,
    AUTONOMY_PROPOSAL_START,
    AUTONOMY_REVIEW_END,
    AUTONOMY_REVIEW_START,
    AUTONOMY_VERIFY_END,
    AUTONOMY_VERIFY_START,
)
from codex_factory_runtime.runtime_engineering import build_prompt
from codex_factory_runtime.runtime_goals import GoalRuntime
from codex_factory_runtime.runtime_proposals import ProposalRuntime
from codex_factory_runtime.state import RuntimeState, utc_now


API_KEY = "contract-test-key"


class AssertionFailed(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionFailed(message)


async def fake_run_request(
    self,
    app_id: str,
    job_id: str,
    request_payload: dict[str, Any],
    *,
    event_callback=None,
) -> dict[str, Any]:
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
    if event_callback is not None:
        event_callback(
            event_type="runtime.context.loaded",
            body="Loaded app lane state for the simulated contract run.",
            status="planning",
            job_id=job_id,
            data={"execution_mode": record.get("execution_mode", "direct")},
        )
        event_callback(
            event_type="codex.exec.started",
            body="Started simulated Codex execution.",
            status="running",
            job_id=job_id,
            data={"simulated": True},
        )
    self.state.append_engineering_log(
        app_id=app_id,
        title=request_payload["title"],
        job_id=job_id,
        request_id=request_payload["request_id"],
        summary=decision_summary,
    )

    extra_fields: dict[str, Any] = {}
    goal_review = {}
    if request_payload.get("goal_loop"):
        goal_review = {
            "hypothesis": f"Iteration {request_payload['goal_loop']['iteration']} applies one bounded improvement step.",
            "verification_result": "Simulated verification passed.",
            "comparison_to_previous": "This simulated run represents incremental forward progress.",
            "continue_recommended": "yes" if request_payload["goal_loop"]["iteration"] < 2 else "no",
            "alignment_assessment": "yes",
            "safety_assessment": "yes",
            "next_focus": "Continue with the next bounded improvement step." if request_payload["goal_loop"]["iteration"] < 2 else "Stop after this iteration.",
        }
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
        if event_callback is not None:
            event_callback(
                event_type="proposal.saved",
                body="Saved a simulated proposal for review.",
                status="proposal",
                job_id=job_id,
                data={"branch_name": proposal["branch_name"], "status": proposal["status"]},
            )
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
        goal_review=goal_review,
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


async def fake_apply_proposal_failed_push(self, job_id: str) -> dict[str, Any]:
    proposal = self.state.get_proposal(job_id)
    proposal["status"] = "applied_local_push_failed"
    proposal["applied_at"] = utc_now()
    proposal["push_status"] = "failed"
    proposal["push_remote"] = self.settings.push_remote
    proposal["push_branch"] = self.settings.push_branch
    proposal["push_message"] = "Simulated push failure."
    proposal["pushed_at"] = ""
    self.state.save_proposal(proposal)
    return proposal


async def fake_run_advisory_prompt(
    self,
    *,
    prompt: str,
    cwd: Path,
    output_stem: str,
    sandbox: str = "read-only",
) -> tuple[int, str, str, str]:
    require(sandbox == "read-only", f"advisory prompts must use read-only sandbox, got {sandbox}")
    if not hasattr(fake_run_advisory_prompt, "_attempts"):
        fake_run_advisory_prompt._attempts = {}
    attempts = fake_run_advisory_prompt._attempts
    if AUTONOMY_PROPOSAL_START in prompt:
        return (
            0,
            '{"type":"thread.started","thread_id":"advisory-proposal"}\n',
            "",
            "\n".join(
                [
                    "Propose a bounded UI improvement.",
                    AUTONOMY_PROPOSAL_START,
                    '{"hypothesis":"Improve conversation visibility first.","target_area":"conversation list","change_outline":"Make the active thread easier to find and keep the message composer secondary.","success_criteria":"The active conversation is easier to identify and continue.","why_now":"The operator experience depends on regaining context quickly."}',
                    AUTONOMY_PROPOSAL_END,
                ]
            ),
        )
    if AUTONOMY_REVIEW_START in prompt:
        if "Reviewer A" in prompt:
            key = "reviewer-a"
            attempts[key] = attempts.get(key, 0) + 1
            if attempts[key] == 1:
                return (
                    1,
                    "",
                    "Reading additional input from stdin...",
                    "",
                )
        return (
            0,
            '{"type":"thread.started","thread_id":"advisory-review"}\n',
            "",
            "\n".join(
                [
                    "The bounded proposal looks safe.",
                    AUTONOMY_REVIEW_START,
                    '{"verdict":"approve","rationale":"The change is small and aligned with the goal.","blocking_issue":"","suggested_adjustment":"Keep the scope focused on context recovery."}',
                    AUTONOMY_REVIEW_END,
                ]
            ),
        )
    if AUTONOMY_VERIFY_START in prompt:
        return (
            0,
            '{"type":"thread.started","thread_id":"advisory-verify"}\n',
            "",
            "\n".join(
                [
                    "The implementation satisfies the approved hypothesis.",
                    AUTONOMY_VERIFY_START,
                    '{"verdict":"pass","evidence":"The implementation summary matches the approved bounded change.","residual_risk":"Low","follow_up":"Continue with the next bounded improvement if the goal review recommends it."}',
                    AUTONOMY_VERIFY_END,
                ]
            ),
        )
    raise AssertionFailed(f"Unexpected advisory prompt: {prompt[:120]}")


def build_settings(temp_root: Path) -> RuntimeSettings:
    state_root = temp_root / "state"
    runtime_root = state_root / "runtime"
    return RuntimeSettings(
        repo_root=REPO_ROOT,
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
        host="127.0.0.1",
        port=8787,
        codex_command="codex",
        codex_args=[],
        codex_home=None,
        codex_profile="",
        codex_model="",
        codex_sandbox="workspace-write",
        advisory_timeout_seconds=90,
        codex_skip_git_repo_check=True,
        cors_allowed_origins=[],
        auto_execute_requests=True,
        auth_providers=["api_key"],
        runtime_api_key=API_KEY,
        allowed_user_emails=[],
        iap_expected_audience="",
        operator_base_url="https://codex-factory-vm.tail1b6dd1.ts.net",
        github_pages_base_url="https://cfalws.github.io/codex-app-factory",
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
        attachments_root=settings.attachments_root,
        jobs_root=settings.jobs_root,
        proposals_root=settings.proposals_root,
        worktrees_root=settings.worktrees_root,
        conversations_root=settings.conversations_root,
        goals_root=settings.goals_root,
        host=settings.host,
        port=settings.port,
        codex_command=settings.codex_command,
        codex_args=settings.codex_args,
        codex_home=settings.codex_home,
        codex_profile=settings.codex_profile,
        codex_model=settings.codex_model,
        codex_sandbox=settings.codex_sandbox,
        advisory_timeout_seconds=settings.advisory_timeout_seconds,
        codex_skip_git_repo_check=settings.codex_skip_git_repo_check,
        cors_allowed_origins=settings.cors_allowed_origins,
        auto_execute_requests=settings.auto_execute_requests,
        auth_providers=["iap"],
        runtime_api_key="",
        allowed_user_emails=["owner@example.com"],
        iap_expected_audience="/projects/123/global/backendServices/456",
        operator_base_url=settings.operator_base_url,
        github_pages_base_url=settings.github_pages_base_url,
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


def verify_prompt_contract(settings: RuntimeSettings, state: RuntimeState) -> None:
    app_record = state.get_app("habit-tracker-pwa")
    prompt = build_prompt(
        settings,
        app_record,
        {
            "title": "Prompt contract smoke",
            "request_text": "Reply with exactly one line and do not modify files.",
            "source": "verify-runtime-contract",
            "conversation_id": "contract-conversation",
            "intent_summary": {
                "explicit_request": "Reply with exactly one line and do not modify files.",
                "interpreted_outcome": "Return a bounded no-op response.",
                "assumptions": "No file edits required.",
                "ambiguity": "Low",
                "success_signal": "A non-empty prompt is produced for codex exec.",
            },
        },
    )
    require(isinstance(prompt, str), "build_prompt must return a string")
    require(bool(prompt.strip()), "build_prompt must return a non-empty prompt")
    require("Request:" in prompt, "build_prompt must include the request body")
    ui_prompt = build_prompt(
        settings,
        state.get_app("factory-runtime"),
        {
            "title": "UI discomfort fix",
            "request_text": "The conversation list is confusing on mobile. Simplify it.",
            "source": "verify-runtime-contract",
            "conversation_id": "contract-conversation",
            "ux_context": {
                "affected_surface": "conversation list",
                "pain_points": ["길 찾기 어려움", "모바일에서 누르기 불편"],
                "note": "The list feels noisy and I cannot tell where to tap first.",
                "desired_feel": "more obvious and calmer",
            },
            "intent_summary": {
                "explicit_request": "Simplify the conversation list.",
                "interpreted_outcome": "Reduce friction in the conversation list on mobile.",
                "assumptions": "Keep the current lane and reduce clutter first.",
                "ambiguity": "Medium",
                "success_signal": "The mobile list should feel more obvious.",
            },
        },
    )
    require("UX_REVIEW_JSON_START" in ui_prompt, "UI-oriented prompt must require a UX review block")
    require("User-reported UX friction:" in ui_prompt, "UI-oriented prompt must include structured UX context")
    screenshot_prompt = build_prompt(
        settings,
        state.get_app("factory-runtime"),
        {
            "title": "Screenshot-backed UX review",
            "request_text": "Use the screenshot evidence to simplify the operator console.",
            "source": "verify-runtime-contract",
            "conversation_id": "contract-conversation",
            "attachments": [
                {
                    "attachment_id": "shot1",
                    "filename": "operator-console.png",
                    "content_type": "image/png",
                    "size_bytes": 1024,
                    "api_path": "/api/conversations/contract-conversation/attachments/shot1",
                }
            ],
            "intent_summary": {
                "explicit_request": "Use the screenshot evidence to simplify the operator console.",
                "interpreted_outcome": "Reduce visible friction in the operator console based on the screenshot.",
                "assumptions": "Treat the screenshot as the current UI truth.",
                "ambiguity": "Medium",
                "success_signal": "The UI should better match the visible friction in the screenshot.",
            },
        },
    )
    require("Attached screenshots:" in screenshot_prompt, "screenshot-backed prompt must include attached screenshot evidence")


def request(client: TestClient, method: str, path: str, *, api_key: bool = True, **kwargs: Any):
    headers = kwargs.pop("headers", {})
    if api_key:
        headers = {**headers, "X-API-Key": API_KEY}
    return client.request(method, path, headers=headers, **kwargs)


def wait_for_goal_status(client: TestClient, goal_id: str, expected_status: str, *, attempts: int = 40, delay: float = 0.05) -> dict[str, Any]:
    last_goal: dict[str, Any] | None = None
    for _ in range(attempts):
        last_goal = request(client, "GET", f"/api/goals/{goal_id}").json()
        if last_goal.get("status") == expected_status:
            return last_goal
        time.sleep(delay)
    raise AssertionFailed(f"goal {goal_id} did not reach {expected_status}: {last_goal}")


def verify_goal_task_lifecycle(settings: RuntimeSettings, state: RuntimeState) -> None:
    async def _run() -> None:
        original_run_goal_loop = RuntimeApiContext.run_goal_loop
        context = RuntimeApiContext(
            settings=settings,
            state=state,
            runtime=api_app.CodexAgentsRuntime(settings, state),
            goals=GoalRuntime(),
            autonomy=api_app.AutonomyRuntime(),
        )

        started = asyncio.Event()
        release = asyncio.Event()

        async def fake_goal_loop(self, goal_id: str) -> None:
            started.set()
            await release.wait()

        RuntimeApiContext.run_goal_loop = fake_goal_loop
        try:
            context.spawn_goal_loop("goal-task-contract")
            await asyncio.wait_for(started.wait(), timeout=1.0)
            require(
                "goal-task-contract" in context.goal_tasks,
                f"spawned goal task should be retained until completion: {context.goal_tasks.keys()}",
            )
            first_task = context.goal_tasks["goal-task-contract"]
            context.spawn_goal_loop("goal-task-contract")
            require(
                context.goal_tasks["goal-task-contract"] is first_task,
                "spawn_goal_loop should not replace an already running task for the same goal",
            )
            release.set()
            await asyncio.wait_for(first_task, timeout=1.0)
            await asyncio.sleep(0)
            require(
                "goal-task-contract" not in context.goal_tasks,
                "completed goal task should be removed from the retained task table",
            )
        finally:
            RuntimeApiContext.run_goal_loop = original_run_goal_loop

    asyncio.run(_run())


def verify_retryable_advisory_phase(settings: RuntimeSettings, state: RuntimeState) -> None:
    async def _run() -> None:
        context = RuntimeApiContext(
            settings=settings,
            state=state,
            runtime=api_app.CodexAgentsRuntime(settings, state),
            goals=GoalRuntime(),
            autonomy=api_app.AutonomyRuntime(),
        )
        goal = {
            "goal_id": "retry-goal",
            "objective": "Verify retry handling.",
        }
        app = {"title": "Retry App", "app_id": "retry-app"}
        proposal = {
            "hypothesis": "Retry transient advisory failures.",
            "target_area": "review phase",
            "change_outline": "Retry once on stdin error.",
            "success_criteria": "Second attempt succeeds.",
            "why_now": "Prevent false pauses on transient errors.",
        }
        conversation = context.state.create_conversation(app_id="habit-tracker-pwa", title="Retry Contract", source="contract-test")
        review = await context.run_autonomy_review(
            goal=goal,
            app_record=app,
            proposal=proposal,
            conversation_id=conversation["conversation_id"],
            iteration_number=1,
            reviewer_name="Reviewer A",
        )
        require(review["verdict"] == "approve", f"retryable review phase should recover and approve: {review}")
        conversation_after = context.state.get_conversation(conversation["conversation_id"])
        event_types = [event["type"] for event in conversation_after["events"]]
        require("goal.review.phase.retrying" in event_types, f"retryable advisory failure should emit retry event: {event_types}")

    asyncio.run(_run())


def main() -> None:
    original_run_request = api_app.CodexAgentsRuntime.run_request
    original_apply_proposal = api_app.CodexAgentsRuntime.apply_proposal
    original_run_advisory_prompt = api_app.CodexAgentsRuntime.run_advisory_prompt
    api_app.CodexAgentsRuntime.run_request = fake_run_request
    api_app.CodexAgentsRuntime.apply_proposal = fake_apply_proposal
    api_app.CodexAgentsRuntime.run_advisory_prompt = fake_run_advisory_prompt
    if hasattr(fake_run_advisory_prompt, "_attempts"):
        fake_run_advisory_prompt._attempts = {}

    try:
        with tempfile.TemporaryDirectory(prefix="codex-contract-") as temp_dir:
            temp_root = Path(temp_dir)
            settings = build_settings(temp_root)
            state = RuntimeState(settings)
            seed_apps(state)
            verify_prompt_contract(settings, state)
            verify_goal_task_lifecycle(settings, state)
            verify_retryable_advisory_phase(settings, state)
            client = TestClient(api_app.create_app(settings))

            runner = CodexCliRunner(settings)
            resume_command = runner.build_command(
                "019d6fed-7653-7dd1-aa05-774a52a635d9",
                "Reply with exactly CONTRACT_RESUME_OK.",
                temp_root / "resume-last-message.txt",
                use_resume=True,
                image_paths=["/tmp/contract-image.png"],
            )
            require("--sandbox" not in resume_command, f"resume command must not include --sandbox: {resume_command}")
            require("resume" in resume_command, f"resume command should include resume subcommand: {resume_command}")
            require("--image" in resume_command, f"resume command should include --image for screenshot review: {resume_command}")
            fresh_command = runner.build_command(
                "",
                "Reply with exactly CONTRACT_FRESH_OK.",
                temp_root / "fresh-last-message.txt",
                use_resume=False,
                image_paths=["/tmp/contract-image.png"],
            )
            require("--image" in fresh_command, f"fresh exec command should include --image for screenshot review: {fresh_command}")

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

            png_bytes = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Z3ioAAAAASUVORK5CYII="
            )
            upload_response = request(
                client,
                "POST",
                f"/api/conversations/{conversation_id}/attachments",
                files={"files": ("contract-shot.png", png_bytes, "image/png")},
            )
            require(upload_response.status_code == 200, f"attachment upload failed: {upload_response.text}")
            uploaded_attachments = upload_response.json()["attachments"]
            require(len(uploaded_attachments) == 1, f"expected 1 uploaded attachment, got {uploaded_attachments}")
            require(uploaded_attachments[0]["api_path"], "uploaded attachment should expose an api_path")

            message_response = request(
                client,
                "POST",
                f"/api/conversations/{conversation_id}/messages",
                json={
                    "message_text": "The mobile conversation list feels confusing. Simplify it and explain the change.",
                    "source": "contract-test",
                    "ux_context": {
                        "affected_surface": "conversation list",
                        "pain_points": ["길 찾기 어려움", "모바일에서 누르기 불편"],
                        "note": "It feels noisy and I cannot tell where to tap first.",
                        "desired_feel": "calmer and more obvious",
                    },
                    "attachments": uploaded_attachments,
                },
            )
            require(message_response.status_code == 200, f"message failed: {message_response.text}")
            payload = message_response.json()
            job_id = payload["job"]["job_id"]
            require(payload["job"]["status"] == "queued", "job should be queued before background execution completes")
            require(payload["request"]["intent_summary"]["explicit_request"], "request should include interpreted intent")
            require(payload["job"]["intent_summary"]["interpreted_outcome"], "job should include interpreted outcome")
            require(payload["request"]["ux_context"]["affected_surface"] == "conversation list", "request should persist ux_context")
            require(payload["request"]["attachments"], "request should persist uploaded attachment refs")
            require(payload["job"]["attachments"], "job should persist uploaded attachment refs")
            require(
                payload["conversation"]["messages"][0]["metadata"]["ux_context"]["desired_feel"] == "calmer and more obvious",
                "conversation request message should persist ux_context",
            )
            require(
                payload["conversation"]["messages"][0]["metadata"]["attachments"][0]["filename"] == "contract-shot.png",
                "conversation request message should persist uploaded screenshot refs",
            )

            job_response = request(client, "GET", f"/api/jobs/{job_id}")
            job = job_response.json()
            require(job["status"] == "completed", f"expected completed job, got {job['status']}")
            require(job["result_summary"].startswith("SIMULATED_OK:"), f"unexpected job summary: {job['result_summary']}")
            require(job["decision_summary"]["verification"], "decision summary should include verification evidence")
            require(job["ux_context"]["affected_surface"] == "conversation list", "job should persist ux_context")
            require(job["intent_summary"]["success_signal"], "job intent summary should include success signal")

            conversation_after = request(client, "GET", f"/api/conversations/{conversation_id}").json()
            message_types = [message["role"] for message in conversation_after["messages"]]
            event_types = [event["type"] for event in conversation_after["events"]]
            require(message_types == ["user", "assistant"], f"unexpected conversation message roles: {message_types}")
            require(
                conversation_after["messages"][0]["metadata"]["intent_summary"]["explicit_request"],
                "user conversation message should preserve interpreted intent",
            )
            require(
                all(
                    name in event_types
                    for name in [
                        "conversation.created",
                        "message.accepted",
                        "intent.interpreted",
                        "job.queued",
                        "job.running",
                        "job.completed",
                    ]
                ),
                f"conversation events missing expected transitions: {event_types}",
            )
            require("codex.exec.retrying" not in event_types, f"unexpected degraded retry event in contract flow: {event_types}")
            require("runtime.exception" not in event_types, f"unexpected runtime exception event in contract flow: {event_types}")

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

            goal_response = request(
                client,
                "POST",
                "/api/goals",
                json={
                    "app_id": "habit-tracker-pwa",
                    "objective": "Keep improving the phone operator experience until the goal review says to stop.",
                    "source": "contract-test",
                    "max_iterations": 0,
                    "autostart": True,
                },
            )
            require(goal_response.status_code == 200, f"goal creation failed: {goal_response.text}")
            goal_payload = goal_response.json()
            goal = wait_for_goal_status(client, goal_payload["goal"]["goal_id"], "completed")
            require(goal["status"] == "completed", f"goal should stop through goal review: {goal}")
            require(goal["stop_reason"] == "goal_review_stop", f"goal should stop through goal review signal: {goal}")
            require(len(goal["iterations"]) == 2, f"expected 2 goal iterations, got {len(goal['iterations'])}")
            require(goal["iterations"][0]["proposal_reviews"][0]["verdict"] == "approve", "goal iteration should record reviewer approval")
            require(goal["iterations"][0]["goal_review"]["continue_recommended"] == "yes", "first goal iteration should continue")
            require(goal["iterations"][1]["goal_review"]["continue_recommended"] == "no", "second goal iteration should stop")

            proposal_goal_response = request(
                client,
                "POST",
                "/api/goals",
                json={
                    "app_id": "factory-runtime",
                    "objective": "Keep improving the runtime through proposal-mode iterations until the goal review says to stop.",
                    "source": "contract-test",
                    "max_iterations": 0,
                    "autostart": True,
                    "auto_apply_proposals": True,
                    "auto_resume_after_apply": False,
                },
            )
            require(proposal_goal_response.status_code == 200, f"proposal goal creation failed: {proposal_goal_response.text}")
            proposal_goal = wait_for_goal_status(client, proposal_goal_response.json()["goal"]["goal_id"], "completed")
            require(proposal_goal["status"] == "completed", f"proposal goal should complete through auto-applied iterations: {proposal_goal}")
            require(proposal_goal["stop_reason"] == "goal_review_stop", f"proposal goal should stop through goal review signal: {proposal_goal}")
            require(len(proposal_goal["iterations"]) == 2, f"expected 2 proposal goal iterations, got {len(proposal_goal['iterations'])}")
            require(proposal_goal["iterations"][0]["auto_applied"] is True, "first proposal goal iteration should be auto-applied")
            require(proposal_goal["iterations"][0]["proposal_status"] == "applied", "proposal goal iteration should record applied proposal status")
            require(proposal_goal["iterations"][0]["verification_reviews"][0]["verdict"] == "pass", "proposal goal iteration should record verifier pass")

            api_app.CodexAgentsRuntime.apply_proposal = fake_apply_proposal_failed_push
            try:
                degraded_goal_response = request(
                    client,
                    "POST",
                    "/api/goals",
                    json={
                        "app_id": "factory-runtime",
                        "objective": "Pause if proposal auto-apply ends in a degraded apply outcome.",
                        "source": "contract-test",
                        "max_iterations": 0,
                        "autostart": True,
                        "auto_apply_proposals": True,
                        "auto_resume_after_apply": True,
                    },
                )
                require(degraded_goal_response.status_code == 200, f"degraded proposal goal creation failed: {degraded_goal_response.text}")
                degraded_goal = request(client, "GET", f"/api/goals/{degraded_goal_response.json()['goal']['goal_id']}").json()
                require(degraded_goal["status"] == "paused", f"degraded auto-apply should pause the goal: {degraded_goal}")
                require(
                    degraded_goal["stop_reason"] == "auto_apply_push_failed",
                    f"degraded auto-apply should record an explicit stop reason: {degraded_goal}",
                )
                require(
                    degraded_goal["iterations"][0]["push_status"] == "failed",
                    f"degraded auto-apply should persist failed push status into the iteration: {degraded_goal}",
                )
                require(
                    degraded_goal["iterations"][0]["degraded_apply_reason"] == "auto_apply_push_failed",
                    f"degraded auto-apply should persist the degraded apply reason: {degraded_goal}",
                )
                degraded_conversation = request(
                    client, "GET", f"/api/conversations/{degraded_goal_response.json()['conversation']['conversation_id']}"
                ).json()
                degraded_event_types = [event["type"] for event in degraded_conversation["events"]]
                require(
                    "goal.proposal.auto_apply.degraded" in degraded_event_types,
                    f"degraded auto-apply should emit explicit degraded event: {degraded_event_types}",
                )
                require(
                    "goal.awaiting_restart_resume" not in degraded_event_types,
                    f"degraded auto-apply should not proceed into restart-resume continuation: {degraded_event_types}",
                )
            finally:
                api_app.CodexAgentsRuntime.apply_proposal = fake_apply_proposal

            restart_resume_response = request(
                client,
                "POST",
                "/api/goals",
                json={
                    "app_id": "factory-runtime",
                    "objective": "Keep improving through unattended proposal iterations, auto-apply them, and continue after restart.",
                    "source": "contract-test",
                    "max_iterations": 0,
                    "autostart": True,
                    "auto_apply_proposals": True,
                    "auto_resume_after_apply": True,
                },
            )
            require(restart_resume_response.status_code == 200, f"restart-resume goal creation failed: {restart_resume_response.text}")
            restart_resume_goal_id = restart_resume_response.json()["goal"]["goal_id"]
            restart_resume_goal = request(client, "GET", f"/api/goals/{restart_resume_goal_id}").json()
            require(restart_resume_goal["status"] == "running", f"restart-resume goal should stay running until startup recovery: {restart_resume_goal}")
            require(
                restart_resume_goal["awaiting_restart_resume"] is True,
                f"restart-resume goal should record pending restart recovery: {restart_resume_goal}",
            )
            require(
                restart_resume_goal["awaiting_restart_iteration"] == 1,
                f"restart-resume goal should record pending iteration: {restart_resume_goal}",
            )
            restart_conversation_before = request(
                client, "GET", f"/api/conversations/{restart_resume_response.json()['conversation']['conversation_id']}"
            ).json()
            restart_event_types_before = [event["type"] for event in restart_conversation_before["events"]]
            require(
                "goal.awaiting_restart_resume" in restart_event_types_before,
                f"restart-resume goal should emit awaiting restart event before startup recovery: {restart_event_types_before}",
            )

            with TestClient(api_app.create_app(settings)) as restart_client:
                restart_resume_goal = wait_for_goal_status(restart_client, restart_resume_goal_id, "completed")
                require(
                    restart_resume_goal["stop_reason"] == "goal_review_stop",
                    f"restart-resume goal should complete after startup recovery: {restart_resume_goal}",
                )
                require(
                    restart_resume_goal["awaiting_restart_resume"] is False,
                    f"restart-resume goal should clear pending restart marker after startup recovery: {restart_resume_goal}",
                )
                require(
                    restart_resume_goal["last_resume_reason"] == "restart_resume",
                    f"restart-resume goal should record why it was resumed: {restart_resume_goal}",
                )
                require(restart_resume_goal["last_resumed_at"], f"restart-resume goal should record when it was resumed: {restart_resume_goal}")
                require(
                    len(restart_resume_goal["iterations"]) == 2,
                    f"restart-resume goal should continue with the next bounded iteration after startup recovery: {restart_resume_goal}",
                )
                restart_conversation_after = request(
                    restart_client, "GET", f"/api/conversations/{restart_resume_response.json()['conversation']['conversation_id']}"
                ).json()
                restart_resume_events = [event for event in restart_conversation_after["events"] if event["type"] == "goal.resumed"]
                require(
                    restart_resume_events,
                    f"restart-resume goal should emit a goal.resumed event after startup recovery: {restart_conversation_after['events']}",
                )
                require(
                    restart_resume_events[-1]["data"].get("resume_reason") == "restart_resume",
                    f"restart-resume goal should label the resume path explicitly: {restart_resume_events[-1]}",
                )

            proposal_runtime = ProposalRuntime(settings, state, CodexCliRunner(settings))
            blocking = proposal_runtime.blocking_repo_changes(
                " M src/codex_factory_runtime/api_app.py\n"
                "?? state/runtime/jobs/example.json\n"
                "?? state/runtime/goals/example.json\n"
                "?? state/runtime/smoke/habit-tracker-pwa/phone-ops-check.md\n"
                "?? examples/generated_apps/habit-tracker-pwa/runtime-api-verification/phone-ops-check.md\n"
            )
            require(
                blocking == ["src/codex_factory_runtime/api_app.py"],
                f"proposal apply should ignore runtime-owned artifacts and only block real source edits: {blocking}",
            )

            engineering_log = (settings.state_root / "engineering-log.md").read_text(encoding="utf-8")
            require("Simulated the runtime contract without invoking the Codex CLI." in engineering_log, "engineering log missing expected entry")

            tailscale_settings = RuntimeSettings(
                repo_root=settings.repo_root,
                state_root=(temp_root / "tailscale" / "state"),
                registry_root=(temp_root / "tailscale" / "state" / "registry" / "apps"),
                requests_root=(temp_root / "tailscale" / "state" / "requests"),
                runtime_root=(temp_root / "tailscale" / "state" / "runtime"),
                attachments_root=(temp_root / "tailscale" / "state" / "runtime" / "attachments"),
                jobs_root=(temp_root / "tailscale" / "state" / "runtime" / "jobs"),
                proposals_root=(temp_root / "tailscale" / "state" / "runtime" / "proposals"),
                worktrees_root=(temp_root / "tailscale" / "state" / "runtime" / "worktrees"),
                conversations_root=(temp_root / "tailscale" / "state" / "runtime" / "conversations"),
                goals_root=(temp_root / "tailscale" / "state" / "runtime" / "goals"),
                host=settings.host,
                port=settings.port,
                codex_command=settings.codex_command,
                codex_args=settings.codex_args,
                codex_home=settings.codex_home,
                codex_profile=settings.codex_profile,
                codex_model=settings.codex_model,
                codex_sandbox=settings.codex_sandbox,
                advisory_timeout_seconds=settings.advisory_timeout_seconds,
                codex_skip_git_repo_check=settings.codex_skip_git_repo_check,
                cors_allowed_origins=settings.cors_allowed_origins,
                auto_execute_requests=settings.auto_execute_requests,
                auth_providers=["tailscale"],
                runtime_api_key="",
                allowed_user_emails=["owner@example.com"],
                iap_expected_audience="",
                operator_base_url=settings.operator_base_url,
                github_pages_base_url=settings.github_pages_base_url,
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
        api_app.CodexAgentsRuntime.run_advisory_prompt = original_run_advisory_prompt


if __name__ == "__main__":
    main()
