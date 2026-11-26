"""Write a short one-sentence After-Action Review rule from step traces."""

from __future__ import annotations


def distill_aar(goal: str, trace: list[dict], resolved_file: str | None = None) -> str:
    """Record fixed file paths and recovered errors without raw log text."""
    errors = [entry["tool"] for entry in trace if entry.get("status") == "error"]
    if resolved_file and errors:
        return f"Inspect '{resolved_file}' directly via read_file instead of guessing missing root filenames."
    if resolved_file:
        return f"Read '{resolved_file}' first to extract telemetry records reliably."
    if errors:
        return f"Handle structured error hints after failed calls to {', '.join(errors)}."
    return f"Execute direct tool sequence verified for task: {goal[:80]}."
