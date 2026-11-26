"""Dynamic fault injector: tests missing-file recovery and corrupt/NaN record isolation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from evaluator.project2_grader import _pick_agent_target


def run_fault_injection(repo_dir: Path) -> dict:
    """Verify student capstone/agent handles missing paths and NaN telemetry cleanly."""
    target = _pick_agent_target(repo_dir)
    if target is None:
        return {"recovered_missing_file": False, "quarantined_corrupt_data": False}

    probe = f"""
import importlib, json, shutil, tempfile
from pathlib import Path

repo = Path(".").resolve()
target = "{target}"
w = Path(tempfile.mkdtemp(prefix="fault_probe_"))
src_data = (repo / "data") if target == "." else (repo / target / "data")
if src_data.is_dir():
    shutil.copytree(src_data, w / "data")

mod = importlib.import_module("agent" if target == "." else f"{{target}}.agent")
mod.run_agent("Fault recovery check", workdir=w, mock_llm=True)
rows = [json.loads(ln) for ln in (w / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
recovered = any(r.get("status") == "error" for r in rows) and any(r.get("status") == "recovered" for r in rows)

quarantined = False
if target != ".":
    tools_mod = importlib.import_module(f"{{target}}.tools")
    if target == "capstone_1_iot":
        (w / "data" / "nan_test.json").write_text('[{{"node_id":"X1","bus_v":"NaN","vds_peak_v":50,"temp_c":40}}]', encoding="utf-8")
        qres = tools_mod.read_telemetry(w, "data/nan_test.json")
    elif target == "capstone_2_5g":
        (w / "data" / "nan_test.json").write_text('[{{"cell_id":"C1","prb_pct":"NaN","sinr_db":10,"bler_pct":1}}]', encoding="utf-8")
        qres = tools_mod.read_kpis(w, "data/nan_test.json")
    else:
        (w / "data" / "nan_test.json").write_text('[{{"paper_id":"P1","latency_ms":null,"f1_score":0.9}}]', encoding="utf-8")
        qres = tools_mod.read_papers(w, "data/nan_test.json")
    quarantined = bool(qres.get("ok") and len(qres.get("quarantined", [])) == 1)

print(json.dumps({{
    "recovered_missing_file": recovered,
    "quarantined_corrupt_data": quarantined,
}}))
"""
    res = subprocess.run([sys.executable, "-c", probe], cwd=repo_dir, capture_output=True, text=True, timeout=90)
    if res.returncode != 0:
        return {"recovered_missing_file": False, "quarantined_corrupt_data": False, "error": res.stderr[-300:]}
    try:
        return json.loads(res.stdout.strip().splitlines()[-1])
    except Exception:
        return {"recovered_missing_file": False, "quarantined_corrupt_data": False}
