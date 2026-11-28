"""Capstone 3 (Research): ReAct loop that screens papers by latency and F1 limits."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
import requests
from dotenv import load_dotenv

try:
    from .ingest import ingest_domain_kb
    from .memory import EpisodicMemory
    from .tools import TOOL_REGISTRY
except ImportError:
    from ingest import ingest_domain_kb
    from memory import EpisodicMemory
    from tools import TOOL_REGISTRY

DEFAULT_GROQ_MODEL = "qwen/qwen3.8-27b"


def _llm_decide(goal: str, trace: list[dict], precedents: list[dict]) -> dict:
    load_dotenv()
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key or key == "gsk_replace_with_your_real_key":
        raise RuntimeError("Missing GROQ_API_KEY; use --mock-llm offline.")
    model = os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip() or DEFAULT_GROQ_MODEL
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Output ONLY a single raw JSON object starting with '{' and ending with '}'. "
                    "Never write text outside JSON. "
                    'Schema: {"thought": "...", "tool": "list_dir|read_papers|query_standards|write_report|FINAL_ANSWER", "args": {...}}. '
                    "Tools: list_dir(directory), read_papers(filepath), query_standards(query_text), write_report(filepath, content), FINAL_ANSWER(). "
                    "Use relative workspace paths (e.g. 'data', 'out/research_report.md') and keep report under 150 words."
                ),
            },
            {"role": "user", "content": json.dumps({"goal": goal, "precedents": precedents, "trace": trace[-5:]})},
        ],
        "temperature": 0.1,
        "max_tokens": 550,
        "response_format": {"type": "json_object"},
    }
    if "qwen" in model.lower():
        payload["reasoning_effort"] = "none"
    resp = None
    for attempt in range(4):
        req_body = dict(payload)
        if attempt >= 1 and resp is not None and resp.status_code == 400:
            req_body["messages"] = payload["messages"] + [
                {"role": "user", "content": "Return ONLY a valid JSON object starting with '{'. No prose."}
            ]
            req_body["max_tokens"] = 700
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=req_body,
            timeout=30,
        )
        if resp.status_code not in (400, 429) or attempt == 3:
            break
        wait_s = min(float(resp.headers.get("Retry-After", 4 * (attempt + 1))), 25.0) if resp.status_code == 429 else 1.0
        time.sleep(wait_s)
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"].strip()
    start, end = raw.find("{"), raw.rfind("}")
    return json.loads(raw[start : end + 1] if start != -1 and end > start else raw)


def _mock_decide(step: int, trace: list[dict], precedents: list[dict], papers_rel: str) -> dict:
    warm = any("paper_abstracts" in p["lesson"] or "data/" in p["lesson"] for p in precedents)
    last_obs = trace[-1]["observation"] if trace else {}

    if warm and step == 1:
        return {"thought": "Recalled AAR precedent: read research JSON directly.", "tool": "read_papers", "args": {"filepath": papers_rel}}
    if not warm:
        if step == 1:
            return {"thought": "Open default root paper index.", "tool": "read_papers", "args": {"filepath": "missing_papers.json"}}
        if step == 2 and not last_obs.get("ok"):
            return {"thought": "Recover from FileNotFoundError by inspecting data/.", "tool": "list_dir", "args": {"directory": "data"}}
        if step == 3:
            entries = [e for e in last_obs.get("entries", []) if e.endswith(".json")]
            target = papers_rel if (papers_rel != "data/paper_abstracts.json") else f"data/{entries[0]}" if entries else papers_rel
            return {"thought": f"Inspect discovered literature file {target}.", "tool": "read_papers", "args": {"filepath": target}}

    paper_obs = next((r["observation"] for r in reversed(trace) if r["tool"] == "read_papers" and r["observation"].get("ok")), {})
    records = paper_obs.get("records", [])
    quarantined = paper_obs.get("quarantined", [])
    if step <= (2 if warm else 4) and not any(r["tool"] == "query_standards" for r in trace):
        return {"thought": "Check target latency and F1 benchmark criteria.", "tool": "query_standards", "args": {"query_text": "latency_ms and f1_score threshold"}}

    qualified = [r["paper_id"] for r in records if r.get("latency_ms", 999) <= 50.0 and r.get("f1_score", 0) >= 0.85]
    report = (
        "# ECE Literature Benchmark Synthesis\n\n"
        f"- **Papers Evaluated**: {len(records)}\n"
        f"- **Quarantined Corrupt Entries**: {len(quarantined)}\n"
        f"- **Production-Ready Studies**: {', '.join(qualified) if qualified else 'None'}\n"
    )
    return {"thought": "Generate cited literature synthesis report.", "tool": "write_report", "args": {"filepath": "out/research_report.md", "content": report}}


def run_agent(
    goal: str,
    workdir: Path | None = None,
    db_dir: Path | None = None,
    papers_rel: str = "data/paper_abstracts.json",
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
        decision = _mock_decide(step, trace, precedents, papers_rel) if mock_llm else _llm_decide(goal, trace, precedents)
        tool = decision["tool"]
        args = decision.get("args", {})
        if tool == "FINAL_ANSWER":
            break
        fn = TOOL_REGISTRY.get(tool)
        if fn is None:
            obs = {"ok": False, "error": "UnknownTool"}
        else:
            try:
                obs = fn(workdir, **args)
            except Exception as exc:
                obs = {"ok": False, "error": type(exc).__name__, "detail": str(exc)}
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
    lesson = f"Inspect '{papers_rel}' in data/ directly before applying edge F1/latency benchmarks."
    mem.store_aar(goal, lesson, len(trace))
    return {"goal": goal, "steps": len(trace), "recalled": len(precedents), "trace_path": str(trace_path)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("goal", nargs="?", default="Synthesize edge ECE literature benchmarks and flag production studies.")
    ap.add_argument("--papers", default="data/paper_abstracts.json")
    ap.add_argument("--mock-llm", action="store_true")
    args = ap.parse_args()
    print(json.dumps(run_agent(args.goal, papers_rel=args.papers, mock_llm=args.mock_llm), indent=2))
