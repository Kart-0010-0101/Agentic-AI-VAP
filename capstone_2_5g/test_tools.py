"""Capstone 2 (5G NR): Test KPI quarantine, path recovery, and memory recall."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from capstone_2_5g.agent import run_agent
from capstone_2_5g.tools import read_kpis


def test_5g_quarantines_corrupt_and_recovers(tmp_path: Path):
    shutil.copytree(Path(__file__).resolve().parent / "data", tmp_path / "data")
    goal = "Triage 5G NR cell PRB congestion and interference."
    r1 = run_agent(goal, workdir=tmp_path, mock_llm=True)
    trace1 = [json.loads(line) for line in (tmp_path / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(row["status"] == "error" for row in trace1)
    assert any(row["status"] == "recovered" for row in trace1)
    assert (tmp_path / "out" / "nr_report.md").exists()

    r2 = run_agent(goal, workdir=tmp_path, mock_llm=True)
    assert r2["recalled"] >= 1
    assert r2["steps"] < r1["steps"]

    (tmp_path / "data" / "nan_kpis.json").write_text('[{"cell_id": "C1", "prb_pct": "bad", "sinr_db": 10, "bler_pct": 1}]', encoding="utf-8")
    res = read_kpis(tmp_path, "data/nan_kpis.json")
    assert res["ok"] is True and len(res["quarantined"]) == 1
