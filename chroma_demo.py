"""Search short ECE sentences by meaning with ChromaDB."""

from __future__ import annotations

import chromadb


def run_demo() -> dict:
    client = chromadb.Client()
    collection = client.get_or_create_collection("day1_semantic_demo")
    collection.upsert(
        documents=[
            "The MOSFET gate voltage controls the channel drain current.",
            "A capacitor stores electrostatic energy inside an electric field.",
            "Python uses indentation cleanly to delimit code blocks.",
        ],
        ids=["doc1", "doc2", "doc3"],
    )
    results = collection.query(
        query_texts=["How does a transistor work?"],
        n_results=3,
        include=["documents", "distances"],
    )
    return results


if __name__ == "__main__":
    res = run_demo()
    print("Query: 'How does a transistor work?'")
    for doc, dist in zip(res["documents"][0], res["distances"][0]):
        print(f"  dist={dist:.3f} | {doc}")
