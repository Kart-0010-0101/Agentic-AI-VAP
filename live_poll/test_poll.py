"""Test Basic Auth, poll controls, and 100 concurrent student votes."""

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


def test_live_poll_basic_auth_and_end_to_end():
    server, _, _ = create_server(host="127.0.0.1", port=0)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"
    creds = ("ECE", "december30")
    try:
        # Public student & health routes work with no credentials
        for path, ctype_hint in [("/vote", "text/html"), ("/style.css", "text/css"), ("/health", "application/json")]:
            st, ct, body = _req(base + path)
            assert st == 200 and ctype_hint in ct and len(body) > 5

        # Projector & admin endpoints require Basic Auth
        for protected_path, method, payload in [("/present", "GET", None), ("/api/admin", "POST", {"action": "next"})]:
            try:
                _req(base + protected_path, method=method, payload=payload)
                raise AssertionError(f"Expected 401 on {protected_path}")
            except urllib.error.HTTPError as exc:
                assert exc.code == 401

            try:
                _req(base + protected_path, method=method, payload=payload, auth=("ECE", "wrong"))
                raise AssertionError(f"Expected 401 for bad password on {protected_path}")
            except urllib.error.HTTPError as exc:
                assert exc.code == 401

        st, ct, _ = _req(base + "/present", auth=creds)
        assert st == 200 and "text/html" in ct

        st, ct, qr_bytes = _req(base + "/qr.png")
        assert st == 200 and ct == "image/png" and qr_bytes.startswith(b"\x89PNG")

        # Simulate 100 concurrent student phones voting simultaneously across networks
        def _cast(i: int) -> int:
            status, _, _ = _req(
                base + "/api/vote",
                method="POST",
                payload={"poll_id": 1, "option_idx": i % 3},
            )
            return status

        with ThreadPoolExecutor(max_workers=25) as pool:
            statuses = list(pool.map(_cast, range(100)))
        assert all(s == 200 for s in statuses)

        st, _, raw = _req(base + "/api/state")
        state = json.loads(raw)
        assert st == 200 and state["poll"]["total_votes"] == 100
        assert sum(state["poll"]["counts"]) == 100

        # Authorized admin navigation & reset
        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "next"}, auth=creds)
        assert st == 200 and json.loads(raw)["poll"]["id"] == 2

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "prev"}, auth=creds)
        assert st == 200 and json.loads(raw)["poll"]["id"] == 1

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "reset"}, auth=creds)
        assert st == 200 and json.loads(raw)["poll"]["total_votes"] == 0
    finally:
        server.shutdown()
        server.server_close()
