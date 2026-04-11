#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

try:
    from fastapi.testclient import TestClient
except ModuleNotFoundError:
    venv_python = REPO_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists() and Path(sys.executable).resolve() != venv_python.resolve():
        os.execv(str(venv_python), [str(venv_python), __file__, *sys.argv[1:]])
    raise

from codex_factory_runtime import api_app
from codex_factory_runtime.api_runtime_context import RuntimeApiContext
from codex_factory_runtime.auth import IAP_JWT_HEADER, IapIdentityProvider, TAILSCALE_LOGIN_HEADER, TAILSCALE_NAME_HEADER
from codex_factory_runtime.config import RuntimeSettings
from codex_factory_runtime.runtime_autonomy import (
    AUTONOMY_PROPOSAL_END,
    AUTONOMY_PROPOSAL_START,
    AUTONOMY_REVIEW_END,
    AUTONOMY_REVIEW_START,
    AUTONOMY_VERIFY_END,
    AUTONOMY_VERIFY_START,
)
from codex_factory_runtime.runtime_cli import CodexCliRunner
from codex_factory_runtime.runtime_goals import GoalRuntime
from codex_factory_runtime.runtime_proposals import ProposalRuntime
from codex_factory_runtime.runtime_engineering import build_prompt
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
    simulate_retry_fallback = "SIMULATE_DEGRADED_RETRY" in str(request_payload.get("request_text") or "")
    decision_summary = {
        "goal": request_payload["request_text"],
        "system_area": "execution, verification",
        "decision": "Simulated the runtime contract without invoking the Codex CLI.",
        "why": "Contract tests should prove API and state behavior without depending on external model execution.",
        "tradeoff": "This verifies state transitions and orchestration, not model quality.",
        "issue_encountered": "",
        "verification": "conversation, job, proposal, and goal flows exercised through TestClient",
        "follow_up": "Run deployed smoke tests before production deployment.",
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
        if simulate_retry_fallback:
            event_callback(
                event_type="codex.exec.retrying",
                body="Simulated fallback to a fresh session after resume failure.",
                status="running",
                job_id=job_id,
                data={"previous_session_id": "contract-session"},
            )
    self.state.append_engineering_log(
        app_id=app_id,
        title=request_payload["title"],
        job_id=job_id,
        request_id=request_payload["request_id"],
        summary=decision_summary,
    )

    goal_review = {}
    extra_fields: dict[str, Any] = {}
    if request_payload.get("goal_loop"):
        iteration = int(request_payload["goal_loop"]["iteration"])
        goal_review = {
            "hypothesis": f"Iteration {iteration} applies one bounded improvement step.",
            "verification_result": "Simulated verification passed.",
            "comparison_to_previous": "This simulated run represents incremental forward progress.",
            "continue_recommended": "yes" if iteration < 2 else "no",
            "alignment_assessment": "yes",
            "safety_assessment": "yes",
            "next_focus": "Continue with the next bounded improvement step." if iteration < 2 else "Stop after this iteration.",
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
                    "Propose a bounded runtime improvement.",
                    AUTONOMY_PROPOSAL_START,
                    '{"hypothesis":"Improve conversation visibility first.","target_area":"conversation list","change_outline":"Make the active thread easier to find and keep the message composer secondary.","success_criteria":"The active conversation is easier to identify and continue.","why_now":"The operator experience depends on regaining context quickly."}',
                    AUTONOMY_PROPOSAL_END,
                ]
            ),
        )
    if AUTONOMY_REVIEW_START in prompt:
        if "Reviewer A" in prompt:
            key = "reviewer-a"
            attempt = attempts.get(key, 0)
            attempts[key] = attempt + 1
            if attempt == 0:
                return (1, "", "Reading additional input from stdin...", "")
        return (
            0,
            '{"type":"thread.started","thread_id":"advisory-review"}\n',
            "",
            "\n".join(
                [
                    "Review verdict ready.",
                    AUTONOMY_REVIEW_START,
                    '{"verdict":"approve","rationale":"The change is bounded and aligned with the stated goal.","risk":"Low","required_adjustment":"None"}',
                    AUTONOMY_REVIEW_END,
                ]
            ),
        )
    if AUTONOMY_VERIFY_START in prompt:
        degraded = "verdict: degraded" in prompt or "codex_exec_retrying" in prompt
        return (
            0,
            '{"type":"thread.started","thread_id":"advisory-verify"}\n',
            "",
            "\n".join(
                [
                    "Verification verdict ready.",
                    AUTONOMY_VERIFY_START,
                    (
                        '{"verdict":"fail","path_acceptability":"disqualifying","evidence":"The iteration only succeeded through degraded intended-path signals.","residual_risk":"The fallback path should not count as healthy autonomous progress.","follow_up":"Fix the degraded execution path before allowing unattended continuation."}'
                        if degraded
                        else '{"verdict":"pass","path_acceptability":"acceptable","evidence":"The implementation summary matches the approved bounded change through the expected path.","residual_risk":"Low","follow_up":"Continue with the next bounded improvement if the goal review recommends it."}'
                    ),
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
        advisory_timeout_seconds=180,
        running_job_grace_seconds=1,
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
        running_job_grace_seconds=settings.running_job_grace_seconds,
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
    prompt = build_prompt(
        settings,
        state.get_app("habit-tracker-pwa"),
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


def verify_proposer_prompt_contract() -> None:
    autonomy = api_app.AutonomyRuntime()
    goal = {
        "title": "Self-Improving Agentic Dev Environment",
        "objective": "Keep improving the runtime through bounded proposal-mode iterations.",
        "iterations": [
            {
                "iteration": 1,
                "status": "completed",
                "result_summary": "Healthy bounded improvement landed.",
                "goal_review": {"next_focus": "Tighten verification evidence."},
                "intended_path": {
                    "expected_path": "job_completed_without_degraded_signals",
                    "degraded_signals": [],
                    "verdict": "expected",
                },
                "continuation_blocker_reason": "none",
                "verification_reviews": [
                    {"verdict": "pass", "path_acceptability": "acceptable"},
                    {"verdict": "pass", "path_acceptability": "acceptable"},
                ],
            },
            {
                "iteration": 2,
                "status": "paused",
                "result_summary": "Fallback-only success should not continue unattended.",
                "goal_review": {"next_focus": "Target the degraded path directly."},
                "intended_path": {
                    "expected_path": "job_completed_without_degraded_signals",
                    "degraded_signals": ["codex_exec_retrying"],
                    "verdict": "degraded",
                },
                "continuation_blocker_reason": "verifier_path_disqualifying",
                "verification_reviews": [
                    {"verdict": "fail", "path_acceptability": "disqualifying"},
                    {"verdict": "fail", "path_acceptability": "disqualifying"},
                ],
            },
        ],
    }
    app_record = {"app_id": "factory-runtime", "title": "Factory Runtime"}
    prompt = autonomy.build_proposer_prompt(goal, app_record)
    require("blocker=none" in prompt, f"healthy proposer history should include blocker context: {prompt}")
    require(
        "blocker=verifier_path_disqualifying" in prompt,
        f"degraded proposer history should include canonical blocker reason: {prompt}",
    )
    require("intended_path=degraded" in prompt, f"proposer prompt should include intended-path verdicts: {prompt}")
    require("degraded_signals=codex_exec_retrying" in prompt, f"proposer prompt should include degraded signals: {prompt}")
    require(
        "verifier_path_acceptability=disqualifying" in prompt,
        f"proposer prompt should include verifier path-acceptability context: {prompt}",
    )
    require("next_focus=Target the degraded path directly." in prompt, f"proposer prompt should preserve next_focus: {prompt}")


def verify_review_rejection_proposer_context_contract() -> None:
    autonomy = api_app.AutonomyRuntime()
    goal = {
        "title": "Review rejection recovery",
        "objective": "Keep exploring bounded changes when review rejects one iteration.",
        "iterations": [
            {
                "iteration": 1,
                "status": "rejected_before_implementation",
                "result_summary": "Reviewer rejection before implementation.",
                "continuation_blocker_reason": "proposal_not_approved",
                "proposal_reviews": [
                    {
                        "verdict": "reject",
                        "rationale": "The hypothesis is still too close to the last rejected shape.",
                        "blocking_issue": "Needs a different bounded option.",
                        "suggested_adjustment": "Try another bounded hypothesis.",
                    },
                    {
                        "verdict": "reject",
                        "rationale": "The proposal is still too vague.",
                        "blocking_issue": "Still too vague.",
                        "suggested_adjustment": "Make the next hypothesis more specific.",
                    },
                ],
            }
        ],
    }
    prompt = autonomy.build_proposer_prompt(goal, {"app_id": "factory-runtime", "title": "Factory Runtime"})
    require(
        "blocker=proposal_not_approved" in prompt,
        f"rejected proposer history should include proposal_not_approved blocker: {prompt}",
    )
    require(
        "proposal_review_blocking_issues=Needs a different bounded option., Still too vague." in prompt,
        f"rejected proposer history should include structured blocking issues: {prompt}",
    )
    require(
        "proposal_review_suggested_adjustments=Make the next hypothesis more specific., Try another bounded hypothesis." in prompt,
        f"rejected proposer history should include structured suggested adjustments: {prompt}",
    )


def verify_blocker_precedence_contract() -> None:
    goals = GoalRuntime()
    disqualifying_blocker = goals.continuation_blocker_reason(
        {
            "proposal": {"status": "ready_to_apply"},
            "goal_review": {
                "continue_recommended": "yes",
                "alignment_assessment": "yes",
                "safety_assessment": "yes",
            },
        },
        proposal_ready=True,
        intended_path={"verdict": "expected", "degraded_signals": []},
        verification_reviews=[
            {"verdict": "fail", "path_acceptability": "disqualifying"},
            {"verdict": "fail", "path_acceptability": "disqualifying"},
        ],
    )
    require(
        disqualifying_blocker == "verifier_path_disqualifying",
        f"verifier disqualification should outrank proposal_ready: {disqualifying_blocker}",
    )

    healthy_proposal_blocker = goals.continuation_blocker_reason(
        {
            "proposal": {"status": "ready_to_apply"},
            "goal_review": {
                "continue_recommended": "yes",
                "alignment_assessment": "yes",
                "safety_assessment": "yes",
            },
        },
        proposal_ready=True,
        intended_path={"verdict": "expected", "degraded_signals": []},
        verification_reviews=[
            {"verdict": "pass", "path_acceptability": "acceptable"},
            {"verdict": "pass", "path_acceptability": "acceptable"},
        ],
    )
    require(
        healthy_proposal_blocker == "proposal_ready",
        f"healthy proposal-ready iterations should still keep proposal_ready blocker: {healthy_proposal_blocker}",
    )

    autonomy = api_app.AutonomyRuntime()
    proposer_prompt = autonomy.build_proposer_prompt(
        {
            "iterations": [
                {
                    "iteration": 1,
                    "status": "paused",
                    "continuation_blocker_reason": "verifier_path_disqualifying",
                    "intended_path": {"verdict": "expected", "degraded_signals": []},
                    "verification_reviews": [
                        {"verdict": "fail", "path_acceptability": "disqualifying"},
                    ],
                    "goal_review": {"next_focus": "Fix the verifier-disqualifying path first."},
                    "result_summary": "Proposal was ready, but verifier evidence disqualified the path.",
                }
            ]
        },
        {"app_id": "factory-runtime", "title": "Factory Runtime"},
    )
    require(
        "blocker=verifier_path_disqualifying" in proposer_prompt,
        f"proposer prompt should expose verifier_path_disqualifying blocker: {proposer_prompt}",
    )


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
            require("goal-task-contract" in context.goal_tasks, "spawned goal task should be retained until completion")
            first_task = context.goal_tasks["goal-task-contract"]
            context.spawn_goal_loop("goal-task-contract")
            require(context.goal_tasks["goal-task-contract"] is first_task, "spawn_goal_loop should not replace an active goal task")
            release.set()
            await asyncio.wait_for(first_task, timeout=1.0)
            await asyncio.sleep(0)
            require("goal-task-contract" not in context.goal_tasks, "completed goal task should be removed from the retained task table")
        finally:
            RuntimeApiContext.run_goal_loop = original_run_goal_loop

    asyncio.run(_run())


def verify_reconcile_orphaned_running_job(settings: RuntimeSettings, state: RuntimeState) -> None:
    context = RuntimeApiContext(
        settings=settings,
        state=state,
        runtime=api_app.CodexAgentsRuntime(settings, state),
        goals=GoalRuntime(),
        autonomy=api_app.AutonomyRuntime(),
    )
    conversation = state.create_conversation(app_id="factory-runtime", title="Orphaned job", source="contract-test")
    request_payload = state.create_request(
        app_id="factory-runtime",
        title="Orphaned job",
        request_text="Test orphaned running job reconciliation.",
        source="contract-test",
        conversation_id=conversation["conversation_id"],
    )
    job = state.create_job(
        app_id="factory-runtime",
        request_id=request_payload["request_id"],
        title="Orphaned job",
        conversation_id=conversation["conversation_id"],
    )
    state.update_job(
        job["job_id"],
        status="running",
        started_at="2000-01-01T00:00:00+00:00",
        runner_pid=0,
    )
    context.reconcile_running_jobs()
    reconciled = state.get_job(job["job_id"])
    require(reconciled["status"] == "failed", f"orphaned running job should be reconciled to failed: {reconciled}")
    require("orphaned_running_job" in reconciled["error"], f"reconciled job should record orphaned reason: {reconciled}")


def verify_reconcile_stale_running_goal(settings: RuntimeSettings, state: RuntimeState) -> None:
    conversation = state.create_conversation(app_id="factory-runtime", title="Stale Goal", source="contract-test")
    goal = state.create_goal(
        app_id="factory-runtime",
        title="Stale Goal",
        objective="Detect stale running goals without a live job process.",
        source="contract-test",
        conversation_id=conversation["conversation_id"],
        max_iterations=0,
        auto_apply_proposals=True,
        auto_resume_after_apply=True,
    )
    goal["status"] = "running"
    goal["started_at"] = "2026-01-01T00:00:00+00:00"
    goal["updated_at"] = "2026-01-01T00:00:00+00:00"
    goal["current_iteration"] = 3
    goal["current_phase"] = "implementation"
    goal["current_job_id"] = "missing-job"
    goal["last_job_id"] = "missing-job"
    state.save_goal(goal)

    context = RuntimeApiContext(
        settings=settings,
        state=state,
        runtime=api_app.CodexAgentsRuntime(settings, state),
        goals=GoalRuntime(),
        autonomy=api_app.AutonomyRuntime(),
    )
    context.reconcile_running_goals()

    reconciled = state.get_goal(goal["goal_id"])
    require(reconciled["status"] == "paused", f"stale running goal should be paused: {reconciled}")
    require(reconciled["stop_reason"] == "stale_running_goal", f"stale running goal should record stop reason: {reconciled}")
    require(reconciled["current_phase"] == "", f"stale running goal should clear current phase: {reconciled}")
    require(reconciled["current_job_id"] == "", f"stale running goal should clear current job id: {reconciled}")
    refreshed_conversation = state.get_conversation(conversation["conversation_id"])
    require(
        any(event.get("type") == "goal.paused" and "stale running goal" in str(event.get("body") or "") for event in refreshed_conversation.get("events") or []),
        f"stale running goal should append a paused event: {refreshed_conversation}",
    )


def verify_retryable_advisory_phase(settings: RuntimeSettings, state: RuntimeState) -> None:
    async def _run() -> None:
        context = RuntimeApiContext(
            settings=settings,
            state=state,
            runtime=api_app.CodexAgentsRuntime(settings, state),
            goals=GoalRuntime(),
            autonomy=api_app.AutonomyRuntime(),
        )
        goal = {"goal_id": "retry-goal", "objective": "Verify retry handling."}
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
        event_types = [event["type"] for event in context.state.get_conversation(conversation["conversation_id"])["events"]]
        require("goal.review.phase.retrying" in event_types, f"retryable advisory failure should emit retry event: {event_types}")

    asyncio.run(_run())


def verify_goal_continues_after_review_rejection(settings: RuntimeSettings, state: RuntimeState) -> None:
    async def _run() -> None:
        original_proposal = RuntimeApiContext.run_autonomy_proposal
        original_review = RuntimeApiContext.run_autonomy_review

        async def fake_proposal(self, *, goal, app_record, conversation_id, iteration_number):
            return {
                "hypothesis": f"Improve iteration {iteration_number}",
                "target_area": "conversation",
                "change_outline": "Keep moving with one bounded step.",
                "success_criteria": "A bounded step is implemented.",
                "why_now": "Contract coverage.",
            }

        async def fake_review(self, *, goal, app_record, proposal, conversation_id, iteration_number, reviewer_name):
            verdict = "reject" if iteration_number == 1 else "approve"
            return {
                "verdict": verdict,
                "rationale": f"{reviewer_name} returned {verdict} on iteration {iteration_number}.",
                "blocking_issue": "Needs a different bounded option." if verdict == "reject" else "",
                "suggested_adjustment": "Try another bounded hypothesis." if verdict == "reject" else "",
            }

        RuntimeApiContext.run_autonomy_proposal = fake_proposal
        RuntimeApiContext.run_autonomy_review = fake_review
        context = RuntimeApiContext(
            settings=settings,
            state=state,
            runtime=api_app.CodexAgentsRuntime(settings, state),
            goals=GoalRuntime(),
            autonomy=api_app.AutonomyRuntime(),
        )
        try:
            created = context.create_goal(
                app_id="habit-tracker-pwa",
                title="Review rejection recovery",
                objective="Keep exploring bounded changes when review rejects one iteration.",
                source="contract-test",
                max_iterations=2,
                autostart=False,
                auto_apply_proposals=False,
                auto_resume_after_apply=False,
            )
            goal = created["goal"]
            goal["status"] = "running"
            goal["started_at"] = utc_now()
            context.state.save_goal(goal)

            await context.run_goal_loop(goal["goal_id"])

            final_goal = context.state.get_goal(goal["goal_id"])
            require(final_goal["status"] == "completed", f"goal should keep going after review rejection: {final_goal}")
            require(final_goal["current_iteration"] == 2, f"goal should advance to a second iteration after review rejection: {final_goal}")
            require(len(final_goal.get("iterations") or []) == 2, f"goal should record both rejected and completed iterations: {final_goal}")
            require(
                final_goal["iterations"][0]["status"] == "rejected_before_implementation",
                f"first iteration should be recorded as rejected before implementation: {final_goal['iterations']}",
            )
            event_types = [event["type"] for event in context.state.get_conversation(created["conversation"]["conversation_id"])["events"]]
            require("goal.iteration.rejected" in event_types, f"review rejection should emit recovery event: {event_types}")
            require("goal.completed" in event_types, f"goal should still complete after trying another option: {event_types}")
        finally:
            RuntimeApiContext.run_autonomy_proposal = original_proposal
            RuntimeApiContext.run_autonomy_review = original_review

    asyncio.run(_run())


def verify_goal_continues_after_verification_rejection(settings: RuntimeSettings, state: RuntimeState) -> None:
    async def _run() -> None:
        original_proposal = RuntimeApiContext.run_autonomy_proposal
        original_review = RuntimeApiContext.run_autonomy_review
        original_verifier = RuntimeApiContext.run_autonomy_verifier

        async def fake_proposal(self, *, goal, app_record, conversation_id, iteration_number):
            return {
                "hypothesis": f"Improve verification iteration {iteration_number}",
                "target_area": "runtime",
                "change_outline": "Apply one bounded autonomous improvement.",
                "success_criteria": "The proposal passes verification.",
                "why_now": "Contract coverage.",
            }

        async def fake_review(self, *, goal, app_record, proposal, conversation_id, iteration_number, reviewer_name):
            return {
                "verdict": "approve",
                "rationale": f"{reviewer_name} approved iteration {iteration_number}.",
                "blocking_issue": "",
                "suggested_adjustment": "",
            }

        async def fake_verifier(self, *, goal, app_record, proposal, implementation_summary, intended_path, conversation_id, iteration_number, verifier_name, cwd):
            verdict = "fail" if iteration_number == 1 else "pass"
            return {
                "verdict": verdict,
                "path_acceptability": "disqualifying" if verdict == "fail" else "acceptable",
                "evidence": f"{verifier_name} produced {verdict} on iteration {iteration_number}.",
                "residual_risk": "Needs another bounded option." if verdict == "fail" else "Low",
                "follow_up": "Explore a different bounded hypothesis." if verdict == "fail" else "Stop after success.",
            }

        RuntimeApiContext.run_autonomy_proposal = fake_proposal
        RuntimeApiContext.run_autonomy_review = fake_review
        RuntimeApiContext.run_autonomy_verifier = fake_verifier
        context = RuntimeApiContext(
            settings=settings,
            state=state,
            runtime=api_app.CodexAgentsRuntime(settings, state),
            goals=GoalRuntime(),
            autonomy=api_app.AutonomyRuntime(),
        )
        try:
            created = context.create_goal(
                app_id="factory-runtime",
                title="Verification rejection recovery",
                objective="Keep exploring bounded changes when verification rejects one iteration.",
                source="contract-test",
                max_iterations=2,
                autostart=False,
                auto_apply_proposals=True,
                auto_resume_after_apply=False,
            )
            goal = created["goal"]
            goal["status"] = "running"
            goal["started_at"] = utc_now()
            context.state.save_goal(goal)

            await context.run_goal_loop(goal["goal_id"])

            final_goal = context.state.get_goal(goal["goal_id"])
            require(final_goal["status"] == "completed", f"goal should keep going after verification rejection: {final_goal}")
            require(final_goal["current_iteration"] == 2, f"goal should advance to a second iteration after verification rejection: {final_goal}")
            require(len(final_goal.get("iterations") or []) == 2, f"goal should record both iterations after verifier rejection: {final_goal}")
            first_iteration = final_goal["iterations"][0]
            require(
                any(review.get("verdict") == "fail" for review in first_iteration.get("verification_reviews") or []),
                f"first iteration should capture failed verification reviews: {first_iteration}",
            )
            require(
                all(review.get("path_acceptability") == "disqualifying" for review in first_iteration.get("verification_reviews") or []),
                f"failed verification reviews should record disqualifying path acceptability: {first_iteration}",
            )
            event_types = [event["type"] for event in context.state.get_conversation(created["conversation"]["conversation_id"])["events"]]
            require("goal.iteration.verification_rejected" in event_types, f"verification rejection should emit recovery event: {event_types}")
            require("goal.proposal.auto_apply.completed" in event_types, f"second iteration should auto-apply after passing verification: {event_types}")
            require("goal.completed" in event_types, f"goal should still complete after trying another option: {event_types}")
        finally:
            RuntimeApiContext.run_autonomy_proposal = original_proposal
            RuntimeApiContext.run_autonomy_review = original_review
            RuntimeApiContext.run_autonomy_verifier = original_verifier

    asyncio.run(_run())


def verify_legacy_goal_defaults_continue(settings: RuntimeSettings, state: RuntimeState) -> None:
    context = RuntimeApiContext(
        settings=settings,
        state=state,
        runtime=api_app.CodexAgentsRuntime(settings, state),
        goals=GoalRuntime(),
        autonomy=api_app.AutonomyRuntime(),
    )
    legacy_goal = {
        "goal_id": "legacy-goal",
        "policy": {
            "open_ended": True,
        },
        "max_iterations": 0,
    }
    require(
        context._goal_can_explore_alternative(legacy_goal, iteration_number=1, failure_kind="review"),
        "legacy goals without explicit review-failure policy should default to continued exploration",
    )
    require(
        context._goal_can_explore_alternative(legacy_goal, iteration_number=1, failure_kind="verification"),
        "legacy goals without explicit verification-failure policy should default to continued exploration",
    )


def verify_iap_provider() -> None:
    settings = build_iap_settings(Path(tempfile.mkdtemp(prefix="codex-iap-contract-")))
    original_verify = IapIdentityProvider.verify_iap_assertion
    try:
        IapIdentityProvider.verify_iap_assertion = lambda self, token: {
            "iss": "https://cloud.google.com/iap",
            "aud": settings.iap_expected_audience,
            "sub": "iap-user",
            "email": token,
        }
        app = api_app.create_app(settings)
        client = TestClient(app)
        allowed = client.get("/api/apps", headers={IAP_JWT_HEADER: "owner@example.com"})
        require(allowed.status_code == 200, f"IAP provider should allow configured user: {allowed.text}")
        denied = client.get("/api/apps", headers={IAP_JWT_HEADER: "other@example.com"})
        require(denied.status_code == 403, f"IAP provider should reject other users: {denied.text}")
    finally:
        IapIdentityProvider.verify_iap_assertion = original_verify


def verify_tailscale_provider() -> None:
    tail_settings = build_settings(Path(tempfile.mkdtemp(prefix="codex-tail-contract-")))
    tail_settings = RuntimeSettings(**{**tail_settings.__dict__, "auth_providers": ["tailscale"], "runtime_api_key": ""})
    tail_client = TestClient(api_app.create_app(tail_settings))
    response = tail_client.get(
        "/api/apps",
        headers={TAILSCALE_LOGIN_HEADER: "owner@example.com", TAILSCALE_NAME_HEADER: "operator-phone"},
    )
    require(response.status_code == 200, f"tailscale auth should allow app listing: {response.text}")


def verify_conversation_append_stream(client: TestClient) -> None:
    route_paths = {route.path for route in client.app.router.routes}
    require(
        "/api/internal/conversations/{conversation_id}/append-stream" in route_paths,
        "append stream route should be registered on the runtime API",
    )

    conversation_response = request(
        client,
        "POST",
        "/api/conversations",
        json={"app_id": "habit-tracker-pwa", "title": "SSE contract", "source": "contract-test"},
    )
    require(conversation_response.status_code == 200, f"append stream conversation failed: {conversation_response.text}")
    conversation_id = conversation_response.json()["conversation_id"]

    request(
        client,
        "POST",
        f"/api/conversations/{conversation_id}/messages",
        json={
            "title": "SSE message",
            "message_text": "Check append stream contract.",
            "source": "contract-test",
            "execute_now": False,
        },
    )
    conversation = request(client, "GET", f"/api/conversations/{conversation_id}").json()
    first_message = conversation["messages"][0]
    first_event = conversation["events"][0]
    require(int(first_message.get("append_id") or 0) > 0, "conversation messages should carry append_id")
    require(int(first_event.get("append_id") or 0) > 0, "conversation events should carry append_id")
    require(
        int(first_message.get("append_id") or 0) != int(first_event.get("append_id") or 0),
        "conversation append ids should advance across messages and events",
    )
    snapshot_autonomy = conversation.get("autonomy_summary") or {}
    require(isinstance(snapshot_autonomy, dict), f"conversation snapshot should expose autonomy_summary envelope: {conversation}")
    require(snapshot_autonomy.get("source") == "conversation-snapshot", f"conversation snapshot should mark snapshot autonomy source: {snapshot_autonomy}")
    require("generated_at" in snapshot_autonomy, f"conversation snapshot autonomy envelope should include generated_at: {snapshot_autonomy}")
    require("freshness_state" in snapshot_autonomy, f"conversation snapshot autonomy envelope should include freshness_state: {snapshot_autonomy}")
    require("fallback_allowed" in snapshot_autonomy, f"conversation snapshot autonomy envelope should include fallback_allowed: {snapshot_autonomy}")
    with client.stream(
        "GET",
        f"/api/internal/conversations/{conversation_id}/append-stream",
        headers=DEFAULT_HEADERS,
    ) as response:
        require(response.status_code == 200, f"append stream request failed: {response.text}")
        lines = []
        for raw_line in response.iter_lines():
            if raw_line is None:
                continue
            line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
            lines.append(line)
            if line == "":
                break
        require(any(line == "event: session.bootstrap" for line in lines), "append stream should emit session.bootstrap before append events")
        data_lines = [line.split(":", 1)[1].lstrip() for line in lines if line.startswith("data:")]
        bootstrap = json.loads("\n".join(data_lines))
        require(bootstrap.get("version") == 2, f"session bootstrap should be versioned: {bootstrap}")
        require(bootstrap.get("attach_mode") == "sse-bootstrap", f"session bootstrap should mark sse attach mode: {bootstrap}")
        require(int(bootstrap.get("resume_from_append_id") or 0) == 0, f"initial bootstrap should not resume from append id: {bootstrap}")
        require(isinstance(bootstrap.get("session_phase"), dict), f"session bootstrap should expose session_phase payload: {bootstrap}")
        require(isinstance(bootstrap.get("session_status"), dict), f"session bootstrap should expose session_status payload: {bootstrap}")
        require("value" in (bootstrap.get("session_phase") or {}), f"session bootstrap phase payload should include value: {bootstrap}")
        require("authoritative" in (bootstrap.get("session_phase") or {}), f"session bootstrap phase payload should include authoritative flag: {bootstrap}")
        require(bootstrap.get("session_status", {}).get("version") == 1, f"session bootstrap should expose versioned session_status: {bootstrap}")
        require(bootstrap.get("session_status", {}).get("conversation_id") == conversation_id, f"session bootstrap session_status should match conversation: {bootstrap}")
        require(bootstrap.get("session_status", {}).get("transport", {}).get("channel") == "append-sse", f"session bootstrap session_status should mark append-sse channel: {bootstrap}")
        require(bootstrap.get("session_status", {}).get("transport", {}).get("state") == "sse-bootstrap", f"session bootstrap session_status should mark sse-bootstrap state: {bootstrap}")
        require(bootstrap.get("session_status", {}).get("transport", {}).get("attach_mode") == "sse-bootstrap", f"session bootstrap session_status should mark sse-bootstrap attach mode: {bootstrap}")
        require(bootstrap.get("session_status", {}).get("phase", {}).get("value") == bootstrap.get("session_phase", {}).get("value"), f"session bootstrap session_status phase should mirror session_phase: {bootstrap}")
        require("proposal_ready" in (bootstrap.get("session_status") or {}), f"session bootstrap session_status should expose proposal_ready: {bootstrap}")
        require(bootstrap.get("conversation", {}).get("conversation_id") == conversation_id, "session bootstrap should hydrate the selected conversation")
        bootstrap_autonomy = bootstrap.get("autonomy_summary") or {}
        require(isinstance(bootstrap_autonomy, dict), f"session bootstrap should expose autonomy_summary envelope: {bootstrap}")
        require(bootstrap_autonomy.get("source") == "session-bootstrap", f"session bootstrap should mark bootstrap autonomy source: {bootstrap_autonomy}")
        require(bootstrap_autonomy.get("generated_at") == snapshot_autonomy.get("generated_at"), f"bootstrap autonomy envelope should reuse snapshot freshness timestamp: {bootstrap_autonomy}")
        require(bootstrap_autonomy.get("freshness_state") == snapshot_autonomy.get("freshness_state"), f"bootstrap autonomy envelope should match snapshot freshness state: {bootstrap_autonomy}")
        require(bootstrap_autonomy.get("fallback_allowed") is False, f"session bootstrap autonomy envelope should disallow fallback on healthy attach: {bootstrap_autonomy}")
        require(
            (bootstrap.get("conversation") or {}).get("autonomy_summary", {}).get("freshness_state") == bootstrap_autonomy.get("freshness_state"),
            f"bootstrap conversation autonomy envelope should match top-level freshness state: {bootstrap}",
        )

    with client.stream(
        "GET",
        f"/api/internal/conversations/{conversation_id}/append-stream?after=3",
        headers=DEFAULT_HEADERS,
    ) as response:
        require(response.status_code == 200, f"append stream resume request failed: {response.text}")
        lines = []
        for raw_line in response.iter_lines():
            if raw_line is None:
                continue
            line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
            lines.append(line)
            if line == "":
                break
        data_lines = [line.split(":", 1)[1].lstrip() for line in lines if line.startswith("data:")]
        bootstrap = json.loads("\n".join(data_lines))
        require(bootstrap.get("version") == 2, f"resume bootstrap should keep versioned contract: {bootstrap}")
        require(bootstrap.get("attach_mode") == "sse-resume", f"resume bootstrap should mark sse resume mode: {bootstrap}")
        require(int(bootstrap.get("resume_from_append_id") or 0) == 3, f"resume bootstrap should echo requested append cursor: {bootstrap}")
        require(isinstance(bootstrap.get("session_phase"), dict), f"resume bootstrap should expose session_phase payload: {bootstrap}")
        require(isinstance(bootstrap.get("session_status"), dict), f"resume bootstrap should expose session_status payload: {bootstrap}")
        require(bootstrap.get("session_status", {}).get("transport", {}).get("state") == "sse-resume", f"resume bootstrap session_status should mark sse-resume state: {bootstrap}")
        require(bootstrap.get("session_status", {}).get("transport", {}).get("attach_mode") == "sse-resume", f"resume bootstrap session_status should mark sse-resume attach mode: {bootstrap}")
        require(isinstance(bootstrap.get("autonomy_summary"), dict), f"resume bootstrap should expose autonomy_summary envelope: {bootstrap}")
        require(bootstrap.get("autonomy_summary", {}).get("source") == "session-bootstrap", f"resume bootstrap should keep bootstrap autonomy source: {bootstrap}")


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
            verify_proposer_prompt_contract()
            verify_review_rejection_proposer_context_contract()
            verify_blocker_precedence_contract()
            verify_goal_task_lifecycle(settings, state)
            verify_reconcile_orphaned_running_job(settings, state)
            verify_reconcile_stale_running_goal(settings, state)
            verify_retryable_advisory_phase(settings, state)
            verify_goal_continues_after_review_rejection(settings, state)
            verify_goal_continues_after_verification_rejection(settings, state)
            verify_legacy_goal_defaults_continue(settings, state)
            verify_iap_provider()

            client = TestClient(api_app.create_app(settings))
            verify_tailscale_provider()
            verify_conversation_append_stream(client)

            runner = CodexCliRunner(settings)
            resume_command = runner.build_command(
                "019d6fed-7653-7dd1-aa05-774a52a635d9",
                "Reply with exactly CONTRACT_RESUME_OK.",
                temp_root / "resume-last-message.txt",
                use_resume=True,
            )
            require("--sandbox" not in resume_command, f"resume command must not include --sandbox: {resume_command}")
            require("resume" in resume_command, f"resume command should include resume subcommand: {resume_command}")
            fresh_command = runner.build_command(
                "",
                "Reply with exactly CONTRACT_FRESH_OK.",
                temp_root / "fresh-last-message.txt",
                use_resume=False,
            )
            require("--sandbox" in fresh_command, f"fresh exec command should include sandbox selection: {fresh_command}")

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
                json={
                    "message_text": "Reply with exactly one line and do not modify files.",
                    "source": "contract-test",
                },
            )
            require(message_response.status_code == 200, f"message failed: {message_response.text}")
            payload = message_response.json()
            job_id = payload["job"]["job_id"]
            require(payload["job"]["status"] == "queued", "job should be queued before background execution completes")
            require(payload["request"]["intent_summary"]["explicit_request"], "request should include interpreted intent")
            require(payload["job"]["intent_summary"]["interpreted_outcome"], "job should include interpreted outcome")

            job = request(client, "GET", f"/api/jobs/{job_id}").json()
            require(job["status"] == "completed", f"expected completed job, got {job['status']}")
            require(job["result_summary"].startswith("SIMULATED_OK:"), f"unexpected job summary: {job['result_summary']}")
            require(job["decision_summary"]["verification"], "decision summary should include verification evidence")
            require(job["intent_summary"]["success_signal"], "job intent summary should include success signal")

            conversation_after = request(client, "GET", f"/api/conversations/{conversation_id}").json()
            message_types = [message["role"] for message in conversation_after["messages"]]
            event_types = [event["type"] for event in conversation_after["events"]]
            require(message_types == ["user", "assistant"], f"unexpected conversation message roles: {message_types}")
            require(
                all(
                    name in event_types
                    for name in ["conversation.created", "message.accepted", "intent.interpreted", "job.queued", "job.running", "job.completed"]
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

            proposal_events = [event["type"] for event in request(client, "GET", f"/api/conversations/{proposal_conversation['conversation_id']}").json()["events"]]
            require("proposal.ready" in proposal_events, f"missing proposal.ready event: {proposal_events}")
            require("proposal.applied" in proposal_events, f"missing proposal.applied event: {proposal_events}")

            goal_response = request(
                client,
                "POST",
                "/api/goals",
                json={
                    "app_id": "habit-tracker-pwa",
                    "objective": "Keep improving the runtime through bounded iterations until the goal review says to stop.",
                    "source": "contract-test",
                    "max_iterations": 0,
                    "autostart": True,
                },
            )
            require(goal_response.status_code == 200, f"goal creation failed: {goal_response.text}")
            goal = wait_for_goal_status(client, goal_response.json()["goal"]["goal_id"], "completed")
            require(goal["stop_reason"] == "goal_review_stop", f"goal should stop through goal review signal: {goal}")
            require(len(goal["iterations"]) == 2, f"expected 2 goal iterations, got {len(goal['iterations'])}")
            require(
                all(
                    (item.get("intended_path") or {}).get("verdict") == "expected"
                    and not (item.get("intended_path") or {}).get("degraded_signals")
                    for item in goal["iterations"]
                ),
                f"healthy goal iterations should record expected intended path verdicts: {goal['iterations']}",
            )
            require(
                all((item.get("continuation_blocker_reason") or "none") in {"none", "goal_review_stop"} for item in goal["iterations"]),
                f"healthy goal iterations should only record none or goal_review_stop as continuation blockers: {goal['iterations']}",
            )

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
            require(proposal_goal["stop_reason"] == "goal_review_stop", f"proposal goal should stop through goal review signal: {proposal_goal}")
            require(proposal_goal["iterations"][0]["auto_applied"] is True, "first proposal goal iteration should be auto-applied")
            require(proposal_goal["iterations"][0]["proposal_status"] == "applied", "proposal goal iteration should record applied proposal status")
            require(
                proposal_goal["iterations"][0]["intended_path"]["verdict"] == "expected",
                f"healthy proposal iteration should keep expected intended-path verdict: {proposal_goal['iterations'][0]}",
            )
            require(
                all(review.get("path_acceptability") == "acceptable" for review in proposal_goal["iterations"][0].get("verification_reviews") or []),
                f"healthy proposal iteration should record acceptable path attestation: {proposal_goal['iterations'][0]}",
            )
            require(
                (proposal_goal["iterations"][0].get("continuation_blocker_reason") or "none") == "none",
                f"healthy proposal iteration should not record a continuation blocker: {proposal_goal['iterations'][0]}",
            )

            degraded_goal_response = request(
                client,
                "POST",
                "/api/goals",
                json={
                    "app_id": "habit-tracker-pwa",
                    "objective": "SIMULATE_DEGRADED_RETRY: verify that fallback-only success does not count as healthy unattended progress.",
                    "source": "contract-test",
                    "max_iterations": 0,
                    "autostart": True,
                },
            )
            require(degraded_goal_response.status_code == 200, f"degraded goal creation failed: {degraded_goal_response.text}")
            degraded_goal = wait_for_goal_status(client, degraded_goal_response.json()["goal"]["goal_id"], "paused")
            require(degraded_goal["stop_reason"] == "intended_path_degraded", f"degraded goal should pause on intended-path verdict: {degraded_goal}")
            require(len(degraded_goal["iterations"]) == 1, f"degraded goal should pause on first iteration: {degraded_goal}")
            degraded_path = degraded_goal["iterations"][0].get("intended_path") or {}
            require(degraded_path.get("verdict") == "degraded", f"degraded goal should record degraded verdict: {degraded_goal['iterations'][0]}")
            require(
                degraded_goal["iterations"][0].get("continuation_blocker_reason") == "intended_path_degraded",
                f"degraded goal iteration should record intended_path_degraded blocker: {degraded_goal['iterations'][0]}",
            )
            require(
                "codex_exec_retrying" in (degraded_path.get("degraded_signals") or []),
                f"degraded retry signal should be visible in intended-path state: {degraded_goal['iterations'][0]}",
            )

            degraded_proposal_goal_response = request(
                client,
                "POST",
                "/api/goals",
                json={
                    "app_id": "factory-runtime",
                    "objective": "SIMULATE_DEGRADED_RETRY: proposal-mode verification should attest that fallback-only success is disqualifying.",
                    "source": "contract-test",
                    "max_iterations": 1,
                    "autostart": True,
                    "auto_apply_proposals": True,
                    "auto_resume_after_apply": False,
                },
            )
            require(
                degraded_proposal_goal_response.status_code == 200,
                f"degraded proposal goal creation failed: {degraded_proposal_goal_response.text}",
            )
            degraded_proposal_goal = wait_for_goal_status(client, degraded_proposal_goal_response.json()["goal"]["goal_id"], "paused")
            require(
                degraded_proposal_goal["stop_reason"] in {"verifier_path_disqualifying", "proposal_ready", "intended_path_degraded"},
                f"degraded proposal goal should pause with a verifier or proposal blocker: {degraded_proposal_goal}",
            )
            degraded_reviews = degraded_proposal_goal["iterations"][0].get("verification_reviews") or []
            require(degraded_reviews, f"degraded proposal goal should persist verifier reviews: {degraded_proposal_goal}")
            require(
                degraded_proposal_goal["iterations"][0].get("continuation_blocker_reason")
                in {"verifier_path_disqualifying", "proposal_ready", "intended_path_degraded"},
                f"degraded proposal goal iteration should record a verifier or proposal blocker: {degraded_proposal_goal['iterations'][0]}",
            )
            require(
                all(review.get("path_acceptability") == "disqualifying" for review in degraded_reviews),
                f"degraded proposal verifier reviews should record disqualifying path attestation: {degraded_proposal_goal['iterations'][0]}",
            )
            require(
                all(review.get("verdict") == "fail" for review in degraded_reviews),
                f"degraded proposal verifier reviews should fail when intended path is degraded: {degraded_proposal_goal['iterations'][0]}",
            )

    finally:
        api_app.CodexAgentsRuntime.run_request = original_run_request
        api_app.CodexAgentsRuntime.apply_proposal = original_apply_proposal
        api_app.CodexAgentsRuntime.run_advisory_prompt = original_run_advisory_prompt


if __name__ == "__main__":
    main()
