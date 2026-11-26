"""Test chunk overlap, idempotent upsert, and grounded citations."""

from __future__ import annotations

from pathlib import Path
from ingest import chunk_text, ingest_directory
from query import retrieve_context, synthesize_answer


def test_chunk_overlap_preserves_boundary():
    sample = " ".join(f"word{i}" for i in range(150))
    chunks = chunk_text(sample, chunk_size=200, overlap=40)
    assert len(chunks) >= 3
    # Verify tail of chunk 0 overlaps head of chunk 1
    assert any(tok in chunks[1] for tok in chunks[0].split()[-4:])


def test_ingest_is_idempotent(tmp_path: Path):
    kb = Path(__file__).resolve().parent / "knowledge_base"
    db = tmp_path / "chroma_test"
    first_count = ingest_directory(kb_dir=kb, db_dir=db)
    second_count = ingest_directory(kb_dir=kb, db_dir=db)
    assert first_count > 0
    assert first_count == second_count


def test_retrieval_hits_irf540n_and_cites_source(tmp_path: Path):
    kb = Path(__file__).resolve().parent / "knowledge_base"
    db = tmp_path / "chroma_test"
    ingest_directory(kb_dir=kb, db_dir=db)

    hits = retrieve_context("What is the maximum drain-source voltage Vds of IRF540N MOSFET?", db_dir=db, top_k=3)
    assert hits, "Expected at least one semantic match"
    assert hits[0]["source"] == "irf540n_mosfet.md"
    assert "100 V" in hits[0]["text"]

    ans = synthesize_answer("What is max Vds of IRF540N?", hits, mock_llm=True)
    assert "[irf540n_mosfet.md]" in ans
