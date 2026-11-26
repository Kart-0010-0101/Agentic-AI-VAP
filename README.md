# Day 1 — Toolchain Setup, Vectors, and Live Poll

Welcome to Day 1 of the **5-Day Value Added Program** (Department of ECE, Acharya Institute of Technology).

## Files in This Branch
- `pyproject.toml` and `uv.lock` — Pinned Python 3.13 packages (`chromadb`, `python-dotenv`, `qrcode`, `pytest`)
- `.env.example` — Sample file for your `GROQ_API_KEY`. Never commit `.env`.
- `verify.py` — Script that checks Groq HTTPS access and ChromaDB install.
- `chroma_demo.py` — Vector search lab with 384-D local ONNX embeddings.
- `live_poll/` — Classroom poll server (`poll_server.py`, `Dockerfile`, `test_poll.py`).
- `render.yaml` — Free Render setup file for `live_poll/`.

## Run Locally
```powershell
uv sync
Copy-Item .env.example .env
# Put your GROQ_API_KEY in .env
uv run python verify.py
uv run python chroma_demo.py
```

## Run the Live Poll (Cloud or Class Wi-Fi)
- Deploy branch `day-1` on **Render.com** with `python live_poll/poll_server.py`.
- Login prompt opens immediately on `/` and `/vote` (student username `ECE`, password `december30`).
- Projector display (`/present`), QR image (`/qr.png`), and admin controls (`/api/admin`) require instructor credentials (`ECEKART` / `WasteOfTimeGG`).
- Supports 100 concurrent phones across mobile data and any Wi-Fi.
```powershell
uv run python live_poll/poll_server.py --port 8765
uv run pytest live_poll/test_poll.py -v
```
