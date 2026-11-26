"""Grade Project 1 RAG: check idempotent upsert and retrieval accuracy."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def grade_project1(repo_dir: Path) -> dict:
    """Test ingest.py idempotency & query retrieval in an isolated subprocess."""
    ingest_py = repo_dir / "ingest.py"
    query_py = repo_dir / "query.py"
    if not (ingest_py.is_file() and query_py.is_file()):
        return {"ran": False, "idempotent": False, "retrieval_ok": False}

    probe = """
import json, tempfile
from pathlib import Path
import ingest, query

tmp = Path(tempfile.mkdtemp(prefix="rag_probe_"))
kb = Path("knowledge_base")
c1 = ingest.ingest_directory(kb_dir=kb, db_dir=tmp / "db")
c2 = ingest.ingest_directory(kb_dir=kb, db_dir=tmp / "db")
hits = query.retrieve_context("What is the max Vds of IRF540N MOSFET?", db_dir=tmp / "db", top_k=3)
print(json.dumps({
    "ran": True,
    "idempotent": c1 > 0 and c1 == c2,
    "retrieval_ok": bool(hits and "irf540n" in hits[0].get("source", "").lower()),
}))
"""
    res = subprocess.run([sys.executable, "-c", probe], cwd=repo_dir, capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        return {"ran": True, "idempotent": False, "retrieval_ok": False, "error": res.stderr[-300:]}
    try:
        return json.loads(res.stdout.strip().splitlines()[-1])
    except Exception:
        return {"ran": True, "idempotent": False, "retrieval_ok": False}
