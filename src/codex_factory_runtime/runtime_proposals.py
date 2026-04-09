from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .config import RuntimeSettings
from .runtime_cli import CodexCliRunner
from .runtime_engineering import is_proposal_mode
from .state import RuntimeState, utc_now


class ProposalRuntime:
    def __init__(self, settings: RuntimeSettings, state: RuntimeState, cli: CodexCliRunner) -> None:
        self.settings = settings
        self.state = state
        self.cli = cli

    async def prepare_worktree(self, record: dict[str, Any], job_id: str, title: str) -> dict[str, str]:
        repo_root = self.settings.repo_root
        base_branch = str(record.get("base_branch") or "main").strip() or "main"
        slug_source = title or job_id
        slug = "".join(char.lower() if char.isalnum() else "-" for char in slug_source).strip("-") or "proposal"
        branch_name = f"codex/{record['app_id']}-{slug[:32]}-{job_id[:8]}"
        worktree_path = self.settings.worktrees_root / job_id
        if worktree_path.exists():
            shutil.rmtree(worktree_path)
        await self.cli.git_output(repo_root, "worktree", "add", str(worktree_path), "-b", branch_name, base_branch)
        return {
            "base_branch": base_branch,
            "branch_name": branch_name,
            "worktree_path": str(worktree_path),
        }

    async def cleanup_worktree(self, worktree_path: str, branch_name: str) -> None:
        path = Path(worktree_path)
        if path.exists():
            await self.cli.run_command(["git", "worktree", "remove", "--force", str(path)], cwd=self.settings.repo_root)
        await self.cli.run_command(["git", "branch", "-D", branch_name], cwd=self.settings.repo_root)

    def proposal_payload(
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
        decision_summary: dict[str, str] | None = None,
        ux_review: dict[str, str] | None = None,
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
            "decision_summary": decision_summary or {},
            "ux_review": ux_review or {},
            "git_status": git_status,
            "git_show_stat": git_show_stat,
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }

    async def finalize_proposal(
        self,
        record: dict[str, Any],
        job_id: str,
        request_payload: dict[str, Any],
        job_context: dict[str, str],
        final_output: str,
        decision_summary: dict[str, str],
        ux_review: dict[str, str],
    ) -> dict[str, Any]:
        worktree_path = Path(job_context["worktree_path"])
        head_commit = await self.cli.git_output(worktree_path, "rev-parse", "HEAD")
        base_commit = await self.cli.git_output(worktree_path, "rev-parse", job_context["base_branch"])
        status = await self.cli.git_output(worktree_path, "status", "--short")
        diff_stat = await self.cli.git_output(worktree_path, "show", "--stat", "--oneline", "--format=%H%n%s", "HEAD")
        proposal = self.proposal_payload(
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
            decision_summary=decision_summary,
            ux_review=ux_review,
        )
        self.state.save_proposal(proposal)
        return proposal

    async def merge_proposal(self, proposal: dict[str, Any]) -> None:
        repo_root = self.settings.repo_root
        try:
            await self.cli.git_output(repo_root, "merge", "--ff-only", proposal["head_commit"])
        except RuntimeError:
            await self.cli.git_output(repo_root, "merge", "--no-ff", "--no-edit", proposal["head_commit"])

    async def schedule_restart(self, service_name: str) -> None:
        repo_root = self.settings.repo_root
        returncode, stdout_text, stderr_text = await self.cli.run_command(
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

    async def push_applied_branch(self) -> tuple[bool, str]:
        repo_root = self.settings.repo_root
        returncode, stdout_text, stderr_text = await self.cli.run_command(
            ["git", "push", self.settings.push_remote, f"HEAD:{self.settings.push_branch}"],
            cwd=repo_root,
        )
        detail = (stderr_text or stdout_text).strip()
        if returncode == 0 and not detail:
            detail = f"Pushed HEAD to {self.settings.push_remote}/{self.settings.push_branch}."
        return returncode == 0, detail

    def blocking_repo_changes(self, status_output: str) -> list[str]:
        ignored_prefixes = {
            "state/",
            "examples/generated_apps/habit-tracker-pwa/runtime-api-verification/",
            "workspaces/habit-tracker-pwa/runtime-api-verification/",
        }
        blocking: list[str] = []
        for raw_line in status_output.splitlines():
            line = raw_line.rstrip()
            if not line:
                continue
            path_part = line[3:] if len(line) > 3 else line
            if " -> " in path_part:
                path_part = path_part.split(" -> ", 1)[1]
            normalized = path_part.strip()
            if any(normalized.startswith(prefix) for prefix in ignored_prefixes):
                continue
            blocking.append(normalized)
        return blocking

    async def current_proposal_context(self, record: dict[str, Any], job_id: str, title: str) -> tuple[dict[str, str] | None, Path]:
        if not is_proposal_mode(record):
            return None, self.settings.repo_root
        context = await self.prepare_worktree(record, job_id, title)
        return context, Path(context["worktree_path"])
