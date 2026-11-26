"""Day 2: Idempotent sliding-window chunking and ChromaDB ingestion pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
import chromadb

DEFAULT_KB_DIR = Path(__file__).resolve().parent / "knowledge_base"
DEFAULT_DB_DIR = Path(__file__).resolve().parent / "chroma_db"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping character chunks."""
    clean = " ".join(text.split())
    if not clean:
        return []
    if len(clean) <= chunk_size:
        return [clean]

    step = max(1, chunk_size - overlap)
    chunks: list[str] = []
    for start in range(0, len(clean), step):
        piece = clean[start : start + chunk_size].strip()
        if piece:
            chunks.append(piece)
        if start + chunk_size >= len(clean):
            break
    return chunks


def ingest_directory(
    kb_dir: Path = DEFAULT_KB_DIR,
    db_dir: Path = DEFAULT_DB_DIR,
    collection_name: str = "ece_knowledge",
    chunk_size: int = 500,
    overlap: int = 50,
) -> int:
    """Ingest all .md/.txt files in kb_dir into persistent ChromaDB using idempotent upsert."""
    db_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_or_create_collection(collection_name)

    docs, ids, metas = [], [], []
    for path in sorted(kb_dir.glob("*")):
        if path.suffix.lower() not in {".md", ".txt"} or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for idx, chunk in enumerate(chunk_text(text, chunk_size=chunk_size, overlap=overlap)):
            docs.append(chunk)
            ids.append(f"{path.name}::chunk_{idx}")
            metas.append({"source": path.name, "chunk_index": idx})

    if docs:
        collection.upsert(documents=docs, ids=ids, metadatas=metas)
    return collection.count()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest ECE knowledge base into ChromaDB.")
    parser.add_argument("--kb-dir", type=Path, default=DEFAULT_KB_DIR)
    parser.add_argument("--db-dir", type=Path, default=DEFAULT_DB_DIR)
    args = parser.parse_args()

    total = ingest_directory(args.kb_dir, args.db_dir)
    print(f"Ingestion complete. Collection 'ece_knowledge' now holds {total} chunks.")


if __name__ == "__main__":
    main()
