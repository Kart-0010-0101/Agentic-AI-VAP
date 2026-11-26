# Day 1 — Agentic Foundations, Toolchain & Semantic Vectors

Welcome to Day 1 of the **5-Day Value Added Program: Autonomous Agentic AI & Vector RAG Systems** (Department of ECE, Acharya Institute of Technology).

## Contents
- `pyproject.toml` / `uv.lock` — Reproducible Python 3.13 environment (`chromadb`, `python-dotenv`, `qrcode`, `pytest`)
- `.env.example` — Template for your local `GROQ_API_KEY` (never commit `.env`)
- `verify.py` — Preflight HTTPS connectivity & ChromaDB check
- `chroma_demo.py` — Zero-keyword semantic proximity search lab using 384-dim ONNX embeddings
- `live_poll/` — Anonymous mobile-first classroom polling server (`poll_server.py`, `Dockerfile`, `test_poll.py`)
- `render.yaml` — Permanent free-tier Render Blueprint for `live_poll/` (Basic Auth protected `/present` & `/api/admin`)

## Quick Start
```powershell
uv sync
Copy-Item .env.example .env
# Add your GROQ_API_KEY in .env
uv run python verify.py
uv run python chroma_demo.py
```

## Classroom Live Poll (Permanent Cloud or Local)
- Deploy branch `day-1` on **Render.com** (Free Docker Web Service via `render.yaml`).
- **Instructor Presenter Login**: username `ECE` / password `december30` (on `/present` and `/api/admin`).
- **Student Voting Route**: `/vote` (100% anonymous, works across mobile 4G/5G & any Wi-Fi, 100+ concurrent capacity).
```powershell
uv run python live_poll/poll_server.py --port 8765
uv run pytest live_poll/test_poll.py -v
```
