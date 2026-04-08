from __future__ import annotations

import asyncio
import json
import os
import shutil
from pathlib import Path
from typing import Any

from .config import RuntimeSettings
from .state import RuntimeState, utc_now


class CodexAgentsRuntime:
    def __init__(self, settings: RuntimeSettings, state: RuntimeState) -> None:
        self.settings = settings
        self.state = state

    def _is_proposal_mode(self, record: dict[str, Any]) -> bool:
        return str(record.get("execution_mode", "")).strip() == "proposal"

    def _allowed_paths_text(self, record: dict[str, Any]) -> str:
        allowed_paths = record.get("allowed_paths") or []
        if not allowed_paths:
            return "- No explicit path allowlist was provided."
        return "\n".join(f"- {path}" for path in allowed_paths)

    def _build_instructions(self, record: dict[str, Any], *, job_context: dict[str, str] | None = None) -> str:
        source_path = record.get("source_path") or "(not set)"
        workspace_path = record.get("workspace_path") or "(not set)"
        deployment_url = record.get("deployment_url") or "(not deployed yet)"
        summary = record.get("last_summary") or "No prior summary."
        proposal_mode = self._is_proposal_mode(record)
        proposal_lines = ""
        if proposal_mode and job_context is not None:
            proposal_lines = f"""
Proposal mode context:
- Worktree path: {job_context["worktree_path"]}
- Proposal branch: {job_context["branch_name"]}
- Base branch: {job_context["base_branch"]}
- Allowed paths:
{self._allowed_paths_text(record)}

Proposal rules:
- Work only inside the proposal worktree.
- Restrict edits to the allowed paths when they are provided.
- Create a git commit on the proposal branch before finishing.
- Do not deploy, merge, or restart services yourself.
""".strip()
        return f"""
You are maintaining one app inside a stateful personal app factory repository.

Repository root: {self.settings.repo_root}
Target app id: {record["app_id"]}
Target app title: {record["title"]}
Source path: {source_path}
Workspace path: {workspace_path}
Deployment URL: {deployment_url}
Last summary: {summary}

Rules:
- Work only inside this repository.
- Prefer continuity with the existing app instead of rebuilding from scratch.
- Keep the web app deployable through GitHub Pages after code changes.
- If the request is ambiguous, make the smallest reasonable assumption and proceed.
- Summarize exactly what changed and any follow-up needed.
{proposal_lines if proposal_lines else ""}
""".strip()

    def _build_prompt(
        self,
        record: dict[str, Any],
        request_payload: dict[str, Any],
        *,
        job_context: dict[str, str] | None = None,
    ) -> str:
        proposal_tail = ""
        if self._is_proposal_mode(record):
            proposal_tail = """
Before finishing:
1. stage your changes,
2. create exactly one commit on the proposal branch,
3. include the final commit hash in the summary,
4. mention whether the proposal is ready to apply.
""".strip()
        return f"""
{self._build_instructions(record, job_context=job_context)}

Continue work on the existing app lane.

App id: {record["app_id"]}
App title: {record["title"]}
Request title: {request_payload["title"]}
Request source: {request_payload["source"]}

Request:
{request_payload["request_text"]}

After completing the work, provide:
1. the key code changes,
2. any deployment-impacting notes,
3. the next best follow-up action if the work should continue.
{proposal_tail if proposal_tail else ""}
""".strip()

    def _build_command(self, session_id: str, prompt: str, output_path: Path, *, use_resume: bool) -> list[str]:
        args = [self.settings.codex_command, *self.settings.codex_args, "exec"]
        if use_resume and session_id:
            args.extend(["resume", session_id])
        if self.settings.codex_profile:
            args.extend(["--profile", self.settings.codex_profile])
        if self.settings.codex_model:
            args.extend(["--model", self.settings.codex_model])
        if self.settings.codex_sandbox:
            args.extend(["--sandbox", self.settings.codex_sandbox])
        if self.settings.codex_skip_git_repo_check:
            args.append("--skip-git-repo-check")
        args.extend(["--output-last-message", str(output_path), "--json", prompt])
        return args

    def _build_env(self) -> dict[str, str]:
        env = os.environ.copy()
        if self.settings.codex_home is not None:
            env["CODEX_HOME"] = str(self.settings.codex_home)
        return env

    async def _run_command(
        self,
        command: list[str],
        *,
        cwd: Path,
        capture_output: bool = True,
    ) -> tuple[int, str, str]:
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=str(cwd),
            env=self._build_env(),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE if capture_output else asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE if capture_output else asyncio.subprocess.DEVNULL,
        )
        stdout_bytes, stderr_bytes = await process.communicate()
        stdout_text = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
        stderr_text = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
        return process.returncode, stdout_text, stderr_text

    async def _run_codex(
        self,
        session_id: str,
        prompt: str,
        output_path: Path,
        *,
        use_resume: bool,
        cwd: Path,
    ) -> tuple[int, str, str, str]:
        command = self._build_command(session_id, prompt, output_path, use_resume=use_resume)
        returncode, stdout_text, stderr_text = await self._run_command(command, cwd=cwd)
        final_output = output_path.read_text(encoding="utf-8").strip() if output_path.exists() else ""
        return returncode, stdout_text, stderr_text, final_output

    def _extract_thread_id(self, stdout_text: str) -> str:
        for line in stdout_text.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if payload.get("type") == "thread.started" and payload.get("thread_id"):
                return str(payload["thread_id"])
        return ""

    def _build_failure_message(self, returncode: int, stdout_text: str, stderr_text: str) -> str:
        for source in (stderr_text, stdout_text):
            for line in reversed(source.splitlines()):
                line = line.strip()
                if line:
                    return f"codex exec failed with exit code {returncode}: {line}"
        return f"codex exec failed with exit code {returncode}."

    async def _git_output(self, cwd: Path, *args: str) -> str:
        returncode, stdout_text, stderr_text = await self._run_command(["git", *args], cwd=cwd)
        if returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {(stderr_text or stdout_text).strip()}")
        return stdout_text.strip()

    async def _prepare_proposal_worktree(self, record: dict[str, Any], job_id: str, title: str) -> dict[str, str]:
        repo_root = self.settings.repo_root
        base_branch = str(record.get("base_branch") or "main").strip() or "main"
        slug = "".join(char.lower() if char.isalnum() else "-" for char in title).strip("-") or "proposal"
        branch_name = f"codex/{record['app_id']}-{slug[:32]}-{job_id[:8]}"
        worktree_path = self.settings.worktrees_root / job_id
        if worktree_path.exists():
            shutil.rmtree(worktree_path)
        await self._git_output(repo_root, "worktree", "add", str(worktree_path), "-b", branch_name, base_branch)
        return {
            "base_branch": base_branch,
            "branch_name": branch_name,
            "worktree_path": str(worktree_path),
        }

    async def _cleanup_proposal_worktree(self, worktree_path: str, branch_name: str) -> None:
        path = Path(worktree_path)
        if path.exists():
            await self._run_command(["git", "worktree", "remove", "--force", str(path)], cwd=self.settings.repo_root)
        await self._run_command(["git", "branch", "-D", branch_name], cwd=self.settings.repo_root)

    def _proposal_payload(
        self,
        record: dict[str, Any],
        job_id: str,
        request_payload: dict[str, Any],
        job_context: dict[str, str],
        *,
        status: str,
        result_summary: str = "",
        git_status: str = "",
        git_show_stat: str = "",
        base_commit: str = "",
        head_commit: str = "",
    ) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "app_id": record["app_id"],
            "request_id": request_payload["request_id"],
            "status": status,
            "title": request_payload["title"],
            "branch_name": job_context["branch_name"],
            "base_branch": job_context["base_branch"],
            "base_commit": base_commit,
            "head_commit": head_commit,
            "worktree_path": job_context["worktree_path"],
            "restart_service": str(record.get("restart_service") or "").strip(),
            "allowed_paths": record.get("allowed_paths") or [],
            "result_summary": result_summary,
            "git_status": git_status,
            "git_show_stat": git_show_stat,
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }

    async def _finalize_proposal(
        self,
        record: dict[str, Any],
        job_id: str,
        request_payload: dict[str, Any],
        job_context: dict[str, str],
        final_output: str,
    ) -> dict[str, Any]:
        worktree_path = Path(job_context["worktree_path"])
        head_commit = await self._git_output(worktree_path, "rev-parse", "HEAD")
        base_commit = await self._git_output(worktree_path, "rev-parse", job_context["base_branch"])
        status = await self._git_output(worktree_path, "status", "--short")
        diff_stat = await self._git_output(worktree_path, "show", "--stat", "--oneline", "--format=%H%n%s", "HEAD")
        proposal = self._proposal_payload(
            record,
            job_id,
            request_payload,
            job_context,
            status="ready_to_apply",
            result_summary=final_output,
            git_status=status,
            git_show_stat=diff_stat,
            base_commit=base_commit,
            head_commit=head_commit,
        )
        self.state.save_proposal(proposal)
        return proposal

    async def _merge_proposal(self, proposal: dict[str, Any]) -> None:
        repo_root = self.settings.repo_root
        try:
            await self._git_output(repo_root, "merge", "--ff-only", proposal["head_commit"])
        except RuntimeError:
            await self._git_output(repo_root, "merge", "--no-ff", "--no-edit", proposal["head_commit"])

    async def _schedule_restart(self, service_name: str) -> None:
        repo_root = self.settings.repo_root
        returncode, stdout_text, stderr_text = await self._run_command(
            [
                "sudo",
                "/usr/bin/systemd-run",
                "--unit",
                f"{service_name}-proposal-restart",
                "--on-active=2",
                "/usr/bin/systemctl",
                "restart",
                service_name,
            ],
            cwd=repo_root,
        )
        if returncode != 0:
            raise RuntimeError(
                f"Applied proposal commit but failed to schedule restart for {service_name}: {(stderr_text or stdout_text).strip()}"
            )

    async def run_request(self, app_id: str, job_id: str, request_payload: dict[str, Any]) -> dict[str, Any]:
        if not self.settings.codex_command:
            raise RuntimeError("CODEX_COMMAND is not configured.")

        record = self.state.get_app(app_id)
        session_id = str(record.get("session_id", "")).strip()
        output_path = self.settings.jobs_root / f"{job_id}.last-message.txt"
        job_context: dict[str, str] | None = None
        cwd = self.settings.repo_root

        if self._is_proposal_mode(record):
            job_context = await self._prepare_proposal_worktree(record, job_id, request_payload["title"])
            cwd = Path(job_context["worktree_path"])

        prompt = self._build_prompt(record, request_payload, job_context=job_context)
        self.state.update_job(job_id, status="running", started_at=utc_now())

        try:
            returncode, stdout_text, stderr_text, final_output = await self._run_codex(
                session_id,
                prompt,
                output_path,
                use_resume=bool(session_id),
                cwd=cwd,
            )
            if returncode != 0 and session_id:
                returncode, stdout_text, stderr_text, final_output = await self._run_codex(
                    "",
                    prompt,
                    output_path,
                    use_resume=False,
                    cwd=cwd,
                )

            discovered_thread_id = self._extract_thread_id(stdout_text)
            if discovered_thread_id and discovered_thread_id != session_id:
                record["session_id"] = discovered_thread_id

            if returncode != 0:
                error_message = self._build_failure_message(returncode, stdout_text, stderr_text)
                self.state.save_app(record)
                return self.state.update_job(
                    job_id,
                    status="failed",
                    completed_at=utc_now(),
                    error=error_message,
                )

            final_output = final_output or "Codex run completed without a final message."
            record["last_summary"] = final_output
            self.state.save_app(record)
            self.state.append_memory(app_id, f"Agent Run {utc_now()}", final_output)

            extra_fields: dict[str, Any] = {}
            if job_context is not None:
                proposal = await self._finalize_proposal(record, job_id, request_payload, job_context, final_output)
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
                result_summary=final_output,
                error="",
                **extra_fields,
            )
        except Exception:
            if job_context is not None:
                proposal = self._proposal_payload(
                    record,
                    job_id,
                    request_payload,
                    job_context,
                    status="failed",
                )
                self.state.save_proposal(proposal)
            raise

    async def apply_proposal(self, job_id: str) -> dict[str, Any]:
        proposal = self.state.get_proposal(job_id)
        if proposal.get("status") != "ready_to_apply":
            raise RuntimeError(f"Proposal {job_id} is not ready to apply.")

        repo_root = self.settings.repo_root
        status_before = await self._git_output(repo_root, "status", "--porcelain")
        if status_before.strip():
            raise RuntimeError("Repository has uncommitted changes. Refusing to apply proposal.")

        await self._merge_proposal(proposal)
        restart_service = str(proposal.get("restart_service") or "").strip()
        if restart_service:
            await self._schedule_restart(restart_service)

        proposal["status"] = "applied"
        proposal["applied_at"] = utc_now()
        self.state.save_proposal(proposal)
        await self._cleanup_proposal_worktree(proposal["worktree_path"], proposal["branch_name"])
        return proposal
