"""Save and read short After-Action Review lessons across runs in ChromaDB."""

from __future__ import annotations

import hashlib
from pathlib import Path
import chromadb


class EpisodicMemory:
    """Keep short one-sentence lessons across cold restarts."""

    def __init__(self, db_dir: Path, collection_name: str = "episodic_aar") -> None:
        db_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(db_dir))
        self.collection = self.client.get_or_create_collection(collection_name)

    def store_aar(self, goal: str, lesson: str, steps_taken: int, outcome: str) -> str:
        clean_lesson = " ".join(lesson.split())[:320]
        doc_id = "aar_" + hashlib.sha1(goal.encode("utf-8")).hexdigest()[:12]
        self.collection.upsert(
            documents=[f"Goal: {goal[:120]} | Lesson: {clean_lesson}"],
            ids=[doc_id],
            metadatas=[{"category": "aar_lesson", "steps": steps_taken, "outcome": outcome}],
        )
        return doc_id

    def recall(self, goal: str, top_k: int = 2, max_distance: float = 1.50) -> list[dict]:
        total = self.collection.count()
        if total == 0:
            return []
        res = self.collection.query(
            query_texts=[goal],
            n_results=min(top_k, total),
            include=["documents", "metadatas", "distances"],
        )
        matches = []
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            if dist <= max_distance:
                matches.append({"lesson": doc, "distance": round(float(dist), 4), "meta": meta})
        return matches
