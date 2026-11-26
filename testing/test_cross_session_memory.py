"""Test cross-session ChromaDB memory step reduction across all three capstones."""

from __future__ import annotations

import shutil
from pathlib import Path
import pytest
from capstone_1_iot.agent import run_agent as run_iot
from capstone_2_5g.agent import run_agent as run_5g
from capstone_3_research.agent import run_agent as run_research


@pytest.mark.parametrize(
    "folder,runner,goal",
    [
        ("capstone_1_iot", run_iot, "Cross-session IoT telemetry fault diagnosis"),
        ("capstone_2_5g", run_5g, "Cross-session 5G NR PRB congestion triage"),
        ("capstone_3_research", run_research, "Cross-session ECE literature benchmark review"),
    ],
)
def test_cross_session_memory_reduces_steps(folder: str, runner, goal: str, tmp_path: Path):
    root = Path(__file__).resolve().parent.parent
    shutil.copytree(root / folder / "data", tmp_path / "data")
    r1 = runner(goal, workdir=tmp_path, mock_llm=True)
    r2 = runner(goal, workdir=tmp_path, mock_llm=True)
    assert r2["recalled"] >= 1
    assert r2["steps"] < r1["steps"]
