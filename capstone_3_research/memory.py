"""Capstone 3 (Research): Persistent episodic memory wrapper."""

from __future__ import annotations

import hashlib
from pathlib import Path
import chromadb


class EpisodicMemory:
    def __init__(self, db_dir: Path) -> None:
        db_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(db_dir))
        self.col = self.client.get_or_create_collection("research_episodic_aar")

    def store_aar(self, goal: str, lesson: str, steps: int) -> str:
        doc_id = "aar_" + hashlib.sha1(goal.encode("utf-8")).hexdigest()[:12]
        self.col.upsert(
            documents=[f"Goal: {goal[:120]} | Lesson: {' '.join(lesson.split())[:260]}"],
            ids=[doc_id],
            metadatas=[{"category": "aar_lesson", "steps": steps}],
        )
        return doc_id

    def recall(self, goal: str, top_k: int = 2, max_distance: float = 1.55) -> list[dict]:
        total = self.col.count()
        if total == 0:
            return []
        res = self.col.query(query_texts=[goal], n_results=min(top_k, total), include=["documents", "distances"])
        return [
            {"lesson": doc, "distance": round(float(dist), 4)}
            for doc, dist in zip(res["documents"][0], res["distances"][0])
            if dist <= max_distance
        ]
