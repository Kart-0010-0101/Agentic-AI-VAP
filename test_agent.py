"""Test ReAct self-healing, cross-session speedup, and loop step caps."""

from __future__ import annotations

import json
from pathlib import Path
from agent import run_agent


def test_self_healing_and_cross_session_speedup(tmp_path: Path):
    goal = "Audit IoT thermal anomalies and save out/audit_report.md"
    mem_dir = tmp_path / "mem"

    r1 = run_agent(goal, workdir=tmp_path, db_dir=mem_dir, trace_path=tmp_path / "t1.jsonl", mock_llm=True)
    trace1 = [json.loads(line) for line in (tmp_path / "t1.jsonl").read_text(encoding="utf-8").splitlines()]
    statuses1 = [row["status"] for row in trace1]
    assert "error" in statuses1
    assert "recovered" in statuses1
    assert (tmp_path / "out" / "audit_report.md").exists()

    # Cold process simulation: new trace file, same ChromaDB episodic memory
    r2 = run_agent(goal, workdir=tmp_path, db_dir=mem_dir, trace_path=tmp_path / "t2.jsonl", mock_llm=True)
    assert r2["recalled_precedents"] >= 1
    assert r2["steps"] < r1["steps"], f"Expected speedup, got Run1={r1['steps']} vs Run2={r2['steps']}"


def test_max_steps_prevents_infinite_loop(tmp_path: Path):
    r = run_agent("Audit IoT telemetry", workdir=tmp_path, db_dir=tmp_path / "mem2", trace_path=tmp_path / "t_cap.jsonl", max_steps=2, mock_llm=True)
    assert r["steps"] == 2
