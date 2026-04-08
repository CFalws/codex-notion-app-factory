#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_ROOT = REPO_ROOT / "state"
REGISTRY_ROOT = STATE_ROOT / "registry" / "apps"
MEMORY_ROOT = STATE_ROOT / "memory"
REQUESTS_ROOT = STATE_ROOT / "requests"
WORKSPACES_ROOT = REPO_ROOT / "workspaces"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    result = []
    previous_dash = False
    for char in lowered:
        if char.isalnum():
            result.append(char)
            previous_dash = False
            continue
        if not previous_dash:
            result.append("-")
            previous_dash = True
    slug = "".join(result).strip("-")
    return slug or "app"


def ensure_layout() -> None:
    for path in (REGISTRY_ROOT, MEMORY_ROOT, REQUESTS_ROOT, WORKSPACES_ROOT):
        path.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def app_record_path(app_id: str) -> Path:
    return REGISTRY_ROOT / f"{app_id}.json"


def app_memory_path(app_id: str) -> Path:
    return MEMORY_ROOT / f"{app_id}.md"


def app_requests_path(app_id: str) -> Path:
    path = REQUESTS_ROOT / app_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_record(app_id: str) -> dict[str, Any]:
    path = app_record_path(app_id)
    if not path.exists():
        raise SystemExit(f"Unknown app_id: {app_id}")
    return read_json(path)


def save_record(record: dict[str, Any]) -> None:
    record["updated_at"] = utc_now()
    write_json(app_record_path(record["app_id"]), record)
    workspace_path = REPO_ROOT / record["workspace_path"]
    workspace_path.mkdir(parents=True, exist_ok=True)
    source_path = REPO_ROOT / record["source_path"] if record.get("source_path") else Path()
    write_workspace_anchor(record["app_id"], record["title"], workspace_path, source_path)


