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


def run_generation_checks(momentum_module) -> list[dict]:
    cases = [
        {
            "task": "clean the kitchen",
            "expected": "Clear one small surface or put one item back where it belongs.",
        },
        {
            "task": "reply to emails",
            "expected": "Open your inbox and answer the shortest pending message first.",
        },
        {
            "task": "start studying math",
            "expected": "Open your notes and complete just the first tiny item you see.",
        },
        {
            "task": "build landing page",
            "expected": "Open the project and finish the smallest visible code change first.",
        },
    ]
    results = []
    for case in cases:
        result = momentum_module.generate_momentum(case["task"])
        results.append(
            {
                "task": case["task"],
                "expected": case["expected"],
                "actual": result.first_action,
                "timer_seconds": result.timer_seconds,
                "passed": result.first_action == case["expected"] and result.timer_seconds == 180,
            }
        )
    return results


def run_history_check(server_module) -> dict:
    sample_entries = [
        {
            "task": "clean the kitchen",
            "first_action": "Clear one small surface or put one item back where it belongs.",
            "timer_seconds": 180,
        },
        {
            "task": "reply to emails",
            "first_action": "Open your inbox and answer the shortest pending message first.",
            "timer_seconds": 180,
        },
    ]
    server_module.write_history(sample_entries)
    reloaded = server_module.read_history()
    return {"passed": reloaded == sample_entries, "reloaded": reloaded}


def build_report(payload: dict) -> str:
    compile_check = payload["compile_check"]
    generation_checks = payload["generation_checks"]
    history_check = payload["history_check"]

    lines = [
        "# Validation Report",
        "",
        "## Summary",
        "",
        f"- compile check: {'PASS' if compile_check['passed'] else 'FAIL'}",
        f"- generation checks: {'PASS' if all(item['passed'] for item in generation_checks) else 'FAIL'}",
        f"- history check: {'PASS' if history_check['passed'] else 'FAIL'}",
        "",
        "## Compile Check",
        "",
        "```text",
        compile_check["stdout"] or "(no output)",
        "```",
        "",
        "## Generation Checks",
        "",
    ]
    for item in generation_checks:
        status = "PASS" if item["passed"] else "FAIL"
        lines.append(f"- [{status}] `{item['task']}` -> `{item['actual']}` (`{item['timer_seconds']}s`)")

    lines.extend(
        [
            "",
            "## History Check",
            "",
            f"- passed: {'yes' if history_check['passed'] else 'no'}",
            f"- entries reloaded: {len(history_check['reloaded'])}",
            "",
            "## Environment Note",
            "",
            "The sandbox blocked local HTTP port binding, so full browser serving still needs to be run in a normal local shell.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    momentum_module = load_module("momentum_timer_momentum", BASE_DIR / "momentum.py")
    server_module = load_module("momentum_timer_server", BASE_DIR / "server.py")

    payload = {
        "compile_check": run_compile_check(),
        "generation_checks": run_generation_checks(momentum_module),
        "history_check": run_history_check(server_module),
    }

    RESULTS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    REPORT_PATH.write_text(build_report(payload), encoding="utf-8")

    print(f"Wrote {RESULTS_PATH.name}")
    print(f"Wrote {REPORT_PATH.name}")


if __name__ == "__main__":
    main()
