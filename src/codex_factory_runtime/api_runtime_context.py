from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import asyncio

from fastapi import BackgroundTasks, HTTPException, UploadFile

from .agent_runtime import CodexAgentsRuntime
from .config import RuntimeSettings
from .runtime_engineering import infer_intent_summary
from .runtime_goals import GoalRuntime
from .state import RuntimeState, utc_now


@dataclass(slots=True)
class RuntimeApiContext:
    settings: RuntimeSettings
    state: RuntimeState
    runtime: CodexAgentsRuntime
    goals: GoalRuntime

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
        self.state.append_conversation_event(
            conversation_id,
            event_type=event_type,
            body=body,
            status=status,
            job_id=job_id,
            data=data,
        )

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
        self.state.append_conversation_message(
            conversation_id,
            role="assistant",
            title=title,
            body=body,
            job_id=job_id,
            message_type="result",
            metadata=metadata,
        )

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

    async def store_conversation_attachments(
        self,
        conversation_id: str,
        files: list[UploadFile],
    ) -> list[dict[str, Any]]:
        if not files:
            raise HTTPException(status_code=400, detail="At least one image attachment is required.")
        stored: list[dict[str, Any]] = []
        for upload in files:
            content_type = str(upload.content_type or "").strip().lower()
            if not content_type.startswith("image/"):
                raise HTTPException(
                    status_code=415,
                    detail=f"Only image attachments are supported. Got: {content_type or '(none)'}",
                )
            content = await upload.read()
            if not content:
                raise HTTPException(status_code=400, detail=f"Attachment {upload.filename or '(unnamed)'} is empty.")
            metadata = self.state.save_conversation_attachment(
                conversation_id,
                filename=upload.filename or "",
                content_type=content_type,
                content=content,
            )
            stored.append(self.state.public_attachment_ref(metadata))

        self.append_event(
            conversation_id,
            event_type="attachment.saved",
            body=f"스크린샷 {len(stored)}개를 대화 맥락에 저장했습니다.",
            status="info",
            data={"attachments": stored},
        )
        return stored

    def resolve_attachment_inputs(
        self,
        conversation_id: str,
        attachments: list[dict[str, Any]] | None,
    ) -> tuple[list[dict[str, Any]], list[str]]:
        public_refs: list[dict[str, Any]] = []
        image_paths: list[str] = []
        for item in attachments or []:
            attachment_id = str(item.get("attachment_id") or "").strip()
            if not attachment_id:
                continue
            try:
                metadata = self.state.get_conversation_attachment(conversation_id, attachment_id)
            except KeyError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc
            public_refs.append(self.state.public_attachment_ref(metadata))
            image_paths.append(str(metadata["stored_path"]))
        return public_refs, image_paths

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

    def spawn_goal_loop(self, goal_id: str) -> None:
        asyncio.create_task(self.run_goal_loop(goal_id))

    def resume_running_goals(self) -> None:
        for goal in self.state.list_goals():
            if goal.get("status") != "running":
                continue
            if goal.get("halt_requested"):
                continue
            conversation_id = str(goal.get("conversation_id") or "").strip()
            self.append_event(
                conversation_id,
                event_type="goal.resumed",
                body="서버 시작 후 실행 중이던 자율 목표 루프를 다시 붙였습니다.",
                status="running",
                data={"goal_id": goal.get("goal_id", "")},
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
        ux_context: dict[str, Any] | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> dict[str, str]:
        record = self.require_app(app_id)
        return infer_intent_summary(
            record,
            {
                "title": title,
                "request_text": request_text,
                "source": source,
                "conversation_id": conversation_id,
                "ux_context": ux_context or {},
                "attachments": attachments or [],
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
        ux_context: dict[str, Any] | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        if attachments and not conversation_id:
            raise HTTPException(status_code=409, detail="Screenshot attachments require a conversation_id.")
        resolved_title = self.resolve_request_title(title, request_text)
        public_attachments, attachment_paths = self.resolve_attachment_inputs(conversation_id, attachments)
        resolved_intent = intent_summary or self.interpret_intent(
            app_id=app_id,
            title=resolved_title,
            request_text=request_text,
            source=source,
            conversation_id=conversation_id,
            ux_context=ux_context,
            attachments=public_attachments,
        )
        request_payload = self.state.create_request(
            app_id=app_id,
            title=resolved_title,
            request_text=request_text,
            source=source,
            conversation_id=conversation_id,
            intent_summary=resolved_intent,
            ux_context=ux_context,
            attachments=public_attachments,
        )
        job = self.state.create_job(
            app_id=app_id,
            request_id=request_payload["request_id"],
            title=resolved_title,
            conversation_id=conversation_id,
            intent_summary=resolved_intent,
            ux_context=ux_context,
            attachments=public_attachments,
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
                "attachments": public_attachments,
            },
        )
        if execute_now and self.settings.auto_execute_requests:
            runtime_request = dict(request_payload)
            runtime_request["attachment_paths"] = attachment_paths
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
                    "ux_review": job.get("ux_review") or {},
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
                "ux_review": job.get("ux_review") or {},
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
                "ux_review": proposal.get("ux_review") or {},
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
            title, request_text = self.goals.build_iteration_request(goal, app_record)
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
            await self.run_job(payload["job"]["job_id"], app_id, request_payload)
            job = self.state.get_job(payload["job"]["job_id"])
            goal = self.state.get_goal(goal_id)
            iteration_record = {
                "iteration": iteration_number,
                "request_id": payload["request"]["request_id"],
                "job_id": payload["job"]["job_id"],
                "status": job.get("status"),
                "result_summary": job.get("result_summary", ""),
                "decision_summary": job.get("decision_summary", {}),
                "goal_review": job.get("goal_review", {}),
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
                goal["iterations"][-1] = iteration_record
                self.state.save_goal(goal)
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
                if str(proposal.get("restart_service") or "").strip() and bool(
                    (goal.get("policy") or {}).get("auto_resume_after_apply")
                ):
                    goal["status"] = "running"
                    goal["stop_reason"] = ""
                    goal["completed_at"] = ""
                    self.state.save_goal(goal)
                    self.append_event(
                        conversation_id,
                        event_type="goal.awaiting_restart_resume",
                        body="서비스 재시작 후 자율 목표 루프를 자동으로 다시 시작합니다.",
                        status="running",
                        job_id=payload["job"]["job_id"],
                        data={"goal_id": goal_id, "iteration": iteration_number},
                    )
                    return

            next_status, stop_reason = self.goals.next_goal_status(
                goal,
                job,
                proposal_ready=bool(job.get("proposal")) and not proposal_auto_applied,
            )
            goal["status"] = next_status
            goal["stop_reason"] = stop_reason
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
                    "goal_review": job.get("goal_review", {}),
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
