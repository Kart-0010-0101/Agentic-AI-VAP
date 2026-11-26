"""Grade ReAct trace logs and cross-session memory step speedup."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _pick_agent_target(repo_dir: Path) -> str | None:
    for cand in ("capstone_1_iot", "capstone_2_5g", "capstone_3_research"):
        if (repo_dir / cand / "agent.py").is_file():
            return cand
    if (repo_dir / "agent.py").is_file():
        return "."
    return None


def grade_project2(repo_dir: Path) -> dict:
    """Run agent twice in isolated subprocess to check trace contract and warm-recall speedup."""
    target = _pick_agent_target(repo_dir)
    if target is None:
        return {"ran": False, "trace_valid": False, "cross_session_speedup": False, "recalled_precedents": 0}

    probe = f"""
import importlib, json, shutil, tempfile
from pathlib import Path

repo = Path(".").resolve()
target = "{target}"
w = Path(tempfile.mkdtemp(prefix="agent_probe_"))
src_data = (repo / "data") if target == "." else (repo / target / "data")
if src_data.is_dir():
    shutil.copytree(src_data, w / "data")

mod = importlib.import_module("agent" if target == "." else f"{{target}}.agent")
goal = "Audit anomalies and produce diagnostic report."
r1 = mod.run_agent(goal, workdir=w, mock_llm=True)
r2 = mod.run_agent(goal, workdir=w, mock_llm=True)
trace_file = w / "trace.jsonl"
rows = [json.loads(ln) for ln in trace_file.read_text(encoding="utf-8").splitlines()] if trace_file.is_file() else []
req = {{"step", "thought", "tool", "args", "status", "observation", "elapsed_ms"}}
trace_valid = len(rows) >= 2 and all(req.issubset(r.keys()) for r in rows)
recalled = r2.get("recalled", r2.get("recalled_precedents", 0))
print(json.dumps({{
    "ran": True,
    "target": target,
    "trace_valid": trace_valid,
    "run1_steps": r1.get("steps", 0),
    "run2_steps": r2.get("steps", 0),
    "recalled_precedents": recalled,
    "cross_session_speedup": recalled >= 1 and r2.get("steps", 99) < r1.get("steps", 0),
}}))
"""
    res = subprocess.run([sys.executable, "-c", probe], cwd=repo_dir, capture_output=True, text=True, timeout=90)
    if res.returncode != 0:
        return {"ran": True, "trace_valid": False, "cross_session_speedup": False, "recalled_precedents": 0, "error": res.stderr[-300:]}
    try:
        return json.loads(res.stdout.strip().splitlines()[-1])
    except Exception:
        return {"ran": True, "trace_valid": False, "cross_session_speedup": False, "recalled_precedents": 0}
