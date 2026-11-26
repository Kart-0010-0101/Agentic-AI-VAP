"""Automated integration tests for the anonymous live poll server."""

import json
import threading
import urllib.error
import urllib.request

from poll_server import create_server


def _req(url: str, method: str = "GET", payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, resp.headers.get("Content-Type", ""), resp.read()


def test_live_poll_end_to_end():
    server, _, _ = create_server(host="127.0.0.1", port=0)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"
    try:
        for path, ctype_hint in [("/vote", "text/html"), ("/present", "text/html"), ("/style.css", "text/css")]:
            st, ct, body = _req(base + path)
            assert st == 200 and ctype_hint in ct and len(body) > 50

        st, ct, qr_bytes = _req(base + "/qr.png")
        assert st == 200 and ct == "image/png" and qr_bytes.startswith(b"\x89PNG")

        st, _, raw = _req(base + "/api/state")
        state = json.loads(raw)
        assert state["poll"]["id"] == 1 and state["poll"]["total_votes"] == 0

        st, _, raw = _req(base + "/api/vote", method="POST", payload={"poll_id": 1, "option_idx": 1})
        state = json.loads(raw)
        assert st == 200 and state["poll"]["counts"][1] == 1 and state["poll"]["total_votes"] == 1

        try:
            _req(base + "/api/vote", method="POST", payload={"poll_id": 1, "option_idx": 99})
            raise AssertionError("Expected HTTP 400 for invalid option_idx")
        except urllib.error.HTTPError as exc:
            assert exc.code == 400

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "next"})
        assert st == 200 and json.loads(raw)["poll"]["id"] == 2

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "toggle_reveal"})
        assert st == 200 and json.loads(raw)["reveal_results"] is False

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "prev"})
        assert st == 200 and json.loads(raw)["poll"]["id"] == 1

        st, _, raw = _req(base + "/api/admin", method="POST", payload={"action": "reset"})
        assert st == 200 and json.loads(raw)["poll"]["total_votes"] == 0
    finally:
        server.shutdown()
        server.server_close()
