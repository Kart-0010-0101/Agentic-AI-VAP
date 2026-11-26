"""100-point weighted rubric calculator with explicit hardcoded-chain (0/20) & secret penalties."""

from __future__ import annotations


def compute_score(static_res: dict, rag_res: dict, agent_res: dict, fault_res: dict) -> dict:
    breakdown = {
        "rag_pipeline_25": 0,
        "react_loop_20": 0,
        "fault_recovery_25": 0,
        "episodic_memory_20": 0,
        "hygiene_and_docs_10": 0,
    }
    deductions: list[str] = []

    if rag_res.get("ran"):
        if rag_res.get("idempotent"):
            breakdown["rag_pipeline_25"] += 12
        else:
            deductions.append("RAG ingestion failed idempotency check (-12)")
        if rag_res.get("retrieval_ok"):
            breakdown["rag_pipeline_25"] += 13
        else:
            deductions.append("RAG semantic retrieval missed target spec (-13)")
    else:
        deductions.append("Project 1 RAG scripts not found or failed to execute (-25)")

    if not static_res.get("has_react_loop"):
        breakdown["react_loop_20"] = 0
        deductions.append("CRITICAL: No iterative ReAct loop detected in agent.py (0/20)")
    else:
        if agent_res.get("trace_valid"):
            breakdown["react_loop_20"] = 20
        else:
            breakdown["react_loop_20"] = 10
            deductions.append("Loop present but trace.jsonl contract incomplete (-10)")

    if fault_res.get("recovered_missing_file"):
        breakdown["fault_recovery_25"] += 13
    else:
        deductions.append("Agent did not self-heal from missing file fault (-13)")
    if fault_res.get("quarantined_corrupt_data"):
        breakdown["fault_recovery_25"] += 12
    else:
        deductions.append("Agent failed to quarantine corrupt/NaN records safely (-12)")

    if agent_res.get("cross_session_speedup"):
        breakdown["episodic_memory_20"] = 20
    elif agent_res.get("recalled_precedents", 0) > 0:
        breakdown["episodic_memory_20"] = 10
        deductions.append("Memory recalled precedent but did not reduce step count (-10)")
    else:
        deductions.append("No cross-session episodic recall verified (-20)")

    if static_res.get("secret_hygiene_ok"):
        breakdown["hygiene_and_docs_10"] += 6
    else:
        deductions.append("SECURITY FAIL: .env file or hardcoded API key detected (-6)")
    if static_res.get("has_readme") and static_res.get("has_pyproject"):
        breakdown["hygiene_and_docs_10"] += 4
    else:
        deductions.append("Missing README.md or pyproject.toml (-4)")

    total = sum(breakdown.values())
    grade = "A+" if total >= 90 else "A" if total >= 80 else "B" if total >= 70 else "C" if total >= 60 else "FAIL"
    return {"total_score": total, "max_score": 100, "grade": grade, "breakdown": breakdown, "deductions": deductions}
