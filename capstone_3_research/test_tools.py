"""Capstone 3 (Research): Test path recovery, null quarantine, and memory speedup."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from capstone_3_research.agent import run_agent
from capstone_3_research.tools import read_papers


def test_research_synthesis_self_heal_and_recall(tmp_path: Path):
    shutil.copytree(Path(__file__).resolve().parent / "data", tmp_path / "data")
    goal = "Synthesize edge ECE literature benchmarks and flag production studies."
    r1 = run_agent(goal, workdir=tmp_path, mock_llm=True)
    trace1 = [json.loads(line) for line in (tmp_path / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(row["status"] == "error" for row in trace1)
    assert any(row["status"] == "recovered" for row in trace1)
    assert (tmp_path / "out" / "research_report.md").exists()

    r2 = run_agent(goal, workdir=tmp_path, mock_llm=True)
    assert r2["recalled"] >= 1
    assert r2["steps"] < r1["steps"]

    (tmp_path / "data" / "nan_paper.json").write_text('[{"paper_id": "P1", "latency_ms": null, "f1_score": 0.9}]', encoding="utf-8")
    res = read_papers(tmp_path, "data/nan_paper.json")
    assert res["ok"] is True and len(res["quarantined"]) == 1
