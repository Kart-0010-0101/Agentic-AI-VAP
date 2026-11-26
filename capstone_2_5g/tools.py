"""Capstone 2 (5G NR): Four sandboxed radio KPI tools."""

from __future__ import annotations

import json
import math
from pathlib import Path
import chromadb


def list_dir(workdir: Path, directory: str = ".") -> dict:
    try:
        target = (workdir / directory).resolve()
        if workdir.resolve() not in target.parents and target != workdir.resolve():
            return {"ok": False, "error": "PermissionError", "detail": "Path escapes workspace."}
        if not target.is_dir():
            return {"ok": False, "error": "FileNotFoundError", "detail": f"Missing directory '{directory}'."}
        return {"ok": True, "entries": sorted(p.name + ("/" if p.is_dir() else "") for p in target.iterdir())}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}


def read_kpis(workdir: Path, filepath: str) -> dict:
    try:
        target = (workdir / filepath).resolve()
        if not target.is_file():
            data_dir = workdir / "data"
            hints = sorted(f"data/{p.name}" for p in data_dir.iterdir()) if data_dir.is_dir() else []
            return {"ok": False, "error": "FileNotFoundError", "detail": f"Missing '{filepath}'.", "hints": hints}
        raw = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return {"ok": False, "error": "SchemaError", "detail": "Expected JSON array of cell KPIs."}
        valid, quarantined = [], []
        for idx, row in enumerate(raw):
            if not isinstance(row, dict) or "cell_id" not in row:
                quarantined.append({"index": idx, "reason": "malformed_row"})
                continue
            vals = [row.get("prb_pct", 0), row.get("sinr_db", 0), row.get("bler_pct", 0)]
            if any(not isinstance(v, (int, float)) or math.isnan(float(v)) for v in vals):
                quarantined.append({"index": idx, "cell_id": row.get("cell_id"), "reason": "NaN_or_non_numeric"})
                continue
            valid.append(row)
        return {"ok": True, "filepath": filepath, "records": valid, "quarantined": quarantined}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}


def query_sla(workdir: Path, query_text: str) -> dict:
    try:
        client = chromadb.PersistentClient(path=str(workdir / "capstone_memory"))
        col = client.get_or_create_collection("nr_specs")
        if col.count() == 0:
            return {"ok": True, "hits": []}
        res = col.query(query_texts=[query_text], n_results=min(2, col.count()), include=["documents", "distances"])
        return {"ok": True, "hits": [{"text": d, "distance": round(float(dist), 4)} for d, dist in zip(res["documents"][0], res["distances"][0])]}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}


def write_report(workdir: Path, filepath: str, content: str) -> dict:
    try:
        target = (workdir / filepath).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"ok": True, "filepath": filepath, "bytes_written": len(content.encode("utf-8"))}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)}


TOOL_REGISTRY = {
    "list_dir": list_dir,
    "read_kpis": read_kpis,
    "query_sla": query_sla,
    "write_report": write_report,
}