def write_memory_snapshot(app_id: str, content: str) -> None:
    path = app_memory_path(app_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_workspace_anchor(app_id: str, title: str, workspace_path: Path, source_path: Path) -> None:
    payload = {
        "app_id": app_id,
        "title": title,
        "workspace_path": relative_to_repo(workspace_path),
        "source_path": relative_to_repo(source_path) if str(source_path) else "",
    }
    write_json(workspace_path / "workspace.json", payload)
    summary = f"""# {title} Workspace

This directory anchors the maintenance lane for `{app_id}`.

- workspace_path: `{relative_to_repo(workspace_path)}`
- source_path: `{relative_to_repo(source_path) if str(source_path) else "(not set)"}`

Use this directory as the durable reference point for:

- session ids
- maintenance notes
- change requests
- handoff summaries
"""
    (workspace_path / "README.md").write_text(summary, encoding="utf-8")


def append_memory_section(app_id: str, heading: str, body: str) -> None:
    path = app_memory_path(app_id)
    existing = path.read_text(encoding="utf-8") if path.exists() else f"# {app_id} Memory\n"
    updated = existing.rstrip() + f"\n\n## {heading}\n\n{body.strip()}\n"
    path.write_text(updated, encoding="utf-8")


def relative_to_repo(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


@dataclass
class AppWorkspace:
    app_id: str
    title: str
    workspace_path: Path
    source_path: Path


def create_workspace(app_id: str, title: str, source_path: Path) -> AppWorkspace:
    workspace_path = WORKSPACES_ROOT / app_id
    if workspace_path.exists() and any(workspace_path.iterdir()):
        raise SystemExit(f"Workspace already exists and is not empty: {workspace_path}")

    if source_path.exists():
        shutil.copytree(source_path, workspace_path, dirs_exist_ok=True)
    else:
        workspace_path.mkdir(parents=True, exist_ok=True)

    return AppWorkspace(app_id=app_id, title=title, workspace_path=workspace_path, source_path=source_path)


def command_init_app(args: argparse.Namespace) -> None:
    ensure_layout()
    app_id = args.app_id or slugify(args.title)
    path = app_record_path(app_id)
    if path.exists():
        raise SystemExit(f"App record already exists: {app_id}")

    source_path = Path(args.source_path).expanduser().resolve() if args.source_path else Path()
    workspace = create_workspace(app_id, args.title, source_path) if args.copy_source else AppWorkspace(
        app_id=app_id,
        title=args.title,
        workspace_path=(WORKSPACES_ROOT / app_id),
        source_path=source_path,
    )
    workspace.workspace_path.mkdir(parents=True, exist_ok=True)
    write_workspace_anchor(app_id, args.title, workspace.workspace_path, source_path)

    record = {
        "app_id": app_id,
        "title": args.title,
        "aliases": args.aliases or [],
        "workspace_path": relative_to_repo(workspace.workspace_path),
        "source_path": relative_to_repo(source_path) if str(source_path) else "",
        "platform": args.platform,
        "delivery_type": args.delivery_type,
        "status": "active",
        "session_id": args.session_id or "",
        "deployment_url": args.deployment_url or "",
        "latest_commit": args.latest_commit or "",
        "last_summary": args.summary or "",
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    save_record(record)

    initial_memory = f"""# {app_id} Memory

## App

- title: {args.title}
- workspace_path: {relative_to_repo(workspace.workspace_path)}
- source_path: {relative_to_repo(source_path) if str(source_path) else "(not set)"}
- platform: {args.platform}
- delivery_type: {args.delivery_type}

## Current State

{args.summary or "No summary yet."}
"""
    write_memory_snapshot(app_id, initial_memory)
    print(json.dumps(record, indent=2, ensure_ascii=False))


def command_update_session(args: argparse.Namespace) -> None:
    ensure_layout()
    record = load_record(args.app_id)
    if args.session_id is not None:
        record["session_id"] = args.session_id
    if args.latest_commit is not None:
        record["latest_commit"] = args.latest_commit
    if args.deployment_url is not None:
        record["deployment_url"] = args.deployment_url
    if args.summary is not None:
        record["last_summary"] = args.summary
        append_memory_section(args.app_id, f"Session Update {utc_now()}", args.summary)
    save_record(record)
    print(json.dumps(record, indent=2, ensure_ascii=False))


def command_add_request(args: argparse.Namespace) -> None:
    ensure_layout()
    record = load_record(args.app_id)
    requests_dir = app_requests_path(args.app_id)
    request_id = args.request_id or utc_now().replace(":", "-")
    payload = {
        "request_id": request_id,
        "app_id": args.app_id,
        "status": args.status,
        "title": args.title,
        "request_text": args.request_text,
        "source": args.source,
        "created_at": utc_now(),
        "updated_at": utc_now(),
    }
    write_json(requests_dir / f"{request_id}.json", payload)
    record["last_summary"] = f"Latest request: {args.title}"
    save_record(record)
    append_memory_section(
        args.app_id,
        f"Request {request_id}",
        f"source: {args.source}\nstatus: {args.status}\n\n{args.request_text}",
    )
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def command_show(args: argparse.Namespace) -> None:
    ensure_layout()
    record = load_record(args.app_id)
    payload = {"record": record}
    memory_path = app_memory_path(args.app_id)
    if memory_path.exists():
        payload["memory_path"] = relative_to_repo(memory_path)
    requests_dir = app_requests_path(args.app_id)
    payload["requests"] = sorted(path.name for path in requests_dir.glob("*.json"))
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def command_list(args: argparse.Namespace) -> None:
    ensure_layout()
    records = []
    for path in sorted(REGISTRY_ROOT.glob("*.json")):
        records.append(read_json(path))
    print(json.dumps(records, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage app-specific workspaces and persistent session state.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-app", help="Create an app workspace and persistent record.")
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--app-id")
    init_parser.add_argument("--aliases", nargs="*", default=[])
    init_parser.add_argument("--platform", default="phone-first-web")
    init_parser.add_argument("--delivery-type", default="installable-pwa")
    init_parser.add_argument("--source-path")
    init_parser.add_argument("--copy-source", action="store_true")
    init_parser.add_argument("--session-id")
    init_parser.add_argument("--deployment-url")
    init_parser.add_argument("--latest-commit")
    init_parser.add_argument("--summary")
    init_parser.set_defaults(func=command_init_app)

    update_parser = subparsers.add_parser("update-session", help="Update durable session metadata for an app.")
    update_parser.add_argument("--app-id", required=True)
    update_parser.add_argument("--session-id")
    update_parser.add_argument("--deployment-url")
    update_parser.add_argument("--latest-commit")
    update_parser.add_argument("--summary")
    update_parser.set_defaults(func=command_update_session)

    request_parser = subparsers.add_parser("add-request", help="Attach a change request to an existing app.")
    request_parser.add_argument("--app-id", required=True)
    request_parser.add_argument("--title", required=True)
    request_parser.add_argument("--request-text", required=True)
    request_parser.add_argument("--source", default="notion-mobile")
    request_parser.add_argument("--status", default="pending")
    request_parser.add_argument("--request-id")
    request_parser.set_defaults(func=command_add_request)

    show_parser = subparsers.add_parser("show", help="Show the record and memory path for one app.")
    show_parser.add_argument("--app-id", required=True)
    show_parser.set_defaults(func=command_show)

    list_parser = subparsers.add_parser("list", help="List app records.")
    list_parser.set_defaults(func=command_list)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
