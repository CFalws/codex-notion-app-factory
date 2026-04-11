from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import asyncio
import json
import os
from pathlib import Path
from datetime import datetime, timezone

from fastapi import BackgroundTasks, HTTPException

from .agent_runtime import CodexAgentsRuntime
from .config import RuntimeSettings
from .runtime_autonomy import (
    AutonomyRuntime,
    extract_proposal_json,
    extract_review_json,
    extract_verify_json,
    normalize_proposal_json,
    normalize_review_json,
    normalize_verify_json,
)
from .runtime_engineering import infer_intent_summary
from .runtime_goals import GoalRuntime
from .state import RuntimeState, utc_now


@dataclass(slots=True)
class RuntimeApiContext:
    settings: RuntimeSettings
    state: RuntimeState
    runtime: CodexAgentsRuntime
    goals: GoalRuntime
    autonomy: AutonomyRuntime
    goal_tasks: dict[str, asyncio.Task[Any]] = field(default_factory=dict)
    append_subscribers: dict[str, set[asyncio.Queue[dict[str, Any]]]] = field(default_factory=dict)

    def conversation_append_snapshot(self, conversation_id: str, *, after_append_id: int = 0) -> list[dict[str, Any]]:
        conversation = self.require_conversation(conversation_id)
        items: list[dict[str, Any]] = []
        for kind, key in (("message", "messages"), ("event", "events")):
            for payload in conversation.get(key, []):
                append_id = int(payload.get("append_id") or 0)
                if append_id <= after_append_id:
                    continue
                items.append(
                    {
                        "conversation_id": conversation_id,
                        "kind": kind,
                        "append_id": append_id,
                        "payload": payload,
                        "session_phase": self.conversation_session_phase(payload, kind=kind),
                    }
                )
        items.sort(key=lambda item: int(item["append_id"]))
        return items

    def conversation_session_phase(self, payload: dict[str, Any] | None, *, kind: str) -> dict[str, Any]:
        item = payload if isinstance(payload, dict) else {}
        phase = "UNKNOWN"
        authoritative = False
        event_type = str(item.get("type") or "")
        status = str(item.get("status") or "").lower()
        reason = "no-authoritative-phase"

        if kind == "event":
            if status == "failed" or event_type == "runtime.exception":
                phase = "FAILED"
                authoritative = True
                reason = "event-phase"
            elif event_type == "proposal.ready":
                phase = "READY"
                authoritative = True
                reason = "event-phase"
            elif event_type == "codex.exec.applied" or status == "applied":
                phase = "APPLIED"
                authoritative = True
                reason = "event-phase"
            elif event_type.startswith("goal.verify.phase."):
                phase = "VERIFY"
                authoritative = True
                reason = "event-phase"
            elif event_type.startswith("goal.review.phase."):
                phase = "REVIEW"
                authoritative = True
                reason = "event-phase"
            elif event_type.startswith("goal.proposal.phase."):
                phase = "PROPOSAL"
                authoritative = True
                reason = "event-phase"
            elif event_type:
                phase = "LIVE"
                reason = "non-authoritative-event"
        elif kind == "message":
            phase = "LIVE"
            reason = "non-authoritative-message"

        return {
            "value": phase,
            "authoritative": authoritative,
            "reason": reason,
            "kind": kind,
            "event_type": event_type,
            "status": status,
            "job_id": str(item.get("job_id") or ""),
            "append_id": int(item.get("append_id") or 0),
            "created_at": str(item.get("created_at") or ""),
            "source": "sse",
        }

    def conversation_session_bootstrap(
        self,
        conversation_id: str,
        *,
        requested_after_append_id: int = 0,
    ) -> dict[str, Any]:
        conversation = self.conversation_snapshot_payload(
            conversation_id,
            source="session-bootstrap",
            fallback_allowed=False,
        )
        messages = list(conversation.get("messages", []))
        events = list(conversation.get("events", []))
        append_cursor = 0
        latest_event: dict[str, Any] | None = None
        latest_item: tuple[str, dict[str, Any]] | None = None
        for item in [*messages, *events]:
            append_id = int(item.get("append_id") or 0)
            if append_id > append_cursor:
                append_cursor = append_id
        for kind, items in (("message", messages), ("event", events)):
            for item in items:
                append_id = int(item.get("append_id") or 0)
                if latest_item is None or append_id >= int(latest_item[1].get("append_id") or 0):
                    latest_item = (kind, item)
        if events:
            latest_event = max(events, key=lambda item: int(item.get("append_id") or 0))
        resume_cursor = max(int(requested_after_append_id or 0), 0)
        attach_mode = "sse-resume" if resume_cursor else "sse-bootstrap"
        latest_kind, latest_payload = latest_item if latest_item else ("event", {})
        return {
            "version": 2,
            "conversation_id": conversation_id,
            "attach_mode": attach_mode,
            "append_cursor": append_cursor,
            "resume_from_append_id": resume_cursor,
            "conversation": conversation,
            "autonomy_summary": dict(conversation.get("autonomy_summary") or {}),
            "latest_job_id": str(conversation.get("latest_job_id") or ""),
            "session_phase": self.conversation_session_phase(latest_payload, kind=latest_kind),
            "live_phase_summary": {
                "event_type": str((latest_event or {}).get("type") or ""),
                "status": str((latest_event or {}).get("status") or ""),
                "job_id": str((latest_event or {}).get("job_id") or conversation.get("latest_job_id") or ""),
                "append_id": int((latest_event or {}).get("append_id") or 0),
            },
            "composer_owner": {
                "state": "ready",
                "conversation_id": conversation_id,
                "target_title": str(conversation.get("title") or ""),
            },
        }

    def _pick_relevant_goal(self, app_id: str) -> dict[str, Any] | None:
        items = list(self.state.list_goals(app_id=app_id))
        if not items:
            return None
        return next(
            (
                goal
                for goal in items
                if str(goal.get("status") or "").lower() == "running"
            ),
            next(
                (
                    goal
                    for goal in items
                    if str(goal.get("status") or "").lower() == "paused"
                ),
                items[0],
            ),
        )

    def _latest_goal_iteration(self, goal: dict[str, Any] | None) -> dict[str, Any] | None:
        iterations = goal.get("iterations") if isinstance(goal, dict) else []
        if not isinstance(iterations, list) or not iterations:
            return None
        return iterations[-1]

    def _summarize_verifier_acceptability(self, iteration: dict[str, Any] | None) -> str:
        reviews = iteration.get("verification_reviews") if isinstance(iteration, dict) else []
        if not isinstance(reviews, list) or not reviews:
            return "PENDING"
        if any(str(review.get("path_acceptability") or "").lower() == "disqualifying" for review in reviews if isinstance(review, dict)):
            return "DISQUALIFYING"
        if any(str(review.get("path_acceptability") or "").lower() == "acceptable" for review in reviews if isinstance(review, dict)):
            return "ACCEPTABLE"
        return "PENDING"

    def autonomy_summary_payload(
        self,
        app_id: str,
        *,
        source: str,
        fallback_allowed: bool,
    ) -> dict[str, Any]:
        goal = self._pick_relevant_goal(app_id)
        iteration = self._latest_goal_iteration(goal)
        generated_at = (
            str((goal or {}).get("updated_at") or (goal or {}).get("completed_at") or (goal or {}).get("created_at") or "")
            if isinstance(goal, dict)
            else ""
        ) or utc_now()
        if not goal or not iteration:
            return {
                "goal_title": "Autonomy Goal",
                "goal_status": str((goal or {}).get("status") or "unknown") if isinstance(goal, dict) else "unknown",
                "iteration": "",
                "path_verdict": "UNKNOWN",
                "verifier_acceptability": "PENDING",
                "blocker_reason": "stale-or-missing",
                "expected_path": "unknown",
                "degraded_signals": [],
                "heading": "Autonomy summary unavailable.",
                "source": source,
                "generated_at": generated_at,
                "freshness_state": "stale-or-missing",
                "fallback_allowed": fallback_allowed,
            }

        intended_path = iteration.get("intended_path") if isinstance(iteration, dict) else {}
        if not isinstance(intended_path, dict):
            intended_path = {}
        degraded_signals = intended_path.get("degraded_signals")
        return {
            "goal_title": str(goal.get("title") or "Autonomy Goal"),
            "goal_status": str(goal.get("status") or "unknown"),
            "iteration": str(iteration.get("iteration") or ""),
            "path_verdict": "EXPECTED" if str(intended_path.get("verdict") or "").lower() == "expected" else "DEGRADED",
            "verifier_acceptability": self._summarize_verifier_acceptability(iteration),
            "blocker_reason": str(iteration.get("continuation_blocker_reason") or goal.get("stop_reason") or "none"),
            "expected_path": str(intended_path.get("expected_path") or "").strip() or "unknown",
            "degraded_signals": list(degraded_signals) if isinstance(degraded_signals, list) else [],
            "heading": f"{goal.get('title') or 'Autonomy Goal'} · {goal.get('status') or 'unknown'} · iteration {iteration.get('iteration')}",
            "source": source,
            "generated_at": generated_at,
            "freshness_state": "fresh",
            "fallback_allowed": fallback_allowed,
        }

    def conversation_snapshot_payload(
        self,
        conversation_id: str,
        *,
        source: str = "conversation-snapshot",
        fallback_allowed: bool = True,
    ) -> dict[str, Any]:
        conversation = dict(self.require_conversation(conversation_id))
        conversation["autonomy_summary"] = self.autonomy_summary_payload(
            str(conversation.get("app_id") or ""),
            source=source,
            fallback_allowed=fallback_allowed,
        )
        return conversation

    def subscribe_conversation_appends(self, conversation_id: str) -> asyncio.Queue[dict[str, Any]]:
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        self.append_subscribers.setdefault(conversation_id, set()).add(queue)
        return queue

    def unsubscribe_conversation_appends(self, conversation_id: str, queue: asyncio.Queue[dict[str, Any]]) -> None:
        subscribers = self.append_subscribers.get(conversation_id)
        if not subscribers:
            return
        subscribers.discard(queue)
        if not subscribers:
            self.append_subscribers.pop(conversation_id, None)

    def _publish_conversation_append(self, conversation_id: str, *, kind: str, payload: dict[str, Any]) -> None:
        subscribers = self.append_subscribers.get(conversation_id)
        if not subscribers:
            return
        envelope = {
            "conversation_id": conversation_id,
            "kind": kind,
            "append_id": int(payload.get("append_id") or 0),
            "payload": payload,
            "session_phase": self.conversation_session_phase(payload, kind=kind),
        }
        stale: list[asyncio.Queue[dict[str, Any]]] = []
        for queue in subscribers:
            try:
                queue.put_nowait(envelope)
            except RuntimeError:
                stale.append(queue)
        for queue in stale:
            subscribers.discard(queue)
        if not subscribers:
            self.append_subscribers.pop(conversation_id, None)

    def append_event(
        self,
        conversation_id: str,
        *,
        event_type: str,
        body: str,
        status: str = "info",
        job_id: str = "",
        data: dict[str, Any] | None = None,
    ) -> None:
        if not conversation_id:
            return
        event = self.state.append_conversation_event(
            conversation_id,
            event_type=event_type,
            body=body,
            status=status,
            job_id=job_id,
            data=data,
        )
        self._publish_conversation_append(conversation_id, kind="event", payload=event)

    def append_user_message(
        self,
        conversation_id: str,
        *,
        title: str,
        body: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not conversation_id:
            return
        message = self.state.append_conversation_message(
            conversation_id,
            role="user",
            title=title,
            body=body,
            message_type="request",
            metadata=metadata,
        )
        self._publish_conversation_append(conversation_id, kind="message", payload=message)

    def append_assistant_message(
        self,
        conversation_id: str,
        *,
        title: str,
        body: str,
        job_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not conversation_id:
            return
        message = self.state.append_conversation_message(
            conversation_id,
            role="assistant",
            title=title,
            body=body,
            job_id=job_id,
            message_type="result",
            metadata=metadata,
        )
        self._publish_conversation_append(conversation_id, kind="message", payload=message)

    def resolve_conversation_title(self, app_id: str, explicit_title: str) -> str:
        if explicit_title.strip():
            return explicit_title.strip()
        app_record = self.state.get_app(app_id)
        return f"{app_record.get('title') or app_id} Conversation"

    def resolve_request_title(self, explicit_title: str, request_text: str) -> str:
        if explicit_title.strip():
            return explicit_title.strip()
        first_line = next((line.strip() for line in request_text.splitlines() if line.strip()), "")
        compact = " ".join(first_line.split())
        if len(compact) > 72:
            compact = compact[:69].rstrip() + "..."
        return compact or "Conversation update"

    def require_app(self, app_id: str) -> dict[str, Any]:
        try:
            return self.state.get_app(app_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def require_conversation(self, conversation_id: str) -> dict[str, Any]:
        try:
            return self.state.get_conversation(conversation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def get_job_or_404(self, job_id: str) -> dict[str, Any]:
        try:
            return self.state.get_job(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def get_proposal_or_404(self, job_id: str) -> dict[str, Any]:
        try:
            return self.state.get_proposal(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def get_goal_or_404(self, goal_id: str) -> dict[str, Any]:
        try:
            return self.state.get_goal(goal_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def build_health_payload(self) -> dict[str, Any]:
        return {
            "ok": True,
            "repo_root": str(self.settings.repo_root),
            "codex_command": self.settings.codex_command,
            "codex_home": str(self.settings.codex_home) if self.settings.codex_home is not None else "(default ~/.codex)",
            "codex_profile": self.settings.codex_profile,
            "codex_model": self.settings.codex_model or "(default)",
            "auth_providers": self.settings.auth_providers,
            "api_key_required": "api_key" in self.settings.auth_providers,
            "iap_enabled": "iap" in self.settings.auth_providers,
            "allowed_user_emails": self.settings.allowed_user_emails,
        }

    def _save_goal_phase(
        self,
        goal: dict[str, Any],
        *,
        phase: str,
        iteration: int | None = None,
        job_id: str = "",
    ) -> dict[str, Any]:
        goal["current_phase"] = phase
        if iteration is not None:
            goal["current_iteration"] = iteration
        if job_id:
            goal["current_job_id"] = job_id
        elif phase in {"", "proposal", "review"}:
            goal["current_job_id"] = ""
        return self.state.save_goal(goal)

    def _is_retryable_advisory_error(self, message: str) -> bool:
        lowered = str(message or "").lower()
        return "reading additional input from stdin" in lowered or "timed out" in lowered

    async def _run_advisory_phase(
        self,
        *,
        prompt: str,
        cwd: Path,
        output_stem: str,
        conversation_id: str,
        phase_event_prefix: str,
        phase_label: str,
        iteration_number: int,
        data: dict[str, Any],
    ) -> tuple[int, str, str, str]:
        attempts = 3
        last_result: tuple[int, str, str, str] | None = None
        for attempt in range(1, attempts + 1):
            last_result = await self.runtime.run_advisory_prompt(
                prompt=prompt,
                cwd=cwd,
                output_stem=f"{output_stem}-attempt-{attempt}",
            )
            returncode, stdout_text, stderr_text, final_output = last_result
            if returncode == 0:
                return last_result
            error_message = (stderr_text or stdout_text or f"{phase_label} failed.").strip()
            if attempt >= attempts or not self._is_retryable_advisory_error(error_message):
                raise RuntimeError(error_message)
            self.append_event(
                conversation_id,
                event_type=f"{phase_event_prefix}.retrying",
                body=f"{phase_label}에서 일시적 오류가 발생해 재시도합니다. ({attempt}/{attempts}) {error_message}",
                status="running",
                data={**data, "attempt": attempt, "error": error_message},
            )
            await asyncio.sleep(float(attempt))
        raise RuntimeError(f"{phase_label} failed without a result.")

    async def run_autonomy_proposal(
        self,
        *,
        goal: dict[str, Any],
        app_record: dict[str, Any],
        conversation_id: str,
        iteration_number: int,
    ) -> dict[str, str]:
        prompt = self.autonomy.build_proposer_prompt(goal, app_record)
        goal = self._save_goal_phase(goal, phase="proposal", iteration=iteration_number)
        self.append_event(
            conversation_id,
            event_type="goal.proposal.phase.started",
            body=f"iteration {iteration_number}의 bounded hypothesis를 제안합니다.",
            status="planning",
            data={"goal_id": goal.get("goal_id", ""), "iteration": iteration_number},
        )
        returncode, stdout_text, stderr_text, final_output = await self._run_advisory_phase(
            prompt=prompt,
            cwd=self.settings.repo_root,
            output_stem=f"{goal['goal_id']}-iter-{iteration_number}-proposer",
            conversation_id=conversation_id,
            phase_event_prefix="goal.proposal.phase",
            phase_label="proposal phase",
            iteration_number=iteration_number,
            data={"goal_id": goal.get("goal_id", ""), "iteration": iteration_number},
        )
        _, parsed = extract_proposal_json(final_output)
        proposal = normalize_proposal_json(parsed)
        self.append_event(
            conversation_id,
            event_type="goal.proposal.phase.completed",
            body=f"제안 가설: {proposal.get('hypothesis', '')}",
            status="planning",
            data={"goal_id": goal.get("goal_id", ""), "iteration": iteration_number, "proposal": proposal},
        )
        return proposal

    async def run_autonomy_review(
        self,
        *,
        goal: dict[str, Any],
        app_record: dict[str, Any],
        proposal: dict[str, str],
        conversation_id: str,
        iteration_number: int,
        reviewer_name: str,
    ) -> dict[str, str]:
        prompt = self.autonomy.build_reviewer_prompt(goal, app_record, proposal, reviewer_name=reviewer_name)
        goal = self._save_goal_phase(goal, phase="review", iteration=iteration_number)
        slug = reviewer_name.lower().replace(" ", "-")
        self.append_event(
            conversation_id,
            event_type="goal.review.phase.started",
            body=f"{reviewer_name}가 가설을 평가합니다.",
            status="planning",
            data={"goal_id": goal.get("goal_id", ""), "iteration": iteration_number, "reviewer": reviewer_name},
        )
        returncode, stdout_text, stderr_text, final_output = await self._run_advisory_phase(
            prompt=prompt,
            cwd=self.settings.repo_root,
            output_stem=f"{goal['goal_id']}-iter-{iteration_number}-{slug}",
            conversation_id=conversation_id,
            phase_event_prefix="goal.review.phase",
            phase_label=f"{reviewer_name} review phase",
            iteration_number=iteration_number,
            data={"goal_id": goal.get("goal_id", ""), "iteration": iteration_number, "reviewer": reviewer_name},
        )
        _, parsed = extract_review_json(final_output)
        review = normalize_review_json(parsed)
        self.append_event(
            conversation_id,
            event_type="goal.review.phase.completed",
            body=f"{reviewer_name} verdict: {review.get('verdict', 'reject')}",
            status="planning" if review.get("verdict") == "approve" else "paused",
            data={
                "goal_id": goal.get("goal_id", ""),
                "iteration": iteration_number,
                "reviewer": reviewer_name,
                "review": review,
            },
        )
        return review

    async def run_autonomy_verifier(
        self,
        *,
        goal: dict[str, Any],
        app_record: dict[str, Any],
        proposal: dict[str, str],
        implementation_summary: str,
        intended_path: dict[str, Any],
        conversation_id: str,
        iteration_number: int,
        verifier_name: str,
        cwd: Path,
    ) -> dict[str, str]:
        prompt = self.autonomy.build_verifier_prompt(
            goal,
            app_record,
            proposal,
            implementation_summary,
            verifier_name=verifier_name,
            intended_path=intended_path,
        )
        goal = self._save_goal_phase(goal, phase="verify", iteration=iteration_number)
        slug = verifier_name.lower().replace(" ", "-")
        self.append_event(
            conversation_id,
            event_type="goal.verify.phase.started",
            body=f"{verifier_name}가 구현 결과를 검증합니다.",
            status="running",
            data={"goal_id": goal.get("goal_id", ""), "iteration": iteration_number, "verifier": verifier_name},
        )
        returncode, stdout_text, stderr_text, final_output = await self._run_advisory_phase(
            prompt=prompt,
            cwd=cwd,
            output_stem=f"{goal['goal_id']}-iter-{iteration_number}-{slug}",
            conversation_id=conversation_id,
            phase_event_prefix="goal.verify.phase",
            phase_label=f"{verifier_name} verification phase",
            iteration_number=iteration_number,
            data={"goal_id": goal.get("goal_id", ""), "iteration": iteration_number, "verifier": verifier_name},
        )
        _, parsed = extract_verify_json(final_output)
        review = normalize_verify_json(parsed)
        self.append_event(
            conversation_id,
            event_type="goal.verify.phase.completed",
            body=f"{verifier_name} verdict: {review.get('verdict', 'fail')}",
            status="running" if review.get("verdict") == "pass" else "paused",
            data={
                "goal_id": goal.get("goal_id", ""),
                "iteration": iteration_number,
                "verifier": verifier_name,
                "verification_review": review,
            },
        )
        return review

    def spawn_goal_loop(self, goal_id: str) -> None:
        existing = self.goal_tasks.get(goal_id)
        if existing is not None and not existing.done():
            return
        task = asyncio.create_task(self.run_goal_loop(goal_id))
        self.goal_tasks[goal_id] = task
        task.add_done_callback(lambda finished: self._finalize_goal_task(goal_id, finished))

    def _finalize_goal_task(self, goal_id: str, task: asyncio.Task[Any]) -> None:
        self.goal_tasks.pop(goal_id, None)
        self._handle_goal_task_result(goal_id, task)

    def _handle_goal_task_result(self, goal_id: str, task: asyncio.Task[Any]) -> None:
        if task.cancelled():
            return
        exc = task.exception()
        if exc is None:
            return
        try:
            goal = self.state.get_goal(goal_id)
        except KeyError:
            return
        conversation_id = str(goal.get("conversation_id") or "").strip()
        goal["status"] = "paused"
        goal["stop_reason"] = "autonomy_task_exception"
        goal["completed_at"] = utc_now()
        self.state.save_goal(goal)
        self.append_event(
            conversation_id,
            event_type="goal.paused",
            body=f"자율 목표 task 예외로 루프를 일시중지합니다. {exc}",
            status="paused",
            data={"goal_id": goal_id, "stop_reason": goal["stop_reason"], "error": str(exc)},
        )

    def _goal_stop_reason_for_exception(self, phase: str, exc: Exception) -> str:
        message = str(exc).lower()
        if "timed out" in message:
            return f"{phase}_phase_timeout"
        return f"{phase}_phase_failed"

    def _goal_can_explore_alternative(
        self,
        goal: dict[str, Any],
        *,
        iteration_number: int,
        failure_kind: str,
    ) -> bool:
        policy = goal.get("policy") or {}
        if failure_kind == "review":
            allowed = bool(policy.get("continue_on_review_failure", True))
        elif failure_kind == "verification":
            allowed = bool(policy.get("continue_on_verification_failure", True))
        else:
            return False
        return allowed and self.goals.can_continue_after_iteration(goal, iteration_number=iteration_number)

    def _process_exists(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    def reconcile_running_jobs(self) -> None:
        now = datetime.now(timezone.utc)
        for job in self.state.list_jobs(status="running"):
            job_id = str(job.get("job_id") or "").strip()
            conversation_id = str(job.get("conversation_id") or "").strip()
            runner_pid = int(job.get("runner_pid") or 0)
            timestamp = str(job.get("started_at") or job.get("updated_at") or "")
            stale_seconds = 0.0
            if timestamp:
                try:
                    stale_seconds = max(
                        0.0,
                        (now - datetime.fromisoformat(timestamp.replace("Z", "+00:00"))).total_seconds(),
                    )
                except ValueError:
                    stale_seconds = float(self.settings.running_job_grace_seconds + 1)
            process_missing = runner_pid > 0 and not self._process_exists(runner_pid)
            stale_without_pid = runner_pid <= 0 and stale_seconds > float(self.settings.running_job_grace_seconds)
            if not (process_missing or stale_without_pid):
                continue
            reason = (
                f"codex process pid {runner_pid} is no longer running"
                if process_missing
                else f"running job made no progress for {int(stale_seconds)} seconds and has no tracked codex process"
            )
            self.state.update_job(
                job_id,
                status="failed",
                completed_at=utc_now(),
                runner_pid=0,
                error=f"orphaned_running_job: {reason}",
            )
            self.append_event(
                conversation_id,
                event_type="job.failed",
                body=f"job {job_id}를 orphaned running job으로 정리했습니다. {reason}",
                status="failed",
                job_id=job_id,
                data={"error": f"orphaned_running_job: {reason}"},
            )

    def reconcile_running_goals(self) -> None:
        now = datetime.now(timezone.utc)
        for goal in self.state.list_goals():
            if goal.get("status") != "running":
                continue
            if goal.get("halt_requested"):
                continue
            goal_id = str(goal.get("goal_id") or "").strip()
            conversation_id = str(goal.get("conversation_id") or "").strip()
            current_job_id = str(goal.get("current_job_id") or "").strip()
            last_job_id = str(goal.get("last_job_id") or "").strip()
            phase = str(goal.get("current_phase") or "").strip()
            timestamp = str(goal.get("updated_at") or goal.get("last_resumed_at") or goal.get("started_at") or "")
            stale_seconds = 0.0
            if timestamp:
                try:
                    stale_seconds = max(
                        0.0,
                        (now - datetime.fromisoformat(timestamp.replace("Z", "+00:00"))).total_seconds(),
                    )
                except ValueError:
                    stale_seconds = float(self.settings.running_job_grace_seconds + 1)

            active_job_id = current_job_id or last_job_id
            active_job_running = False
            missing_active_job = False
            if active_job_id:
                try:
                    job = self.state.get_job(active_job_id)
                except KeyError:
                    job = {}
                    missing_active_job = True
                runner_pid = int(job.get("runner_pid") or 0)
                if job.get("status") == "running" and runner_pid > 0 and self._process_exists(runner_pid):
                    active_job_running = True

            if active_job_running:
                continue
            if goal.get("awaiting_restart_resume"):
                continue
            if not missing_active_job and stale_seconds <= float(self.settings.running_job_grace_seconds):
                continue

            reason = (
                f"running goal references missing current_job_id={active_job_id}"
                if missing_active_job
                else (
                    f"running goal made no progress for {int(stale_seconds)} seconds"
                    f" and has no live codex process for current_job_id={current_job_id or '(none)'}"
                )
            )
            goal["status"] = "paused"
            goal["stop_reason"] = "stale_running_goal"
            goal["completed_at"] = utc_now()
            goal["current_phase"] = ""
            goal["current_job_id"] = ""
            self.state.save_goal(goal)
            self.append_event(
                conversation_id,
                event_type="goal.paused",
                body=f"자율 목표 {goal_id}를 stale running goal로 정리했습니다. {reason}",
                status="paused",
                data={"goal_id": goal_id, "stop_reason": "stale_running_goal", "reason": reason},
            )

    def resume_running_goals(self) -> None:
        for goal in self.state.list_goals():
            if goal.get("status") != "running":
                continue
            if goal.get("halt_requested"):
                continue
            conversation_id = str(goal.get("conversation_id") or "").strip()
            resume_reason = "restart_resume" if goal.get("awaiting_restart_resume") else "startup_recovery"
            iteration = int(goal.get("awaiting_restart_iteration") or 0)
            goal["last_resume_reason"] = resume_reason
            goal["last_resumed_at"] = utc_now()
            goal["current_phase"] = "restart_resume" if goal.get("awaiting_restart_resume") else (goal.get("current_phase") or "proposal")
            if goal.get("awaiting_restart_resume"):
                goal["awaiting_restart_resume"] = False
                goal["awaiting_restart_iteration"] = 0
                goal["awaiting_restart_job_id"] = ""
            self.state.save_goal(goal)
            self.append_event(
                conversation_id,
                event_type="goal.resumed",
                body=(
                    "서비스 재시작 뒤 대기 중이던 자율 목표 루프를 다시 붙였습니다."
                    if resume_reason == "restart_resume"
                    else "서버 시작 후 실행 중이던 자율 목표 루프를 다시 붙였습니다."
                ),
                status="running",
                data={
                    "goal_id": goal.get("goal_id", ""),
                    "resume_reason": resume_reason,
                    "iteration": iteration,
                },
            )
            self.spawn_goal_loop(str(goal["goal_id"]))

    def interpret_intent(
        self,
        *,
        app_id: str,
        title: str,
        request_text: str,
        source: str,
        conversation_id: str = "",
    ) -> dict[str, str]:
        record = self.require_app(app_id)
        return infer_intent_summary(
            record,
            {
                "title": title,
                "request_text": request_text,
                "source": source,
                "conversation_id": conversation_id,
            },
        )

    def enqueue_request(
        self,
        *,
        app_id: str,
        title: str,
        request_text: str,
        source: str,
        execute_now: bool,
        background_tasks: BackgroundTasks,
        conversation_id: str = "",
        intent_summary: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        resolved_title = self.resolve_request_title(title, request_text)
        resolved_intent = intent_summary or self.interpret_intent(
            app_id=app_id,
            title=resolved_title,
            request_text=request_text,
            source=source,
            conversation_id=conversation_id,
        )
        request_payload = self.state.create_request(
            app_id=app_id,
            title=resolved_title,
            request_text=request_text,
            source=source,
            conversation_id=conversation_id,
            intent_summary=resolved_intent,
        )
        job = self.state.create_job(
            app_id=app_id,
            request_id=request_payload["request_id"],
            title=resolved_title,
            conversation_id=conversation_id,
            intent_summary=resolved_intent,
        )
        self.append_event(
            conversation_id,
            event_type="intent.interpreted",
            status="intent",
            body="사용자 요청을 실행 가능한 의도로 해석했습니다.",
            job_id=job["job_id"],
            data=resolved_intent,
        )
        self.append_event(
            conversation_id,
            event_type="job.queued",
            status="queued",
            body=f"요청이 접수되어 job {job['job_id']}를 만들었습니다.",
            job_id=job["job_id"],
            data={
                "title": resolved_title,
                "request_id": request_payload["request_id"],
                "intent_summary": resolved_intent,
            },
        )
        if execute_now and self.settings.auto_execute_requests:
            runtime_request = dict(request_payload)
            background_tasks.add_task(self.run_job, job["job_id"], app_id, runtime_request)
        return {
            "request": request_payload,
            "job": job,
            "execute_now": bool(execute_now and self.settings.auto_execute_requests),
        }

    async def run_job(self, job_id: str, app_id: str, request_payload: dict[str, Any]) -> None:
        conversation_id = str(request_payload.get("conversation_id") or "").strip()
        self.append_event(
            conversation_id,
            event_type="job.running",
            status="running",
            body=f"job {job_id}가 실행을 시작했습니다.",
            job_id=job_id,
            data={"title": request_payload.get("title", "")},
        )
        try:
            await self.runtime.run_request(
                app_id,
                job_id,
                request_payload,
                event_callback=lambda **event: self.append_event(conversation_id, **event),
            )
        except Exception as exc:  # noqa: BLE001
            self.state.update_job(
                job_id,
                status="failed",
                completed_at=utc_now(),
                error=str(exc),
            )

        job = self.state.get_job(job_id)
        if job["status"] == "completed":
            self.append_event(
                conversation_id,
                event_type="job.completed",
                status="completed",
                body=f"job {job_id}가 완료되었습니다.",
                job_id=job_id,
                data={"summary": job.get("result_summary", "")},
            )
            self.append_assistant_message(
                conversation_id,
                title=job.get("title") or "작업 결과",
                body=job.get("result_summary") or "작업이 완료되었습니다.",
                job_id=job_id,
                metadata={
                    "decision_summary": job.get("decision_summary") or {},
                    "status": job.get("status"),
                },
            )
            if job.get("proposal"):
                self.append_event(
                    conversation_id,
                    event_type="proposal.ready",
                    status="proposal",
                    body=f"proposal branch {job['proposal']['branch_name']}가 준비되었습니다.",
                    job_id=job_id,
                    data=job["proposal"],
                )
            return

        self.append_event(
            conversation_id,
            event_type="job.failed",
            status="failed",
            body=f"job {job_id}가 실패했습니다. {job.get('error', '')}".strip(),
            job_id=job_id,
            data={"error": job.get("error", "")},
        )
        self.append_assistant_message(
            conversation_id,
            title=job.get("title") or "작업 실패",
            body=job.get("error") or "작업이 실패했습니다.",
            job_id=job_id,
            metadata={
                "decision_summary": job.get("decision_summary") or {},
                "status": job.get("status"),
            },
        )

    async def apply_proposal(self, job_id: str) -> dict[str, Any]:
        try:
            proposal = await self.runtime.apply_proposal(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

        job = self.state.get_job(job_id)
        conversation_id = str(job.get("conversation_id") or "").strip()
        self.append_event(
            conversation_id,
            event_type="proposal.applied",
            status="applied",
            body=f"proposal {job_id}가 적용되었습니다.",
            job_id=job_id,
            data={"branch_name": proposal.get("branch_name", ""), "head_commit": proposal.get("head_commit", "")},
        )
        self.append_assistant_message(
            conversation_id,
            title=f"Proposal applied · {proposal.get('title') or job_id}",
            body=proposal.get("push_message") or proposal.get("result_summary") or "proposal이 적용되었습니다.",
            job_id=job_id,
            metadata={
                "decision_summary": proposal.get("decision_summary") or {},
                "status": proposal.get("status"),
            },
        )
        return proposal

    def create_goal(
        self,
        *,
        app_id: str,
        title: str,
        objective: str,
        source: str,
        max_iterations: int,
        autostart: bool,
        auto_apply_proposals: bool,
        auto_resume_after_apply: bool,
    ) -> dict[str, Any]:
        app_record = self.require_app(app_id)
        conversation = self.state.create_conversation(
            app_id=app_id,
            title=self.resolve_conversation_title(app_id, title or objective),
            source=source,
        )
        self.append_event(
            conversation["conversation_id"],
            event_type="conversation.created",
            body="자율 목표 대화 세션이 시작되었습니다.",
            status="created",
            data={"app_id": app_id, "autonomous": True},
        )
        goal = self.state.create_goal(
            app_id=app_id,
            title=self.goals.resolve_goal_title(str(app_record.get("title") or app_id), title, objective),
            objective=objective,
            source=source,
            conversation_id=conversation["conversation_id"],
            max_iterations=max_iterations,
            auto_apply_proposals=auto_apply_proposals,
            auto_resume_after_apply=auto_resume_after_apply,
        )
        self.append_event(
            conversation["conversation_id"],
            event_type="goal.created",
            body="자율 개선 목표가 등록되었습니다.",
            status="created",
            data={
                "goal_id": goal["goal_id"],
                "max_iterations": max_iterations,
                "open_ended": max_iterations == 0,
                "auto_apply_proposals": auto_apply_proposals,
                "auto_resume_after_apply": auto_resume_after_apply,
            },
        )
        if autostart:
            goal["status"] = "running"
            goal["started_at"] = utc_now()
            goal["current_phase"] = "proposal"
            self.state.save_goal(goal)
            self.spawn_goal_loop(goal["goal_id"])
        return {"goal": self.state.get_goal(goal["goal_id"]), "conversation": conversation, "autostart": autostart}

    def halt_goal(self, goal_id: str) -> dict[str, Any]:
        goal = self.get_goal_or_404(goal_id)
        goal["halt_requested"] = True
        if goal.get("status") == "queued":
            goal["status"] = "stopped"
            goal["stop_reason"] = "halt_requested_before_start"
            goal["completed_at"] = utc_now()
        self.state.save_goal(goal)
        self.append_event(
            str(goal.get("conversation_id") or "").strip(),
            event_type="goal.halt_requested",
            body="자율 목표 중지가 요청되었습니다.",
            status="halted",
            data={"goal_id": goal_id},
        )
        return goal

    def start_goal(self, goal_id: str) -> dict[str, Any]:
        goal = self.get_goal_or_404(goal_id)
        if goal.get("status") == "running":
            raise HTTPException(status_code=409, detail="Goal is already running.")
        if goal.get("status") in {"completed", "failed", "stopped"} and not goal.get("halt_requested"):
            goal["status"] = "running"
        else:
            goal["status"] = "running"
        goal["halt_requested"] = False
        if not goal.get("started_at"):
            goal["started_at"] = utc_now()
        goal["completed_at"] = ""
        goal["stop_reason"] = ""
        goal["current_phase"] = "proposal"
        goal["current_job_id"] = ""
        self.state.save_goal(goal)
        self.spawn_goal_loop(goal_id)
        return goal

    async def run_goal_loop(self, goal_id: str) -> None:
        while True:
            goal = self.state.get_goal(goal_id)
            conversation_id = str(goal.get("conversation_id") or "").strip()
            if goal.get("halt_requested"):
                goal["status"] = "stopped"
                goal["stop_reason"] = "halt_requested"
                goal["completed_at"] = utc_now()
                goal["current_phase"] = ""
                goal["current_job_id"] = ""
                self.state.save_goal(goal)
                self.append_event(
                    conversation_id,
                    event_type="goal.stopped",
                    body="자율 목표 루프가 중지 요청으로 종료되었습니다.",
                    status="stopped",
                    data={"goal_id": goal_id, "stop_reason": goal["stop_reason"]},
                )
                return
            if goal.get("status") != "running":
                return

            app_id = str(goal["app_id"])
            app_record = self.require_app(app_id)
            iteration_number = int(goal.get("current_iteration") or 0) + 1
            current_phase = "proposal"
            try:
                proposal_plan = await self.run_autonomy_proposal(
                    goal=goal,
                    app_record=app_record,
                    conversation_id=conversation_id,
                    iteration_number=iteration_number,
                )
                current_phase = "review"
                proposal_reviews = [
                    await self.run_autonomy_review(
                        goal=goal,
                        app_record=app_record,
                        proposal=proposal_plan,
                        conversation_id=conversation_id,
                        iteration_number=iteration_number,
                        reviewer_name=reviewer_name,
                    )
                    for reviewer_name in ("Reviewer A", "Reviewer B")
                ]
            except Exception as exc:  # noqa: BLE001
                goal = self.state.get_goal(goal_id)
                goal["status"] = "paused"
                goal["stop_reason"] = self._goal_stop_reason_for_exception(current_phase, exc)
                goal["completed_at"] = utc_now()
                goal["current_phase"] = ""
                goal["current_job_id"] = ""
                self.state.save_goal(goal)
                self.append_event(
                    conversation_id,
                    event_type="goal.paused",
                    body=f"자율 목표가 {current_phase} 단계에서 중지되었습니다. {exc}",
                    status="paused",
                    data={"goal_id": goal_id, "iteration": iteration_number, "stop_reason": goal["stop_reason"], "error": str(exc)},
                )
                return
            if any(review.get("verdict") != "approve" for review in proposal_reviews):
                iteration_record = {
                    "iteration": iteration_number,
                    "status": "rejected_before_implementation",
                    "proposal_plan": proposal_plan,
                    "proposal_reviews": proposal_reviews,
                    "continuation_blocker_reason": "proposal_not_approved",
                    "completed_at": utc_now(),
                }
                iterations = goal.get("iterations") or []
                iterations.append(iteration_record)
                goal["iterations"] = iterations
                goal["current_iteration"] = iteration_number
                should_continue = self._goal_can_explore_alternative(goal, iteration_number=iteration_number, failure_kind="review")
                goal["status"] = "running" if should_continue else "paused"
                goal["stop_reason"] = "" if should_continue else "proposal_not_approved"
                goal["completed_at"] = "" if should_continue else utc_now()
                goal["current_phase"] = "proposal" if should_continue else ""
                goal["current_job_id"] = ""
                self.state.save_goal(goal)
                self.append_event(
                    conversation_id,
                    event_type="goal.iteration.rejected" if should_continue else "goal.paused",
                    body=(
                        "두 reviewer의 승인을 모두 받지 못해 다른 bounded hypothesis를 탐색합니다."
                        if should_continue
                        else "두 reviewer의 승인을 모두 받지 못해 iteration을 중지합니다."
                    ),
                    status="running" if should_continue else "paused",
                    data={
                        "goal_id": goal_id,
                        "iteration": iteration_number,
                        "proposal_plan": proposal_plan,
                        "proposal_reviews": proposal_reviews,
                    },
                )
                if should_continue:
                    continue
                return

            title, request_text = self.autonomy.build_implementation_request(
                goal,
                app_record,
                proposal_plan,
                iteration_number=iteration_number,
            )
            intent_summary = self.interpret_intent(
                app_id=app_id,
                title=title,
                request_text=request_text,
                source="goal-loop",
                conversation_id=conversation_id,
            )
            self.state.append_conversation_message(
                conversation_id,
                role="user",
                title=title,
                body=request_text,
                message_type="request",
                metadata={
                    "source": "goal-loop",
                    "goal_id": goal_id,
                    "autonomous": True,
                    "iteration": iteration_number,
                    "intent_summary": intent_summary,
                },
            )
            self.append_event(
                conversation_id,
                event_type="goal.iteration.started",
                body=f"자율 목표 iteration {iteration_number}를 시작합니다.",
                status="running",
                data={"goal_id": goal_id, "iteration": iteration_number},
            )
            payload = self.enqueue_request(
                app_id=app_id,
                title=title,
                request_text=request_text,
                source="goal-loop",
                execute_now=False,
                background_tasks=BackgroundTasks(),
                conversation_id=conversation_id,
                intent_summary=intent_summary,
            )
            request_payload = {
                **payload["request"],
                "goal_loop": {
                    "goal_id": goal_id,
                    "iteration": iteration_number,
                    "open_ended": int(goal.get("max_iterations") or 0) == 0,
                },
            }
            goal = self.state.get_goal(goal_id)
            goal["current_iteration"] = iteration_number
            goal["current_phase"] = "implementation"
            goal["current_job_id"] = payload["job"]["job_id"]
            goal["last_job_id"] = payload["job"]["job_id"]
            self.state.save_goal(goal)
            await self.run_job(payload["job"]["job_id"], app_id, request_payload)
            job = self.state.get_job(payload["job"]["job_id"])
            goal = self.state.get_goal(goal_id)
            conversation_state = self.state.get_conversation(conversation_id)
            intended_path = self.goals.assess_iteration_intended_path(
                job=job,
                conversation=conversation_state,
                proposal_ready=bool(job.get("proposal")),
            )
            iteration_record = {
                "iteration": iteration_number,
                "request_id": payload["request"]["request_id"],
                "job_id": payload["job"]["job_id"],
                "status": job.get("status"),
                "proposal_plan": proposal_plan,
                "proposal_reviews": proposal_reviews,
                "result_summary": job.get("result_summary", ""),
                "decision_summary": job.get("decision_summary", {}),
                "goal_review": job.get("goal_review", {}),
                "intended_path": intended_path,
                "continuation_blocker_reason": self.goals.continuation_blocker_reason(
                    job,
                    proposal_ready=bool(job.get("proposal")),
                    intended_path=intended_path,
                    verification_reviews=[],
                ),
                "completed_at": job.get("completed_at", ""),
            }
            iterations = goal.get("iterations") or []
            iterations.append(iteration_record)
            goal["iterations"] = iterations
            goal["current_iteration"] = iteration_number
            goal["last_job_id"] = payload["job"]["job_id"]
            if job.get("result_summary"):
                goal["best_job_id"] = payload["job"]["job_id"]
                goal["best_summary"] = job.get("result_summary", "")
            self.state.save_goal(goal)

            proposal_auto_applied = False
            if job.get("proposal") and bool((goal.get("policy") or {}).get("auto_apply_proposals")):
                verifier_reviews = []
                try:
                    proposal_state = self.state.get_proposal(payload["job"]["job_id"])
                    verify_cwd = Path(str(proposal_state["worktree_path"]))
                    verifier_reviews = [
                        await self.run_autonomy_verifier(
                            goal=goal,
                            app_record=app_record,
                            proposal=proposal_plan,
                            implementation_summary=str(job.get("result_summary") or ""),
                            intended_path=goal["iterations"][-1].get("intended_path", {}),
                            conversation_id=conversation_id,
                            iteration_number=iteration_number,
                            verifier_name=verifier_name,
                            cwd=verify_cwd,
                        )
                        for verifier_name in ("Verifier A", "Verifier B")
                    ]
                except Exception as exc:  # noqa: BLE001
                    goal["iterations"][-1]["verification_reviews"] = verifier_reviews
                    goal["iterations"][-1]["continuation_blocker_reason"] = "verification_failed"
                    should_continue = self._goal_can_explore_alternative(goal, iteration_number=iteration_number, failure_kind="verification")
                    goal["status"] = "running" if should_continue else "paused"
                    goal["stop_reason"] = "" if should_continue else goal["iterations"][-1]["continuation_blocker_reason"]
                    goal["completed_at"] = "" if should_continue else utc_now()
                    goal["current_phase"] = "proposal" if should_continue else ""
                    goal["current_job_id"] = ""
                    self.state.save_goal(goal)
                    self.append_event(
                        conversation_id,
                        event_type="goal.iteration.verification_failed" if should_continue else "goal.paused",
                        body=(
                            f"자동 verification 단계가 실패해 다른 bounded hypothesis를 탐색합니다. {exc}"
                            if should_continue
                            else f"자동 verification 단계에서 실패해 자율 목표를 일시중지합니다. {exc}"
                        ),
                        status="running" if should_continue else "paused",
                        job_id=payload["job"]["job_id"],
                        data={"goal_id": goal_id, "iteration": iteration_number, "stop_reason": goal["stop_reason"]},
                    )
                    if should_continue:
                        continue
                    return

                goal["iterations"][-1]["verification_reviews"] = verifier_reviews
                goal["iterations"][-1]["continuation_blocker_reason"] = self.goals.continuation_blocker_reason(
                    job,
                    proposal_ready=bool(job.get("proposal")),
                    intended_path=goal["iterations"][-1].get("intended_path", {}),
                    verification_reviews=verifier_reviews,
                )
                if any(review.get("verdict") != "pass" for review in verifier_reviews):
                    should_continue = self._goal_can_explore_alternative(goal, iteration_number=iteration_number, failure_kind="verification")
                    goal["status"] = "running" if should_continue else "paused"
                    goal["stop_reason"] = (
                        ""
                        if should_continue
                        else (
                            goal["iterations"][-1].get("continuation_blocker_reason")
                            if goal["iterations"][-1].get("continuation_blocker_reason") not in {"", "none"}
                            else "verification_not_approved"
                        )
                    )
                    goal["completed_at"] = "" if should_continue else utc_now()
                    goal["current_phase"] = "proposal" if should_continue else ""
                    goal["current_job_id"] = ""
                    self.state.save_goal(goal)
                    self.append_event(
                        conversation_id,
                        event_type="goal.iteration.verification_rejected" if should_continue else "goal.paused",
                        body=(
                            "두 verifier의 통과를 모두 얻지 못해 다른 bounded hypothesis를 탐색합니다."
                            if should_continue
                            else "두 verifier의 통과를 모두 얻지 못해 proposal 자동 적용을 중단합니다."
                        ),
                        status="running" if should_continue else "paused",
                        job_id=payload["job"]["job_id"],
                        data={
                            "goal_id": goal_id,
                            "iteration": iteration_number,
                            "verification_reviews": verifier_reviews,
                        },
                    )
                    if should_continue:
                        continue
                    return

                self.append_event(
                    conversation_id,
                    event_type="goal.proposal.auto_apply.started",
                    body="자율 목표 정책에 따라 proposal을 자동 적용합니다.",
                    status="proposal",
                    job_id=payload["job"]["job_id"],
                    data={"goal_id": goal_id, "iteration": iteration_number},
                )
                try:
                    proposal = await self.apply_proposal(payload["job"]["job_id"])
                except HTTPException as exc:
                    goal["status"] = "paused"
                    goal["stop_reason"] = "auto_apply_failed"
                    goal["completed_at"] = utc_now()
                    goal["current_phase"] = ""
                    goal["current_job_id"] = ""
                    self.state.save_goal(goal)
                    self.append_event(
                        conversation_id,
                        event_type="goal.paused",
                        body=f"proposal 자동 적용에 실패해 자율 목표를 일시중지합니다. {exc.detail}",
                        status="paused",
                        job_id=payload["job"]["job_id"],
                        data={"goal_id": goal_id, "iteration": iteration_number, "stop_reason": goal["stop_reason"]},
                    )
                    return

                proposal_auto_applied = True
                iteration_record["proposal_status"] = str(proposal.get("status") or "")
                iteration_record["auto_applied"] = True
                iteration_record["push_status"] = str(proposal.get("push_status") or "")
                iteration_record["verification_reviews"] = goal["iterations"][-1].get("verification_reviews", [])
                conversation_state = self.state.get_conversation(conversation_id)
                iteration_record["intended_path"] = self.goals.assess_iteration_intended_path(
                    job=job,
                    conversation=conversation_state,
                    proposal=proposal,
                    proposal_auto_applied=True,
                    push_required=bool(self.settings.push_after_apply),
                )
                iteration_record["continuation_blocker_reason"] = self.goals.continuation_blocker_reason(
                    job,
                    proposal_ready=False,
                    intended_path=iteration_record["intended_path"],
                    verification_reviews=iteration_record["verification_reviews"],
                )
                goal["iterations"][-1] = iteration_record
                healthy_apply, degraded_reason = self.goals.auto_apply_health(
                    proposal,
                    push_required=bool(self.settings.push_after_apply),
                )
                self.state.save_goal(goal)
                if not healthy_apply:
                    iteration_record["degraded_apply_reason"] = degraded_reason
                    goal["iterations"][-1] = iteration_record
                    goal["status"] = "paused"
                    goal["stop_reason"] = iteration_record.get("continuation_blocker_reason") or "intended_path_degraded"
                    goal["completed_at"] = utc_now()
                    self.state.save_goal(goal)
                    self.append_event(
                        conversation_id,
                        event_type="goal.proposal.auto_apply.degraded",
                        body="proposal 자동 적용이 degraded path로 끝나 자율 목표를 일시중지합니다.",
                        status="paused",
                        job_id=payload["job"]["job_id"],
                        data={
                            "goal_id": goal_id,
                            "iteration": iteration_number,
                            "proposal_status": proposal.get("status", ""),
                            "push_status": proposal.get("push_status", ""),
                            "stop_reason": goal["stop_reason"],
                            "degraded_apply_reason": degraded_reason,
                        },
                    )
                    return
                self.append_event(
                    conversation_id,
                    event_type="goal.proposal.auto_apply.completed",
                    body="proposal을 자동 적용했고, 자율 목표를 계속 진행할 수 있습니다.",
                    status="applied",
                    job_id=payload["job"]["job_id"],
                    data={
                        "goal_id": goal_id,
                        "iteration": iteration_number,
                        "proposal_status": proposal.get("status", ""),
                        "push_status": proposal.get("push_status", ""),
                    },
                )
            next_status, stop_reason = self.goals.next_goal_status(
                goal,
                job,
                proposal_ready=bool(job.get("proposal")) and not proposal_auto_applied,
                intended_path=goal["iterations"][-1].get("intended_path", {}),
                verification_reviews=goal["iterations"][-1].get("verification_reviews", []),
            )
            if (
                proposal_auto_applied
                and next_status == "running"
                and str(proposal.get("restart_service") or "").strip()
                and bool((goal.get("policy") or {}).get("auto_resume_after_apply"))
            ):
                goal["status"] = "running"
                goal["stop_reason"] = ""
                goal["completed_at"] = ""
                goal["current_phase"] = "restart_resume"
                goal["current_job_id"] = ""
                goal["awaiting_restart_resume"] = True
                goal["awaiting_restart_iteration"] = iteration_number
                goal["awaiting_restart_job_id"] = payload["job"]["job_id"]
                self.state.save_goal(goal)
                self.append_event(
                    conversation_id,
                    event_type="goal.awaiting_restart_resume",
                    body="서비스 재시작 후 자율 목표 루프를 자동으로 다시 시작합니다.",
                    status="running",
                    job_id=payload["job"]["job_id"],
                    data={
                        "goal_id": goal_id,
                        "iteration": iteration_number,
                        "resume_reason": "restart_resume",
                    },
                )
                return
            goal["status"] = next_status
            goal["stop_reason"] = stop_reason
            goal["current_phase"] = "proposal" if next_status == "running" else ""
            goal["current_job_id"] = ""
            if next_status in {"completed", "failed", "paused", "stopped"}:
                goal["completed_at"] = utc_now()
            self.state.save_goal(goal)
            self.append_event(
                conversation_id,
                event_type="goal.iteration.finished",
                body=f"자율 목표 iteration {iteration_number}가 {job.get('status')} 상태로 끝났습니다.",
                status=job.get("status") or "info",
                job_id=payload["job"]["job_id"],
                data={
                    "goal_id": goal_id,
                    "iteration": iteration_number,
                    "next_status": next_status,
                    "stop_reason": stop_reason,
                    "continuation_blocker_reason": goal["iterations"][-1].get("continuation_blocker_reason", "none"),
                    "goal_review": job.get("goal_review", {}),
                    "intended_path": goal["iterations"][-1].get("intended_path", {}),
                },
            )
            if next_status != "running":
                self.append_event(
                    conversation_id,
                    event_type=f"goal.{next_status}",
                    body=f"자율 목표 루프가 {next_status} 상태로 전환되었습니다.",
                    status=next_status,
                    data={"goal_id": goal_id, "stop_reason": stop_reason},
                )
                return
