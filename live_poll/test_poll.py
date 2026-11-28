"""Test dual-credential Basic Auth split, poll controls, and 100 concurrent votes."""

import base64
from concurrent.futures import ThreadPoolExecutor
import json
import threading
import urllib.error
import urllib.request

from poll_server import create_server


def _req(url: str, method: str = "GET", payload: dict | None = None, auth: tuple[str, str] | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    if auth is not None:
        token = base64.b64encode(f"{auth[0]}:{auth[1]}".encode("utf-8")).decode("ascii")
        headers["Authorization"] = f"Basic {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.headers.get("Content-Type", ""), resp.read()


def _expect_401(url: str, method: str = "GET", payload: dict | None = None, auth: tuple[str, str] | None = None):
    try:
        _req(url, method=method, payload=payload, auth=auth)
        raise AssertionError(f"Expected 401 on {method} {url} with auth={auth}")
    except urllib.error.HTTPError as exc:
        assert exc.code == 401


def test_live_poll_dual_basic_auth_and_end_to_end():
    server, _, _ = create_server(host="127.0.0.1", port=0)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"
    student = ("ECE", "december30")
    admin = ("ECEKART", "30december2222")
    try:
        # Health probe works without auth for Render platform checks
        st, ct, _ = _req(base + "/health")
        assert st == 200 and "application/json" in ct

        # Missing auth and wrong password get 401 on all protected routes
        all_protected = [
            ("/", "GET", None),
            ("/vote", "GET", None),
            ("/poll", "GET", None),
            ("/present", "GET", None),
            ("/qr.png", "GET", None),
            ("/api/state", "GET", None),
            ("/api/vote", "POST", {"poll_id": 1, "option_idx": 0}),
            ("/api/admin", "POST", {"action": "next"}),
        ]
        for path, method, payload in all_protected:
            _expect_401(base + path, method=method, payload=payload)
            _expect_401(base + path, method=method, payload=payload, auth=("ECE", "wrong"))

        # Student credentials must be rejected on instructor/admin and unknown routes
        for path, method, payload in [
            ("/poll", "GET", None),
            ("/present", "GET", None),
            ("/qr.png", "GET", None),
            ("/api/admin", "POST", {"action": "next"}),
            ("/other", "GET", None),
        ]:
            _expect_401(base + path, method=method, payload=payload, auth=student)

        # Student credentials unlock student routes and shared vote UI assets
        for path, ctype_hint in [("/", "text/html"), ("/vote", "text/html"), ("/style.css", "text/css")]:
            st, ct, body = _req(base + path, auth=student)
            assert st == 200 and ctype_hint in ct and len(body) > 50

        # Instructor credentials unlock projector routes as well as /, /vote, /style.css, /api/state
        for path, ctype_hint in [
            ("/poll", "text/html"),
            ("/present", "text/html"),
            ("/", "text/html"),
            ("/vote", "text/html"),
            ("/style.css", "text/css"),
        ]:
            st, ct, body = _req(base + path, auth=admin)
            assert st == 200 and ctype_hint in ct and len(body) > 50

        st, ct, qr_bytes = _req(base + "/qr.png", auth=admin)
        assert st == 200 and ct == "image/png" and qr_bytes.startswith(b"\x89PNG")

        # 100 concurrent authenticated phones vote safely with student credentials
        def _cast(i: int) -> int:
            status, _, _ = _req(
                base + "/api/vote",
                method="POST",
                payload={"poll_id": 1, "option_idx": i % 3},
                auth=student,
            )
            return status

        with ThreadPoolExecutor(max_workers=25) as pool:
            statuses = list(pool.map(_cast, range(100)))
        assert all(s == 200 for s in statuses)

        st, _, raw = _req(base + "/api/state", auth=student)
        state = json.loads(raw)
        assert st == 200 and state["poll"]["total_votes"] == 100 and sum(state["poll"]["counts"]) == 100

        st, _, raw = _req(base + "/api/state", auth=admin)
        assert st == 200 and json.loads(raw)["poll"]["total_votes"] == 100

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "next"}, auth=admin)
        assert st == 200 and json.loads(raw)["poll"]["id"] == 2

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "prev"}, auth=admin)
        assert st == 200 and json.loads(raw)["poll"]["id"] == 1

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "reset"}, auth=admin)
        assert st == 200 and json.loads(raw)["poll"]["total_votes"] == 0
    finally:
        server.shutdown()
        server.server_close()
