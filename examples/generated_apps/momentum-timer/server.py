from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from momentum import generate_momentum


BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
DATA_PATH = BASE_DIR / "history.json"
HOST = "127.0.0.1"
PORT = 8041
MAX_HISTORY = 8


def read_history() -> list[dict[str, Any]]:
    if not DATA_PATH.exists():
        return []
    try:
        payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return payload if isinstance(payload, list) else []


def write_history(entries: list[dict[str, Any]]) -> None:
    DATA_PATH.write_text(
        json.dumps(entries[:MAX_HISTORY], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path in {"/", "/index.html"}:
            self._serve_file("index.html", "text/html; charset=utf-8")
            return
        if self.path == "/styles.css":
            self._serve_file("styles.css", "text/css; charset=utf-8")
            return
        if self.path == "/app.js":
            self._serve_file("app.js", "application/javascript; charset=utf-8")
            return
        if self.path == "/api/history":
            self._send_json({"history": read_history()[:MAX_HISTORY]})
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        if self.path != "/api/launch":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length)
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json({"error": "invalid_json"}, status=HTTPStatus.BAD_REQUEST)
            return

        task = str(payload.get("task", "")).strip()
        result = generate_momentum(task)
        if not result.task or not result.first_action:
            self._send_json({"error": "task_required"}, status=HTTPStatus.BAD_REQUEST)
            return

        history = read_history()
        history.insert(
            0,
            {
                "task": result.task,
                "first_action": result.first_action,
                "timer_seconds": result.timer_seconds,
            },
        )
        write_history(history)

        self._send_json(
            {
                "task": result.task,
                "first_action": result.first_action,
                "timer_seconds": result.timer_seconds,
                "history": history[:MAX_HISTORY],
            }
        )

    def _serve_file(self, filename: str, content_type: str) -> None:
        path = WEB_DIR / filename
        if not path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), AppHandler)
    print(f"Momentum Timer running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
