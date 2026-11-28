# Live Classroom Phone Poll (`live-poll`)

Dedicated deployment branch for the anonymous classroom live phone poll web app used in the **5-Day Value Added Program (Department of ECE, Acharya Institute of Technology)**.

## Files in This Branch
- `live_poll/poll_server.py` â€” Threaded Python stdlib HTTP server with dual Basic Auth and QR generator
- `live_poll/static/` â€” Mobile voting view (`vote.html`), projector live chart (`present.html`), and stylesheet (`style.css`)
- `live_poll/Dockerfile` â€” Container image for Render Docker deployment
- `live_poll/test_poll.py` â€” End-to-end auth, admin, and 100-concurrent-vote test suite
- `render.yaml` â€” Render.com Free Docker Web Service specification
- `pyproject.toml` â€” Minimal dependencies (`qrcode[pil]` and `pytest`)

## Run Locally
```powershell
uv sync
uv run python live_poll/poll_server.py --port 8765
uv run pytest live_poll/test_poll.py -v
```

## Render.com Deployment
- Connect branch `live-poll` using Docker (`dockerfilePath: ./live_poll/Dockerfile`, `dockerContext: ./live_poll`, `healthCheckPath: /health`).
- Student routes (`/`, `/vote`) use `POLL_STUDENT_USER` / `POLL_STUDENT_PASS` (default `ECE` / `december30`).
- Instructor/projector routes (`/poll`, `/present`, `/qr.png`, `/api/admin`) use `POLL_ADMIN_USER` / `POLL_ADMIN_PASS` (default `ECEKART` / `30december2222`).
