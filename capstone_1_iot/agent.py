"""Capstone 1 (IoT Fleet): ReAct loop that finds and reports hardware faults."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from pathlib import Path
from dotenv import load_dotenv

try:
    from .ingest import ingest_domain_kb
    from .memory import EpisodicMemory
    from .tools import TOOL_REGISTRY
except ImportError:
    from ingest import ingest_domain_kb
    from memory import EpisodicMemory
    from tools import TOOL_REGISTRY


def _llm_decide(goal: str, trace: list[dict], precedents: list[dict]) -> dict:
    load_dotenv()
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key or key == "gsk_replace_with_your_real_key":
        raise RuntimeError("Missing GROQ_API_KEY; use --mock-llm offline.")
    payload = json.dumps({
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": 'Return JSON {"thought": "...", "tool": "list_dir|read_telemetry|query_specs|write_report|FINAL_ANSWER", "args": {...}}.'},
            {"role": "user", "content": json.dumps({"goal": goal, "precedents": precedents, "trace": trace[-5:]})},
        ],
        "temperature": 0.1,
        "max_tokens": 300,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=payload,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"])


def _mock_decide(step: int, trace: list[dict], precedents: list[dict], telemetry_rel: str) -> dict:
    warm = any("fleet_telemetry" in p["lesson"] or "data/" in p["lesson"] for p in precedents)
    last_obs = trace[-1]["observation"] if trace else {}

    if warm and step == 1:
        return {"thought": "Recalled AAR precedent: read data telemetry directly.", "tool": "read_telemetry", "args": {"filepath": telemetry_rel}}
    if not warm:
        if step == 1:
            return {"thought": "Try default telemetry filename.", "tool": "read_telemetry", "args": {"filepath": "missing_fleet.json"}}
        if step == 2 and not last_obs.get("ok"):
            return {"thought": "Recover from FileNotFoundError by listing data/.", "tool": "list_dir", "args": {"directory": "data"}}
        if step == 3:
            entries = [e for e in last_obs.get("entries", []) if e.endswith(".json")]
            target = telemetry_rel if (telemetry_rel != "data/fleet_telemetry.json") else f"data/{entries[0]}" if entries else telemetry_rel
            return {"thought": f"Inspect discovered file {target}.", "tool": "read_telemetry", "args": {"filepath": target}}

    # Query domain spec and write clean Markdown report
    telemetry_step = next((r["observation"] for r in reversed(trace) if r["tool"] == "read_telemetry" and r["observation"].get("ok")), {})
    records = telemetry_step.get("records", [])
    quarantined = telemetry_step.get("quarantined", [])
    if step <= (2 if warm else 4) and not any(r["tool"] == "query_specs" for r in trace):
        return {"thought": "Check IRF540N Vds & thermal limits from Chroma specs.", "tool": "query_specs", "args": {"query_text": "MOSFET max Vds and enclosure temperature"}}

    faults = [r["node_id"] for r in records if r.get("vds_peak_v", 0) > 100 or r.get("temp_c", 0) > 85 or r.get("bus_v", 24) < 18]
    report = (
        "# IoT Fleet Fault Diagnosis Report\n\n"
        f"- **Valid Nodes Analyzed**: {len(records)}\n"
        f"- **Quarantined Corrupt Rows**: {len(quarantined)}\n"
        f"- **Fault Nodes Detected**: {', '.join(faults) if faults else 'None'}\n"
    )
    return {"thought": "Generate final IoT diagnostic Markdown report.", "tool": "write_report", "args": {"filepath": "out/iot_report.md", "content": report}}


def run_agent(
    goal: str,
    workdir: Path | None = None,
    db_dir: Path | None = None,
    telemetry_rel: str = "data/fleet_telemetry.json",
    max_steps: int = 10,
    mock_llm: bool = False,
) -> dict:
    workdir = workdir or Path(__file__).resolve().parent
    db_dir = db_dir or (workdir / "capstone_memory")
    ingest_domain_kb(workdir / "data", db_dir)
    mem = EpisodicMemory(db_dir)
    precedents = mem.recall(goal)

    trace: list[dict] = []
    for step in range(1, max_steps + 1):
        t0 = time.perf_counter()
        decision = _mock_decide(step, trace, precedents, telemetry_rel) if mock_llm else _llm_decide(goal, trace, precedents)
        tool = decision["tool"]
        args = decision.get("args", {})
        if tool == "FINAL_ANSWER":
            break
        fn = TOOL_REGISTRY.get(tool)
        obs = fn(workdir, **args) if fn else {"ok": False, "error": "UnknownTool"}
        status = "ok" if obs.get("ok") else "error"
        if status == "ok" and any(e["status"] == "error" for e in trace):
            status = "recovered"
        trace.append({
            "step": step,
            "thought": decision.get("thought", ""),
            "tool": tool,
            "args": args,
            "status": status,
            "observation": obs,
            "elapsed_ms": round((time.perf_counter() - t0) * 1000, 2),
        })
        if tool == "write_report" and obs.get("ok"):
            break

    trace_path = workdir / "trace.jsonl"
    trace_path.write_text("\n".join(json.dumps(r) for r in trace) + "\n", encoding="utf-8")
    lesson = f"Inspect '{telemetry_rel}' directly in data/ before checking IRF540N thermal/Vds thresholds."
    mem.store_aar(goal, lesson, len(trace))
    return {"goal": goal, "steps": len(trace), "recalled": len(precedents), "trace_path": str(trace_path)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("goal", nargs="?", default="Diagnose IoT fleet overvoltage and thermal anomalies.")
    ap.add_argument("--telemetry", default="data/fleet_telemetry.json")
    ap.add_argument("--mock-llm", action="store_true")
    args = ap.parse_args()
    print(json.dumps(run_agent(args.goal, telemetry_rel=args.telemetry, mock_llm=args.mock_llm), indent=2))
