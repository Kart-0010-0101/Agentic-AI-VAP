"""Day 3: Closed-loop ReAct Agent with self-healing tool recovery, trace.jsonl, and AAR memory."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from pathlib import Path
from dotenv import load_dotenv

from aar_engine import distill_aar
from generate_mock_data import ensure_sample_data
from memory import EpisodicMemory
from tools import TOOL_REGISTRY


def _write_trace(trace_path: Path, entries: list[dict]) -> None:
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with trace_path.open("w", encoding="utf-8") as fh:
        for row in entries:
            fh.write(json.dumps(row) + "\n")


def _llm_next_action(goal: str, history: list[dict], precedents: list[dict]) -> dict:
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "gsk_replace_with_your_real_key":
        raise RuntimeError("No valid GROQ_API_KEY configured; pass --mock-llm for offline mode.")

    sys_prompt = (
        "You are an autonomous ReAct ECE engineering agent. Respond ONLY with valid JSON: "
        '{"thought": "...", "tool": "list_dir|read_file|search_kb|write_report|FINAL_ANSWER", "args": {...}}.'
    )
    user_msg = json.dumps({"goal": goal, "recalled_lessons": precedents, "history": history[-6:]})
    payload = json.dumps({
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_msg}],
        "temperature": 0.1,
        "max_tokens": 300,
        "response_format": {"type": "json_object"},
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
    return json.loads(raw)


def _mock_next_action(step: int, history: list[dict], precedents: list[dict]) -> dict:
    """Deterministic closed-loop ReAct planner demonstrating cold self-heal vs warm recall."""
    warm_hit = any("data/iot_sensor_log.json" in p["lesson"] for p in precedents)
    last_obs = history[-1]["observation"] if history else {}

    if warm_hit:
        if step == 1:
            return {"thought": "Recalled AAR rule: read data/iot_sensor_log.json directly.", "tool": "read_file", "args": {"filepath": "data/iot_sensor_log.json"}}
        records = last_obs.get("records", [])
        alerts = [r["node"] for r in records if r.get("status") != "ok"]
        return {
            "thought": "Telemetry verified via recalled path; writing audit report.",
            "tool": "write_report",
            "args": {"filepath": "out/audit_report.md", "content": f"# Audit Report\nThermal alerts: {alerts}\n"},
        }

    # Cold run: triggers FileNotFoundError -> recovers cleanly via list_dir -> read_file -> write_report
    if step == 1:
        return {"thought": "Attempt to open root sensor telemetry file.", "tool": "read_file", "args": {"filepath": "sensor_log.csv"}}
    if step == 2 and not last_obs.get("ok"):
        return {"thought": "Recovered from FileNotFoundError; inspecting data/ directory.", "tool": "list_dir", "args": {"directory": "data"}}
    if step == 3:
        entries = last_obs.get("entries", ["iot_sensor_log.json"])
        fname = next((e for e in entries if e.endswith(".json")), "iot_sensor_log.json")
        return {"thought": f"Located '{fname}'; reading telemetry records.", "tool": "read_file", "args": {"filepath": f"data/{fname}"}}
    records = last_obs.get("records", [])
    alerts = [r["node"] for r in records if r.get("status") != "ok"]
    return {
        "thought": "Analyzed thermal alert nodes; generating clean Markdown report.",
        "tool": "write_report",
        "args": {"filepath": "out/audit_report.md", "content": f"# Audit Report\nThermal alerts: {alerts}\n"},
    }


def run_agent(
    goal: str,
    workdir: Path | None = None,
    db_dir: Path | None = None,
    trace_path: Path | None = None,
    max_steps: int = 10,
    mock_llm: bool = False,
) -> dict:
    workdir = workdir or Path(__file__).resolve().parent
    db_dir = db_dir or (workdir / "agent_memory")
    trace_path = trace_path or (workdir / "trace.jsonl")

    ensure_sample_data(workdir)
    mem = EpisodicMemory(db_dir=db_dir)
    precedents = mem.recall(goal)

    trace: list[dict] = []
    resolved_file: str | None = None

    for step in range(1, max_steps + 1):
        t0 = time.perf_counter()
        decision = _mock_next_action(step, trace, precedents) if mock_llm else _llm_next_action(goal, trace, precedents)
        tool_name = decision["tool"]
        args = decision.get("args", {})

        if tool_name == "FINAL_ANSWER":
            trace.append({
                "step": step,
                "thought": decision.get("thought", ""),
                "tool": "FINAL_ANSWER",
                "args": args,
                "status": "ok",
                "observation": {"ok": True},
                "elapsed_ms": round((time.perf_counter() - t0) * 1000, 2),
            })
            break

        fn = TOOL_REGISTRY.get(tool_name)
        if fn is None:
            obs = {"ok": False, "error": "UnknownTool", "detail": f"Tool '{tool_name}' not registered."}
        else:
            obs = fn(workdir, **args)

        status = "ok" if obs.get("ok") else "error"
        if status == "ok" and any(e.get("status") == "error" for e in trace):
            status = "recovered"
        if tool_name == "read_file" and obs.get("ok"):
            resolved_file = args.get("filepath")

        trace.append({
            "step": step,
            "thought": decision.get("thought", ""),
            "tool": tool_name,
            "args": args,
            "status": status,
            "observation": obs,
            "elapsed_ms": round((time.perf_counter() - t0) * 1000, 2),
        })

        if tool_name == "write_report" and obs.get("ok"):
            break

    _write_trace(trace_path, trace)
    lesson = distill_aar(goal, trace, resolved_file=resolved_file)
    mem.store_aar(goal, lesson, steps_taken=len(trace), outcome="success")

    return {
        "goal": goal,
        "steps": len(trace),
        "recalled_precedents": len(precedents),
        "aar_lesson": lesson,
        "trace_path": str(trace_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run closed-loop ReAct agent with episodic memory.")
    parser.add_argument("goal", type=str, nargs="?", default="Audit IoT node thermal anomalies and save report.")
    parser.add_argument("--max-steps", type=int, default=10)
    parser.add_argument("--mock-llm", action="store_true")
    args = parser.parse_args()

    res = run_agent(args.goal, max_steps=args.max_steps, mock_llm=args.mock_llm)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
