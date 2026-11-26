#!/usr/bin/env python3
"""Download the official TodoMVC React build and serve it locally.

Useful when todomvc.com is unreachable (offline, firewall, CI) or when you need
a pinned, reproducible version of the application under test.

    python scripts/serve_app.py            # http://127.0.0.1:7002/
"""
import functools
import http.server
import subprocess
import sys
from pathlib import Path

REPO = "https://github.com/tastejs/todomvc.git"
COMMIT = "ff43b02e59dfa604386bb382034b2cd07c2bcd8a"
PORT = 7002
CHECKOUT = Path(__file__).resolve().parent.parent / ".app"


def git(*args):
    subprocess.run(["git", "-C", str(CHECKOUT), *args], check=True)


def download():
    if (CHECKOUT / "examples/react/dist/index.html").exists():
        return
    CHECKOUT.mkdir(exist_ok=True)
    git("init", "-q")
    git("sparse-checkout", "set", "examples/react/dist")
    git("fetch", "-q", "--depth", "1", "--filter=blob:none", REPO, COMMIT)
    git("checkout", "-q", "FETCH_HEAD")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    download()
    handler = functools.partial(QuietHandler, directory=str(CHECKOUT / "examples/react/dist"))
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler) as server:
        print(f"TodoMVC React running at http://127.0.0.1:{PORT}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()
