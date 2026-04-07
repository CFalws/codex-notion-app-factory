from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPORT_PATH = BASE_DIR / "validation_report.md"
RESULTS_PATH = BASE_DIR / "validation_results.json"


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_compile_check() -> dict:
    proc = subprocess.run(
        [sys.executable, "-m", "compileall", str(BASE_DIR)],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "passed": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def run_generation_checks(launcher_module) -> list[dict]:
    test_cases = [
        {
            "task": "clean the kitchen",
            "expected": "Put one item back in place or clear one small surface.",
        },
        {
            "task": "reply to emails",
            "expected": "Open your inbox and answer the shortest pending message.",
        },
        {
            "task": "start studying math",
            "expected": "Open your notes or book and finish just the first tiny item.",
        },
        {
            "task": "work out",
            "expected": "Open the place where you do 'work out' and do the first visible step.",
        },
        {
            "task": "build my app landing page",
            "expected": "Open the project and fix or write the smallest visible piece first.",
        },
    ]

    results = []
    for case in test_cases:
        result = launcher_module.generate_first_action(case["task"])
        passed = result.first_action == case["expected"]
        results.append(
            {
                "task": case["task"],
                "expected": case["expected"],
                "actual": result.first_action,
                "passed": passed,
            }
        )
    return results


def run_history_check(server_module) -> dict:
    sample_entries = [
        {
            "task": "clean the kitchen",
            "first_action": "Put one item back in place or clear one small surface.",
        },
        {
            "task": "reply to emails",
            "first_action": "Open your inbox and answer the shortest pending message.",
        },
    ]
    server_module.write_history(sample_entries)
    reloaded = server_module.read_history()
    return {
        "passed": reloaded == sample_entries,
        "written": sample_entries,
        "reloaded": reloaded,
    }


def build_report(payload: dict) -> str:
    compile_section = payload["compile_check"]
    generation_section = payload["generation_checks"]
    history_section = payload["history_check"]

    generation_lines = []
    for item in generation_section:
        status = "PASS" if item["passed"] else "FAIL"
        generation_lines.append(
            f"- [{status}] `{item['task']}` -> `{item['actual']}`"
        )

    return "\n".join(
        [
            "# Validation Report",
            "",
            "## Summary",
            "",
            f"- compile check: {'PASS' if compile_section['passed'] else 'FAIL'}",
            f"- generation checks: {'PASS' if all(item['passed'] for item in generation_section) else 'FAIL'}",
            f"- history persistence check: {'PASS' if history_section['passed'] else 'FAIL'}",
            "",
            "## Compile Check",
            "",
            "```text",
            compile_section["stdout"] or "(no output)",
            "```",
            "",
            "## Generation Checks",
            "",
            *generation_lines,
            "",
            "## History Check",
            "",
            f"- passed: {'yes' if history_section['passed'] else 'no'}",
            f"- entries reloaded: {len(history_section['reloaded'])}",
            "",
            "## Environment Note",
            "",
            "Local HTTP port binding could not be demonstrated inside the sandboxed session, so browser-level serving is still a local-shell verification step.",
        ]
    )


def main() -> None:
    launcher_module = load_module("sample_focus_launcher_launcher", BASE_DIR / "launcher.py")
    server_module = load_module("sample_focus_launcher_server", BASE_DIR / "server.py")

    payload = {
        "compile_check": run_compile_check(),
        "generation_checks": run_generation_checks(launcher_module),
        "history_check": run_history_check(server_module),
    }

    RESULTS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    REPORT_PATH.write_text(build_report(payload), encoding="utf-8")

    print(f"Wrote {RESULTS_PATH.name}")
    print(f"Wrote {REPORT_PATH.name}")


if __name__ == "__main__":
    main()
