"""Day 3: Defensive typed Python tools with structured error hints for self-healing."""

from __future__ import annotations

import json
from pathlib import Path
from query import retrieve_context


def _resolve_safe(workdir: Path, rel_path: str) -> Path:
    target = (workdir / rel_path).resolve()
    root = workdir.resolve()
    if root not in target.parents and target != root:
        raise PermissionError(f"Path '{rel_path}' escapes workspace root")
    return target


def list_dir(workdir: Path, directory: str = ".") -> dict:
    """List files and folders inside workdir safely."""
    try:
        target = _resolve_safe(workdir, directory)
        if not target.exists():
            return {"ok": False, "error": "FileNotFoundError", "detail": f"Directory '{directory}' not found."}
        entries = sorted(p.name + ("/" if p.is_dir() else "") for p in target.iterdir())
        return {"ok": True, "directory": directory, "entries": entries}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}


def read_file(workdir: Path, filepath: str) -> dict:
    """Read a text or JSON file, returning directory hints on FileNotFoundError."""
    try:
        target = _resolve_safe(workdir, filepath)
        if not target.is_file():
            data_dir = workdir / "data"
            hints = sorted(f"data/{p.name}" for p in data_dir.iterdir()) if data_dir.is_dir() else []
            return {
                "ok": False,
                "error": "FileNotFoundError",
                "detail": f"Missing file '{filepath}'.",
                "hints": hints,
            }
        raw = target.read_text(encoding="utf-8")
        if target.suffix.lower() == ".json":
            parsed = json.loads(raw)
            return {"ok": True, "filepath": filepath, "records": parsed}
        return {"ok": True, "filepath": filepath, "content": raw[:2000]}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}


def search_kb(workdir: Path, query_text: str) -> dict:
    """Search the local ChromaDB knowledge base."""
    try:
        hits = retrieve_context(query_text, db_dir=workdir / "chroma_db", top_k=2)
        return {"ok": True, "hits": hits}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}


def write_report(workdir: Path, filepath: str, content: str) -> dict:
    """Write a clean Markdown/text report inside workdir."""
    try:
        target = _resolve_safe(workdir, filepath)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"ok": True, "filepath": filepath, "bytes_written": len(content.encode("utf-8"))}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}


TOOL_REGISTRY = {
    "list_dir": list_dir,
    "read_file": read_file,
    "search_kb": search_kb,
    "write_report": write_report,
}
