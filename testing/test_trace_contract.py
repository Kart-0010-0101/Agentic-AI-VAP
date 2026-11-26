"""Test trace.jsonl key schema and step sequence across all three tracks."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from capstone_1_iot.agent import run_agent as run_iot
from capstone_2_5g.agent import run_agent as run_5g
from capstone_3_research.agent import run_agent as run_research

REQUIRED_KEYS = {"step", "thought", "tool", "args", "status", "observation", "elapsed_ms"}
VALID_STATUSES = {"ok", "error", "recovered"}


def test_trace_contract_across_all_tracks(tmp_path: Path):
    root = Path(__file__).resolve().parent.parent
    tracks = [
        ("capstone_1_iot", run_iot, "Verify IoT trace schema"),
        ("capstone_2_5g", run_5g, "Verify 5G trace schema"),
        ("capstone_3_research", run_research, "Verify research trace schema"),
    ]
    for folder, runner, goal in tracks:
        w = tmp_path / folder
        shutil.copytree(root / folder / "data", w / "data")
        runner(goal, workdir=w, mock_llm=True)
        lines = (w / "trace.jsonl").read_text(encoding="utf-8").splitlines()
        assert len(lines) >= 3
        for expected_step, raw in enumerate(lines, start=1):
            row = json.loads(raw)
            assert REQUIRED_KEYS.issubset(row.keys())
            assert row["step"] == expected_step
            assert row["status"] in VALID_STATUSES
            assert isinstance(row["elapsed_ms"], (int, float)) and row["elapsed_ms"] >= 0
