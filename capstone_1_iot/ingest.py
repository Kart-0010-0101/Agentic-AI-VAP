"""Capstone 1 (IoT Fleet): Idempotent domain knowledge ingestion."""

from __future__ import annotations

from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent


def ingest_domain_kb(data_dir: Path | None = None, db_dir: Path | None = None) -> int:
    data_dir = data_dir or (BASE_DIR / "data")
    db_dir = db_dir or (BASE_DIR / "capstone_memory")
    db_dir.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(db_dir))
    col = client.get_or_create_collection("iot_specs")
    docs, ids, metas = [], [], []
    for p in sorted(data_dir.glob("*.md")):
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
            clean = line.strip()
            if len(clean) > 10:
                docs.append(clean)
                ids.append(f"{p.name}::{i}")
                metas.append({"source": p.name})
    if docs:
        col.upsert(documents=docs, ids=ids, metadatas=metas)
    return col.count()


if __name__ == "__main__":
    print(f"Indexed {ingest_domain_kb()} IoT spec rules.")
