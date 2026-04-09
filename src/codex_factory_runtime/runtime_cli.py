from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from .config import RuntimeSettings


class CodexCliRunner:
    def __init__(self, settings: RuntimeSettings) -> None:
        self.settings = settings

    def build_command(
        self,
        session_id: str,
        prompt: str,
        output_path: Path,
        *,
        use_resume: bool,
        sandbox: str | None = None,
    ) -> list[str]:
        args = [self.settings.codex_command, *self.settings.codex_args, "exec"]
        if use_resume and session_id:
            if self.settings.codex_profile:
                args.extend(["--profile", self.settings.codex_profile])
            args.extend(["resume", session_id])
            if self.settings.codex_model:
                args.extend(["--model", self.settings.codex_model])
            if self.settings.codex_skip_git_repo_check:
                args.append("--skip-git-repo-check")
            args.extend(["--output-last-message", str(output_path), "--json", prompt])
            return args
        if self.settings.codex_profile:
            args.extend(["--profile", self.settings.codex_profile])
        if self.settings.codex_model:
            args.extend(["--model", self.settings.codex_model])
        chosen_sandbox = self.settings.codex_sandbox if sandbox is None else sandbox
        if chosen_sandbox:
            args.extend(["--sandbox", chosen_sandbox])
        if self.settings.codex_skip_git_repo_check:
            args.append("--skip-git-repo-check")
        args.extend(["--output-last-message", str(output_path), "--json", prompt])
        return args

    def build_env(self) -> dict[str, str]:
        env = os.environ.copy()
        if self.settings.codex_home is not None:
            env["CODEX_HOME"] = str(self.settings.codex_home)
        return env

    async def run_command(
        self,
        command: list[str],
        *,
        cwd: Path,
        capture_output: bool = True,
        timeout_seconds: int | None = None,
    ) -> tuple[int, str, str]:
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=str(cwd),
            env=self.build_env(),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE if capture_output else asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE if capture_output else asyncio.subprocess.DEVNULL,
        )
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(process.communicate(), timeout=timeout_seconds)
        except TimeoutError:
            process.kill()
            stdout_bytes, stderr_bytes = await process.communicate()
            stdout_text = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
            stderr_text = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
            timeout_message = f"Command timed out after {timeout_seconds} seconds."
            stderr_text = f"{stderr_text}\n{timeout_message}".strip() if stderr_text else timeout_message
            return 124, stdout_text, stderr_text
        stdout_text = stdout_bytes.decode("utf-8", errors="replace") if stdout_bytes else ""
        stderr_text = stderr_bytes.decode("utf-8", errors="replace") if stderr_bytes else ""
        return process.returncode, stdout_text, stderr_text

    async def run_codex(
        self,
        session_id: str,
        prompt: str,
        output_path: Path,
        *,
        use_resume: bool,
        cwd: Path,
        sandbox: str | None = None,
        timeout_seconds: int | None = None,
    ) -> tuple[int, str, str, str]:
        command = self.build_command(
            session_id,
            prompt,
            output_path,
            use_resume=use_resume,
            sandbox=sandbox,
        )
        returncode, stdout_text, stderr_text = await self.run_command(
            command,
            cwd=cwd,
            timeout_seconds=timeout_seconds,
        )
        final_output = output_path.read_text(encoding="utf-8").strip() if output_path.exists() else ""
        return returncode, stdout_text, stderr_text, final_output

    async def git_output(self, cwd: Path, *args: str) -> str:
        returncode, stdout_text, stderr_text = await self.run_command(["git", *args], cwd=cwd)
        if returncode != 0:
            raise RuntimeError(f"git {' '.join(args)} failed: {(stderr_text or stdout_text).strip()}")
        return stdout_text.strip()

    def extract_thread_id(self, stdout_text: str) -> str:
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
