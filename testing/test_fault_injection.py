"""Test unseen Batch B fault injection and broken JSON handling across all capstones."""

from __future__ import annotations

import shutil
from pathlib import Path
from capstone_1_iot.agent import run_agent as run_iot
from capstone_1_iot.tools import read_telemetry
from capstone_2_5g.agent import run_agent as run_5g
from capstone_2_5g.tools import read_kpis
from capstone_3_research.agent import run_agent as run_research
from capstone_3_research.tools import read_papers

BENCH_DIR = Path(__file__).resolve().parent / "unseen_benchmarks"


def _prep(capstone_dir: str, bench_file: str, tmp_path: Path) -> str:
    root = Path(__file__).resolve().parent.parent
    shutil.copytree(root / capstone_dir / "data", tmp_path / "data")
    shutil.copy2(BENCH_DIR / bench_file, tmp_path / "data" / bench_file)
    return f"data/{bench_file}"


def test_fault_injection_unseen_iot_batch_b(tmp_path: Path):
    rel = _prep("capstone_1_iot", "iot_batch_b.json", tmp_path)
    res = run_iot("Audit unseen Batch B IoT telemetry faults.", workdir=tmp_path, telemetry_rel=rel, mock_llm=True)
    assert res["steps"] >= 3
    report = (tmp_path / "out" / "iot_report.md").read_text(encoding="utf-8")
    assert "BATCHB-03" in report
    assert "Quarantined Corrupt Rows**: 2" in report


def test_fault_injection_unseen_5g_batch_b(tmp_path: Path):
    rel = _prep("capstone_2_5g", "gnb_batch_b.json", tmp_path)
    res = run_5g("Audit unseen Batch B 5G cell KPIs.", workdir=tmp_path, kpi_rel=rel, mock_llm=True)
    assert res["steps"] >= 3
    report = (tmp_path / "out" / "nr_report.md").read_text(encoding="utf-8")
    assert "GNB-B02" in report
    assert "Quarantined Corrupt Rows**: 1" in report


def test_fault_injection_unseen_research_batch_b(tmp_path: Path):
    rel = _prep("capstone_3_research", "papers_batch_b.json", tmp_path)
    res = run_research("Evaluate unseen Batch B literature metrics.", workdir=tmp_path, papers_rel=rel, mock_llm=True)
    assert res["steps"] >= 3
    report = (tmp_path / "out" / "research_report.md").read_text(encoding="utf-8")
    assert "ECE-B01" in report
    assert "Quarantined Corrupt Entries**: 1" in report


def test_malformed_json_never_raises_unhandled_traceback(tmp_path: Path):
    (tmp_path / "data").mkdir()
    shutil.copy2(BENCH_DIR / "corrupt_malformed.json", tmp_path / "data" / "broken.json")
    for fn in (read_telemetry, read_kpis, read_papers):
        out = fn(tmp_path, "data/broken.json")
        assert out["ok"] is False and out["error"] == "JSONDecodeError"
