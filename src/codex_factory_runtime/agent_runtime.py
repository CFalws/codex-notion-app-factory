from __future__ import annotations

from typing import Any

from .config import RuntimeSettings
from .runtime_cli import CodexCliRunner
from .runtime_engineering import (
    build_failure_message,
    build_prompt,
    default_decision_summary,
    extract_engineering_log_json,
    extract_goal_review_json,
    extract_ux_review_json,
    normalize_decision_summary,
    normalize_goal_review,
    normalize_ux_review,
    sanitize_user_facing_text,
)
from .runtime_proposals import ProposalRuntime
from .state import RuntimeState, utc_now


class CodexAgentsRuntime:
    def __init__(self, settings: RuntimeSettings, state: RuntimeState) -> None:
        self.settings = settings
        self.state = state
        self.cli = CodexCliRunner(settings)
        self.proposals = ProposalRuntime(settings, state, self.cli)

    def _append_engineering_log(
        self,
        *,
        app_id: str,
        title: str,
        job_id: str,
        request_id: str,
        decision_summary: dict[str, str],
    ) -> None:
        self.state.append_engineering_log(
            app_id=app_id,
            title=title,
            job_id=job_id,
            request_id=request_id,
            summary=decision_summary,
        )

    def _emit_event(
        self,
        event_callback,
        *,
        event_type: str,
        body: str,
        status: str = "info",
        job_id: str = "",
        data: dict[str, Any] | None = None,
    ) -> None:
        if event_callback is None:
            return
        event_callback(
            event_type=event_type,
            body=body,
            status=status,
            job_id=job_id,
            data=data,
        )

    async def run_request(
        self,
        app_id: str,
        job_id: str,
        request_payload: dict[str, Any],
        *,
        event_callback=None,
    ) -> dict[str, Any]:
        record = self.state.get_app(app_id)
        if not self.settings.codex_command:
            decision_summary = default_decision_summary(
                request_payload,
                error_message="CODEX_COMMAND is not configured.",
                decision="Runtime could not start Codex.",
                why="The runtime requires a configured Codex CLI command before executing jobs.",
                verification="job failed before execution",
                follow_up="Set CODEX_COMMAND and retry the request.",
            )
            self._append_engineering_log(
                app_id=app_id,
                title=request_payload["title"],
                job_id=job_id,
                request_id=request_payload["request_id"],
                decision_summary=decision_summary,
            )
            return self.state.update_job(
                job_id,
                status="failed",
                completed_at=utc_now(),
                error="CODEX_COMMAND is not configured.",
                decision_summary=decision_summary,
            )

        session_id = str(record.get("session_id", "")).strip()
        output_path = self.settings.jobs_root / f"{job_id}.last-message.txt"
        self._emit_event(
            event_callback,
            event_type="runtime.context.loaded",
            status="planning",
            body=f"앱 레인 {app_id}의 상태와 세션을 불러왔습니다.",
            job_id=job_id,
            data={"session_id": session_id, "execution_mode": record.get("execution_mode", "direct")},
        )
        job_context, cwd = await self.proposals.current_proposal_context(record, job_id, request_payload["title"])
        if job_context is not None:
            self._emit_event(
                event_callback,
                event_type="proposal.worktree.prepared",
                status="planning",
                body=f"제안 브랜치 {job_context['branch_name']}와 작업 worktree를 준비했습니다.",
                job_id=job_id,
                data=job_context,
            )
        else:
            self._emit_event(
                event_callback,
                event_type="runtime.workspace.selected",
                status="planning",
                body=f"기존 작업 디렉터리 {cwd}에서 직접 실행합니다.",
                job_id=job_id,
                data={"cwd": str(cwd)},
            )
        prompt = build_prompt(self.settings, record, request_payload, job_context=job_context)
        image_paths = [str(path) for path in request_payload.get("attachment_paths") or [] if str(path).strip()]
        self.state.update_job(job_id, status="running", started_at=utc_now())

        try:
            self._emit_event(
                event_callback,
                event_type="codex.exec.started",
                status="running",
                body=f"Codex CLI를 {'기존 세션으로 재개' if session_id else '새 세션으로 시작'}합니다.",
                job_id=job_id,
                data={"cwd": str(cwd), "resuming_session": bool(session_id)},
            )
            returncode, stdout_text, stderr_text, final_output = await self.cli.run_codex(
                session_id,
                prompt,
                output_path,
                use_resume=bool(session_id),
                cwd=cwd,
                image_paths=image_paths,
            )
            if returncode != 0 and session_id:
                self._emit_event(
                    event_callback,
                    event_type="codex.exec.retrying",
                    status="running",
                    body="기존 세션 재개가 실패해 새 세션으로 다시 시도합니다.",
                    job_id=job_id,
                    data={"previous_session_id": session_id},
                )
                returncode, stdout_text, stderr_text, final_output = await self.cli.run_codex(
                    "",
                    prompt,
                    output_path,
                    use_resume=False,
                    cwd=cwd,
                    image_paths=image_paths,
                )

            discovered_thread_id = self.cli.extract_thread_id(stdout_text)
            if discovered_thread_id and discovered_thread_id != session_id:
                record["session_id"] = discovered_thread_id
                self._emit_event(
                    event_callback,
                    event_type="codex.session.updated",
                    status="running",
                    body="Codex가 새 thread id를 반환해 앱 세션 기록을 갱신했습니다.",
                    job_id=job_id,
                    data={"thread_id": discovered_thread_id},
                )

            self._emit_event(
                event_callback,
                event_type="codex.exec.finished",
                status="running" if returncode == 0 else "failed",
                body=(
                    "Codex CLI가 정상 종료되어 결과를 정리합니다."
                    if returncode == 0
                    else "Codex CLI가 오류와 함께 종료되어 실패 정보를 정리합니다."
                ),
                job_id=job_id,
                data={"returncode": returncode},
            )

            if returncode != 0:
                error_message = build_failure_message(returncode, stdout_text, stderr_text)
                decision_summary = default_decision_summary(
                    request_payload,
                    clean_summary=final_output,
                    error_message=error_message,
                    decision="Codex execution failed.",
                    why="The runtime attempted the request but the Codex CLI returned a non-zero exit status.",
                    verification="job failed after codex exec returned an error",
                    follow_up="Inspect the job error and retry after fixing the underlying issue.",
                )
                self.state.save_app(record)
                self._append_engineering_log(
                    app_id=app_id,
                    title=request_payload["title"],
                    job_id=job_id,
                    request_id=request_payload["request_id"],
                    decision_summary=decision_summary,
                )
                if job_context is not None:
                    proposal = self.proposals.proposal_payload(
                        record,
                        job_id,
                        request_payload,
                        job_context,
                        status="failed",
                        result_summary=final_output,
                        decision_summary=decision_summary,
                    )
                    self.state.save_proposal(proposal)
                    self._emit_event(
                        event_callback,
                        event_type="proposal.saved",
                        status="failed",
                        body=f"실패 상태의 proposal {proposal['branch_name']}를 보존했습니다.",
                        job_id=job_id,
                        data={"branch_name": proposal["branch_name"], "status": proposal["status"]},
                    )
                return self.state.update_job(
                    job_id,
                    status="failed",
                    completed_at=utc_now(),
                    error=error_message,
                    result_summary=final_output,
                    decision_summary=decision_summary,
                    ux_review={},
                    goal_review={},
                )

            final_output = final_output or "Codex run completed without a final message."
            clean_summary, parsed_goal_review = extract_goal_review_json(final_output)
            clean_summary, parsed_ux_review = extract_ux_review_json(clean_summary)
            clean_summary, parsed_summary = extract_engineering_log_json(clean_summary)
            clean_summary = sanitize_user_facing_text(clean_summary or "Codex run completed without a final message.")
            decision_summary = normalize_decision_summary(
                request_payload,
                parsed_summary,
                clean_summary=clean_summary,
                system_area="execution",
                verification="job completed",
            )
            ux_review = normalize_ux_review(parsed_ux_review)
            goal_review = normalize_goal_review(parsed_goal_review)

            record["last_summary"] = clean_summary
            self.state.save_app(record)
            self.state.append_memory(app_id, f"Agent Run {utc_now()}", clean_summary)
            self._emit_event(
                event_callback,
                event_type="runtime.summary.recorded",
                status="running",
                body="작업 요약, memory, engineering log를 저장했습니다.",
                job_id=job_id,
                data={"summary_length": len(clean_summary)},
            )
            self._append_engineering_log(
                app_id=app_id,
                title=request_payload["title"],
                job_id=job_id,
                request_id=request_payload["request_id"],
                decision_summary=decision_summary,
            )

            extra_fields: dict[str, Any] = {}
            if job_context is not None:
                proposal = await self.proposals.finalize_proposal(
                    record,
                    job_id,
                    request_payload,
                    job_context,
                    clean_summary,
                    decision_summary,
                    ux_review,
                )
                self._emit_event(
                    event_callback,
                    event_type="proposal.saved",
                    status="proposal",
                    body=f"proposal branch {proposal['branch_name']}를 저장하고 적용 대기 상태로 만들었습니다.",
                    job_id=job_id,
                    data={
                        "branch_name": proposal["branch_name"],
                        "head_commit": proposal["head_commit"],
                        "status": proposal["status"],
                    },
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
                ux_review=ux_review,
                goal_review=goal_review,
                **extra_fields,
            )
        except Exception as exc:
            error_message = str(exc)
            self._emit_event(
                event_callback,
                event_type="runtime.exception",
                status="failed",
                body="런타임 예외가 발생해 작업을 실패로 마감합니다.",
                job_id=job_id,
                data={"error": error_message},
            )
            decision_summary = default_decision_summary(
                request_payload,
                error_message=error_message,
                decision="Runtime failed before the job could finish.",
                why="A runtime exception interrupted the normal Codex execution flow.",
                verification="job failed because of a runtime exception",
                follow_up="Inspect the server traceback and retry once the runtime issue is fixed.",
            )
            self.state.save_app(record)
            self._append_engineering_log(
                app_id=app_id,
                title=request_payload["title"],
                job_id=job_id,
                request_id=request_payload["request_id"],
                decision_summary=decision_summary,
            )
            if job_context is not None:
                proposal = self.proposals.proposal_payload(
                    record,
                    job_id,
                    request_payload,
                    job_context,
                    status="failed",
                    decision_summary=decision_summary,
                )
                self.state.save_proposal(proposal)
            return self.state.update_job(
                job_id,
                status="failed",
                completed_at=utc_now(),
                error=error_message,
                decision_summary=decision_summary,
                ux_review={},
                goal_review={},
            )

    async def run_advisory_prompt(
        self,
        *,
        prompt: str,
        cwd,
        output_stem: str,
        sandbox: str = "read-only",
    ) -> tuple[int, str, str, str]:
        output_path = self.settings.jobs_root / f"{output_stem}.last-message.txt"
        return await self.cli.run_codex(
            "",
            prompt,
            output_path,
            use_resume=False,
            cwd=cwd,
            sandbox=sandbox,
        )

    async def apply_proposal(self, job_id: str) -> dict[str, Any]:
        proposal = self.state.get_proposal(job_id)
        if proposal.get("status") != "ready_to_apply":
            raise RuntimeError(f"Proposal {job_id} is not ready to apply.")

        repo_root = self.settings.repo_root
        status_before = await self.cli.git_output(repo_root, "status", "--porcelain")
        blocking_changes = self.proposals.blocking_repo_changes(status_before)
        if blocking_changes:
            preview = ", ".join(blocking_changes[:8])
            suffix = "" if len(blocking_changes) <= 8 else ", ..."
            raise RuntimeError(f"Repository has uncommitted changes. Refusing to apply proposal. Blocking paths: {preview}{suffix}")

        await self.proposals.merge_proposal(proposal)
        restart_service = str(proposal.get("restart_service") or "").strip()
        if restart_service:
            await self.proposals.schedule_restart(restart_service)

        push_status = "skipped"
        push_message = "Push after apply is disabled."
        if self.settings.push_after_apply:
            pushed, push_message = await self.proposals.push_applied_branch()
            push_status = "pushed" if pushed else "failed"

        proposal["status"] = "applied" if push_status != "failed" else "applied_local_push_failed"
        proposal["applied_at"] = utc_now()
        proposal["push_status"] = push_status
        proposal["push_remote"] = self.settings.push_remote
        proposal["push_branch"] = self.settings.push_branch
        proposal["push_message"] = push_message
        proposal["pushed_at"] = utc_now() if push_status == "pushed" else ""
        decision_summary = normalize_decision_summary(
            {
                "title": proposal.get("title") or f"Apply proposal {job_id}",
                "request_text": proposal.get("result_summary") or "",
            },
            proposal.get("decision_summary") if isinstance(proposal.get("decision_summary"), dict) else None,
            clean_summary=str(proposal.get("result_summary") or "").strip(),
            system_area="approval, deployment",
            decision=(
                f"Applied the approved proposal locally and pushed {self.settings.push_remote}/{self.settings.push_branch}."
                if push_status == "pushed"
                else "Applied the approved proposal locally, but the remote Git push failed."
                if push_status == "failed"
                else "Applied the approved proposal locally without pushing to the remote repository."
            ),
            why="Proposal mode keeps self-edits reviewable before they change the running system.",
            verification=(
                f"proposal merged locally, restart scheduled, and pushed to {self.settings.push_remote}/{self.settings.push_branch}"
                if restart_service and push_status == "pushed"
                else f"proposal merged locally and pushed to {self.settings.push_remote}/{self.settings.push_branch}"
                if push_status == "pushed"
                else "proposal merged locally and restart scheduled, but remote push failed"
                if restart_service and push_status == "failed"
                else "proposal merged locally, but remote push failed"
                if push_status == "failed"
                else "proposal merged locally and restart scheduled; remote push skipped"
                if restart_service
                else "proposal merged locally; remote push skipped"
            ),
            follow_up=(
                "Confirm GitHub Pages picks up the new push and that the service is healthy after restart."
                if push_status == "pushed" and restart_service
                else "Confirm GitHub received the new commit."
                if push_status == "pushed"
                else "Configure Git credentials on the server and push the updated main branch manually so GitHub Pages can redeploy."
                if push_status == "failed"
                else "Push the updated main branch later if GitHub should reflect the local runtime change."
            ),
        )
        proposal["decision_summary"] = decision_summary
        self.state.save_proposal(proposal)
        self._append_engineering_log(
            app_id=str(proposal.get("app_id") or "factory-runtime"),
            title=f"Apply proposal: {proposal.get('title') or job_id}",
            job_id=job_id,
            request_id=str(proposal.get("request_id") or job_id),
            decision_summary=decision_summary,
        )
        await self.proposals.cleanup_worktree(proposal["worktree_path"], proposal["branch_name"])
        return proposal
