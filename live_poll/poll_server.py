"""Minimalist anonymous mobile classroom poll server (pure Python stdlib).

Serves a mobile-first student voting view (/vote), a live projector chart
view (/present), REST endpoints (/api/state, /api/vote, /api/admin), and a
scannable QR PNG (/qr.png) on a pure white (#FFFFFF) taste-skill surface.
"""

from __future__ import annotations

import argparse
from functools import partial
import io
import json
import mimetypes
from pathlib import Path
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

STATIC_DIR = Path(__file__).resolve().parent / "static"

DEFAULT_POLLS = [
    {
        "id": 1,
        "tag": "POLL 1 OF 3",
        "question": "Have you used ChatGPT, Gemini, or Claude for coursework or coding?",
        "options": ["Yes, regularly", "A few times", "Not yet"],
    },
    {
        "id": 2,
        "tag": "POLL 2 OF 3",
        "question": "Have you written a Python script that calls an AI API (Groq, OpenAI, or Gemini)?",
        "options": ["Yes", "Tried, hit errors", "Never"],
    },
    {
        "id": 3,
        "tag": "POLL 3 OF 3",
        "question": (
            "Have you built an AI that executes 4+ independent steps, catches its own error, "
            "consults memory, and finishes without a second prompt?"
        ),
        "options": ["Yes", "Partially", "Not yet"],
    },
]


def detect_lan_ip() -> str:
    """Best-effort LAN IPv4 address for classroom Wi-Fi/hotspot QR scanning."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def render_qr_png(url: str) -> bytes:
    """Render crisp #0F172A-on-#FFFFFF QR PNG bytes for `url`."""
    import qrcode
    from qrcode.constants import ERROR_CORRECT_M

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=12,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class PollStore:
    """Thread-safe in-memory + optional JSON-file state for classroom polls."""

    def __init__(self, state_file: Path | None = None, join_url: str = "http://127.0.0.1:8765/vote"):
        self._lock = threading.Lock()
        self._state_file = state_file
        self.join_url = join_url
        self.polls = [dict(p) for p in DEFAULT_POLLS]
        self.current_idx = 0
        self.reveal_results = True
        self.counts: dict[int, list[int]] = {
            p["id"]: [0] * len(p["options"]) for p in self.polls
        }
        if self._state_file and self._state_file.exists():
            self._load()

    def _load(self) -> None:
        try:
            raw = json.loads(self._state_file.read_text(encoding="utf-8"))
            self.current_idx = max(0, min(int(raw.get("current_idx", 0)), len(self.polls) - 1))
            self.reveal_results = bool(raw.get("reveal_results", True))
            saved_counts = raw.get("counts", {})
            for p in self.polls:
                pid = p["id"]
                vals = saved_counts.get(str(pid), saved_counts.get(pid))
                if isinstance(vals, list) and len(vals) == len(p["options"]):
                    self.counts[pid] = [max(0, int(v)) for v in vals]
        except Exception:
            pass

    def _save(self) -> None:
        if not self._state_file:
            return
        payload = {
            "current_idx": self.current_idx,
            "reveal_results": self.reveal_results,
            "counts": {str(k): v for k, v in self.counts.items()},
        }
        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def snapshot(self) -> dict:
        with self._lock:
            poll = self.polls[self.current_idx]
            pid = poll["id"]
            c = list(self.counts[pid])
            return {
                "current_idx": self.current_idx,
                "total_polls": len(self.polls),
                "reveal_results": self.reveal_results,
                "join_url": self.join_url,
                "poll": {
                    "id": pid,
                    "tag": poll["tag"],
                    "question": poll["question"],
                    "options": list(poll["options"]),
                    "counts": c,
                    "total_votes": sum(c),
                },
            }

    def vote(self, poll_id: int, option_idx: int) -> tuple[bool, str, dict]:
        with self._lock:
            target = next((p for p in self.polls if p["id"] == poll_id), None)
            if not target:
                return False, "Unknown poll_id", {}
            if not (0 <= option_idx < len(target["options"])):
                return False, "Invalid option_idx", {}
            self.counts[poll_id][option_idx] += 1
            self._save()
        return True, "Recorded", self.snapshot()

    def admin(self, action: str, poll_idx: int | None = None) -> tuple[bool, str, dict]:
        with self._lock:
            if action == "next":
                self.current_idx = min(len(self.polls) - 1, self.current_idx + 1)
            elif action == "prev":
                self.current_idx = max(0, self.current_idx - 1)
            elif action == "toggle_reveal":
                self.reveal_results = not self.reveal_results
            elif action == "reset":
                pid = self.polls[self.current_idx]["id"]
                self.counts[pid] = [0] * len(self.polls[self.current_idx]["options"])
            elif action == "set_poll" and poll_idx is not None:
                if 0 <= poll_idx < len(self.polls):
                    self.current_idx = poll_idx
                else:
                    return False, "poll_idx out of range", {}
            else:
                return False, f"Unknown admin action: {action}", {}
            self._save()
        return True, "OK", self.snapshot()


class PollRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, store: PollStore, qr_bytes: bytes, **kwargs):
        self.store = store
        self.qr_bytes = qr_bytes
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args) -> None:
        return  # Keep console clean during live lectures

    def _send_bytes(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict) -> None:
        self._send_bytes(status, "application/json; charset=utf-8", json.dumps(payload).encode("utf-8"))

    def _read_json_body(self) -> dict | None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def _serve_static(self, filename: str) -> None:
        path = (STATIC_DIR / filename).resolve()
        if not path.is_file() or STATIC_DIR.resolve() not in path.parents:
            self._send_json(404, {"error": "Not found"})
            return
        mime, _ = mimetypes.guess_type(str(path))
        self._send_bytes(200, f"{mime or 'text/html'}; charset=utf-8", path.read_bytes())

    def do_GET(self) -> None:
        route = urlparse(self.path).path
        if route in ("/", "/vote"):
            self._serve_static("vote.html")
        elif route == "/present":
            self._serve_static("present.html")
        elif route == "/style.css":
            self._serve_static("style.css")
        elif route == "/qr.png":
            self._send_bytes(200, "image/png", self.qr_bytes)
        elif route == "/api/state":
            self._send_json(200, self.store.snapshot())
        else:
            self._send_json(404, {"error": "Route not found"})

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        data = self._read_json_body()
        if data is None:
            self._send_json(400, {"error": "Invalid JSON payload"})
            return

        if route == "/api/vote":
            try:
                poll_id = int(data["poll_id"])
                opt_idx = int(data["option_idx"])
            except (KeyError, TypeError, ValueError):
                self._send_json(400, {"error": "poll_id and option_idx integers required"})
                return
            ok, msg, snap = self.store.vote(poll_id, opt_idx)
            self._send_json(200 if ok else 400, snap if ok else {"error": msg})
        elif route == "/api/admin":
            action = str(data.get("action", ""))
            poll_idx = data.get("poll_idx")
            ok, msg, snap = self.store.admin(action, int(poll_idx) if poll_idx is not None else None)
            self._send_json(200 if ok else 400, snap if ok else {"error": msg})
        else:
            self._send_json(404, {"error": "Route not found"})


def create_server(
    host: str = "0.0.0.0",
    port: int = 8765,
    public_url: str | None = None,
    state_file: Path | None = None,
) -> tuple[ThreadingHTTPServer, PollStore, bytes]:
    lan_ip = detect_lan_ip()
    base = (public_url or f"http://{lan_ip}:{port}").rstrip("/")
    join_url = base if base.endswith("/vote") else f"{base}/vote"
    store = PollStore(state_file=state_file, join_url=join_url)
    qr_bytes = render_qr_png(join_url)
    handler = partial(PollRequestHandler, store=store, qr_bytes=qr_bytes)
    server = ThreadingHTTPServer((host, port), handler)
    actual_port = server.server_address[1]
    if port == 0 and not public_url:
        join_url = f"http://{lan_ip}:{actual_port}/vote"
        store.join_url = join_url
        qr_bytes = render_qr_png(join_url)
        server.RequestHandlerClass = partial(PollRequestHandler, store=store, qr_bytes=qr_bytes)
    return server, store, qr_bytes


def main() -> None:
    parser = argparse.ArgumentParser(description="Anonymous classroom mobile poll server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--public-url", default=None, help="Override base URL for QR (e.g. cloudflare tunnel)")
    parser.add_argument("--state-file", default=None, help="Optional JSON file for vote persistence")
    parser.add_argument("--export-qr", default=None, help="Write QR PNG to path and exit immediately")
    args = parser.parse_args()

    if args.export_qr:
        lan_ip = detect_lan_ip()
        base = (args.public_url or f"http://{lan_ip}:{args.port}").rstrip("/")
        join_url = base if base.endswith("/vote") else f"{base}/vote"
        out = Path(args.export_qr)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(render_qr_png(join_url))
        print(f"Exported QR code for {join_url} -> {out}")
        return

    sf = Path(args.state_file) if args.state_file else None
    server, store, _ = create_server(args.host, args.port, args.public_url, sf)
    print(f"Student vote URL  : {store.join_url}")
    print(f"Projector display : http://127.0.0.1:{args.port}/present")
    print("Press Ctrl+C to stop server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
