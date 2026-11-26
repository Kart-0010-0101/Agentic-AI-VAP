"""Capstone 1 (IoT Fleet) automated verification suite."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from capstone_1_iot.agent import run_agent
from capstone_1_iot.tools import list_dir, read_telemetry


def test_iot_tools_handle_missing_and_corrupt(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "bad.json").write_text('[{"node_id": "N1", "bus_v": "NaN", "vds_peak_v": 50, "temp_c": 40}]', encoding="utf-8")
    miss = read_telemetry(tmp_path, "nope.json")
    assert miss["ok"] is False and miss["hints"] == ["data/bad.json"]

    res = read_telemetry(tmp_path, "data/bad.json")
    assert res["ok"] is True and len(res["quarantined"]) == 1 and len(res["records"]) == 0
    assert list_dir(tmp_path, "data")["ok"] is True


def test_iot_agent_self_heal_and_recall(tmp_path: Path):
    shutil.copytree(Path(__file__).resolve().parent / "data", tmp_path / "data")
    goal = "Diagnose IoT fleet overvoltage and thermal anomalies."
    r1 = run_agent(goal, workdir=tmp_path, mock_llm=True)
    trace1 = [json.loads(line) for line in (tmp_path / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
    assert any(row["status"] == "error" for row in trace1)
    assert any(row["status"] == "recovered" for row in trace1)
    assert (tmp_path / "out" / "iot_report.md").exists()

    r2 = run_agent(goal, workdir=tmp_path, mock_llm=True)
    assert r2["recalled"] >= 1
    assert r2["steps"] < r1["steps"]
