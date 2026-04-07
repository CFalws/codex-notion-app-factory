from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import functools


HOST = "0.0.0.0"
PORT = 4173
WEB_DIR = Path(__file__).resolve().parent / "web"


def main() -> None:
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(WEB_DIR))
    server = ThreadingHTTPServer((HOST, PORT), handler)
    print(f"Preview running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
