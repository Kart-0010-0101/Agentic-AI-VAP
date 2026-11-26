"""Retrieve matching ECE chunks from ChromaDB and write cited replies."""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path
import chromadb
from dotenv import load_dotenv

DEFAULT_DB_DIR = Path(__file__).resolve().parent / "chroma_db"


def retrieve_context(
    question: str,
    db_dir: Path = DEFAULT_DB_DIR,
    top_k: int = 3,
    max_distance: float = 1.65,
    collection_name: str = "ece_knowledge",
) -> list[dict]:
    """Query ChromaDB and keep chunks within the max distance cap."""
    if not question.strip():
        return []
    client = chromadb.PersistentClient(path=str(db_dir))
    collection = client.get_or_create_collection(collection_name)
    count = collection.count()
    if count == 0:
        return []

    res = collection.query(
        query_texts=[question],
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"],
    )
    hits: list[dict] = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        if dist <= max_distance:
            hits.append({"source": meta.get("source", "unknown"), "distance": round(float(dist), 4), "text": doc})
    return hits


def synthesize_answer(question: str, chunks: list[dict], mock_llm: bool = False) -> str:
    """Write a cited answer using only retrieved text chunks."""
    if not chunks:
        return "Insufficient evidence in the indexed knowledge base to answer that question."

    context_block = "\n\n".join(f"[{c['source']}] (dist={c['distance']}): {c['text']}" for c in chunks)
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY", "").strip()

    if mock_llm or not api_key or api_key == "gsk_replace_with_your_real_key":
        top = chunks[0]
        return f"Grounded Answer (from [{top['source']}], dist={top['distance']}):\n{top['text']}"

    payload = json.dumps({
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Answer strictly using the provided technical context. "
                    "Cite the source filename in brackets, e.g. [irf540n_mosfet.md]. "
                    "If context is missing, say 'Insufficient evidence'."
                ),
            },
            {"role": "user", "content": f"Context:\n{context_block}\n\nQuestion: {question}"},
        ],
        "temperature": 0.1,
        "max_tokens": 350,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Query ECE Vector RAG pipeline.")
    parser.add_argument("question", type=str)
    parser.add_argument("--db-dir", type=Path, default=DEFAULT_DB_DIR)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--mock-llm", action="store_true")
    args = parser.parse_args()

    chunks = retrieve_context(args.question, db_dir=args.db_dir, top_k=args.top_k)
    print(f"Retrieved {len(chunks)} chunks:")
    for c in chunks:
        print(f" - [{c['source']}] dist={c['distance']}")
    print("\n" + synthesize_answer(args.question, chunks, mock_llm=args.mock_llm))


if __name__ == "__main__":
    main()
