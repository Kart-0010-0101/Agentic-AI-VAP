"""
create_vap_diagrams_v2.py
Generates clean, high-resolution (300 DPI) technical block diagrams and cover graphics
for the 5-Day Value Added Program (VAP) on Agentic AI and Vector RAG.

Strict Layout Guarantees:
- Accounts explicitly for FancyBboxPatch padding on all arrow endpoints
- Generous box widths/heights with multi-line wrapped labels so text never clips or overflows
- Clean white corridors for cross-lane arrows so arrows never cross text
- Crisp typography, minimal white background, deep blue (#1E3A8A) and tech orange (#EA580C) accents
- Zero emojis, ASD-STE100 technical terminology
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = r"C:\Users\lapto\Desktop\demo\BEN\VAP\images"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def add_rounded_box(ax, x, y, w, h, edge, bg, lw=1.4, pad=0.06, zorder=2):
    """Draw a rounded box whose OUTER visual bounds are strictly [x, x+w] x [y, y+h]."""
    r = patches.FancyBboxPatch(
        (x + pad, y + pad),
        w - 2 * pad,
        h - 2 * pad,
        boxstyle=f"round,pad={pad}",
        edgecolor=edge,
        facecolor=bg,
        linewidth=lw,
        zorder=zorder,
    )
    ax.add_patch(r)
    return r


def add_arrow(ax, x1, y1, x2, y2, color="#1E3A8A", lw=1.8, style="->", ls="solid", zorder=5):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle=f"{style},head_width=0.32,head_length=0.45",
            color=color,
            lw=lw,
            linestyle=ls,
            shrinkA=2,
            shrinkB=2,
        ),
        zorder=zorder,
    )


# ----------------------------------------------------------------------
# 1. COVER PAGE GRAPHIC: Modern Agentic AI & Vector Memory Visual
# ----------------------------------------------------------------------
def generate_cover_graphic():
    fig, ax = plt.subplots(figsize=(9.5, 5.4), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.8)
    ax.axis("off")

    # Subtle background grid
    for x in np.linspace(0.5, 9.5, 19):
        ax.axvline(x, color="#F1F5F9", lw=0.6, zorder=0)
    for y in np.linspace(0.5, 5.3, 11):
        ax.axhline(y, color="#F1F5F9", lw=0.6, zorder=0)

    # Outer frame
    add_rounded_box(ax, 0.25, 0.2, 9.5, 5.4, edge="#E2E8F0", bg="#FAFAFA", lw=1.0, pad=0.10, zorder=1)

    # Central Agent Core Circle (centered at x=5.0, y=2.9)
    cx, cy = 5.0, 2.9
    outer_r = 0.98
    inner_r = 0.76
    ax.add_patch(patches.Circle((cx, cy), outer_r, facecolor="#EFF6FF", edgecolor="#1E3A8A", linewidth=2.0, zorder=2))
    ax.add_patch(patches.Circle((cx, cy), inner_r, facecolor="#1E3A8A", edgecolor="#1D4ED8", linewidth=1.4, zorder=3))
    ax.text(cx, cy + 0.16, "AGENT CORE", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#FFFFFF", zorder=4)
    ax.text(cx, cy - 0.18, "LLM REASONING\n& CONTROL LOOP", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#DBEAFE", zorder=4)

    # Top Box: ChromaDB Vector Memory (y: 4.45 to 5.40, generous width 4.0)
    add_rounded_box(ax, 3.0, 4.45, 4.0, 0.95, edge="#1E3A8A", bg="#EFF6FF", lw=1.5, pad=0.06, zorder=2)
    ax.text(5.0, 5.10, "CHROMADB VECTOR MEMORY", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(5.0, 4.72, "High-Dimensional Embeddings\nEpisodic Knowledge Store", ha="center", va="center", fontsize=7.6, color="#334155", zorder=3)

    # Bottom Box: Self-Reflection & Verification (y: 0.40 to 1.35, generous width 4.2)
    add_rounded_box(ax, 2.9, 0.40, 4.2, 0.95, edge="#15803D", bg="#F0FDF4", lw=1.5, pad=0.06, zorder=2)
    ax.text(5.0, 1.05, "SELF-REFLECTION & VERIFICATION", ha="center", va="center", fontsize=9.2, fontweight="bold", color="#15803D", zorder=3)
    ax.text(5.0, 0.68, "Error Interception  |  After Action Review (AAR)", ha="center", va="center", fontsize=7.6, color="#334155", zorder=3)

    # Left Box: Perception & Input (x: 0.60 to 2.90, y: 1.95 to 3.85)
    add_rounded_box(ax, 0.60, 1.95, 2.30, 1.90, edge="#1E3A8A", bg="#FFFFFF", lw=1.5, pad=0.07, zorder=2)
    ax.text(1.75, 3.45, "PERCEPTION & INPUT", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(1.75, 2.82, "Goal Objectives\nEngineering Alerts\nSensor Telemetry", ha="center", va="center", fontsize=7.6, color="#334155", zorder=3)
    ax.text(1.75, 2.22, "[ Input Stream ]", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#64748B", zorder=3)

    # Right Box: Tool Execution (x: 7.10 to 9.40, y: 1.95 to 3.85)
    add_rounded_box(ax, 7.10, 1.95, 2.30, 1.90, edge="#EA580C", bg="#FFFFFF", lw=1.5, pad=0.07, zorder=2)
    ax.text(8.25, 3.45, "TOOL EXECUTION", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#EA580C", zorder=3)
    ax.text(8.25, 2.82, "Telemetry Parsers\nDiagnostics APIs\nReport Generators", ha="center", va="center", fontsize=7.6, color="#334155", zorder=3)
    ax.text(8.25, 2.22, "[ Environment ]", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#64748B", zorder=3)

    # Arrows with clean margins and non-overlapping labels
    # Left -> Core (x: 2.95 -> 3.96)
    add_arrow(ax, 2.95, 2.90, 3.96, 2.90, color="#1E3A8A", lw=2.0)
    ax.text(3.46, 3.12, "Observe", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#1E3A8A", zorder=6)

    # Core -> Right (x: 6.04 -> 7.05)
    add_arrow(ax, 6.04, 2.90, 7.05, 2.90, color="#EA580C", lw=2.0)
    ax.text(6.54, 3.12, "Act", ha="center", va="center", fontsize=7.6, fontweight="bold", color="#EA580C", zorder=6)

    # Core <-> Top Memory (y: 3.92 <-> 4.42 -> 0.50 units of clear arrow shaft!)
    add_arrow(ax, 5.0, 3.92, 5.0, 4.42, color="#1E3A8A", lw=1.8, style="<->")
    ax.text(5.22, 4.17, "Recall & Store", ha="left", va="center", fontsize=7.5, fontweight="bold", color="#1E3A8A", zorder=6)

    # Core <-> Bottom Reflection (y: 1.88 <-> 1.38 -> 0.50 units of clear arrow shaft!)
    add_arrow(ax, 5.0, 1.88, 5.0, 1.38, color="#15803D", lw=1.8, style="<->")
    ax.text(5.22, 1.63, "Verify & Learn", ha="left", va="center", fontsize=7.5, fontweight="bold", color="#15803D", zorder=6)

    # Right -> Bottom (Feedback from Environment)
    add_arrow(ax, 8.15, 1.92, 7.15, 0.90, color="#15803D", lw=1.8)
    ax.text(7.95, 1.30, "Result", ha="center", va="center", fontsize=7.3, fontweight="bold", color="#15803D", zorder=6)

    # Bottom -> Left (Feedback loop to next perception cycle)
    add_arrow(ax, 2.85, 0.90, 1.85, 1.92, color="#1E3A8A", lw=1.8)
    ax.text(2.05, 1.30, "Iterate", ha="center", va="center", fontsize=7.3, fontweight="bold", color="#1E3A8A", zorder=6)

    out_file = os.path.join(OUTPUT_DIR, "cover_graphic.png")
    plt.tight_layout(pad=0.2)
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")


# ----------------------------------------------------------------------
# 2. DIAGRAM: Autonomy Spectrum (Zero Overlaps)
# ----------------------------------------------------------------------
def generate_autonomy_spectrum():
    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    ax.text(5.0, 5.25, "ARCHITECTURAL COMPARISON: PASSIVE TOOL USE VS. AUTONOMOUS AGENT",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")

    # --- TOP LANE: PASSIVE TOOL USE ---
    add_rounded_box(ax, 0.15, 3.00, 9.70, 2.00, edge="#CBD5E1", bg="#F8FAFC", lw=1.0, pad=0.07, zorder=1)
    ax.text(0.45, 4.72, "LEVEL 1: PASSIVE TOOL AUGMENTATION (SINGLE-TURN REQUEST / RESPONSE — NOT AGENTIC)",
            fontsize=8.2, fontweight="bold", color="#EA580C", zorder=3)

    boxes_top = [
        (0.45, 3.22, 1.90, 1.25, "Human User", "Types prompt:\n'Summarize emails'", "#64748B", "#FFFFFF"),
        (2.85, 3.22, 1.90, 1.25, "LLM Service", "Parses text &\ncalls 1 function", "#1E3A8A", "#EFF6FF"),
        (5.25, 3.22, 1.90, 1.25, "Single Tool", "Runs fetch_emails()\nAPI request", "#EA580C", "#FFF7ED"),
        (7.65, 3.22, 1.90, 1.25, "Static Output", "Returns summary &\nHALTS IMMEDIATELY", "#64748B", "#FFFFFF"),
    ]
    for x, y, w, h, title, sub, edge, bg in boxes_top:
        add_rounded_box(ax, x, y, w, h, edge=edge, bg=bg, lw=1.3, pad=0.05, zorder=2)
        ax.text(x + w / 2, y + h * 0.72, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=edge, zorder=3)
        ax.text(x + w / 2, y + h * 0.34, sub, ha="center", va="center", fontsize=7.2, color="#334155", zorder=3)

    add_arrow(ax, 2.38, 3.84, 2.82, 3.84, color="#64748B", lw=1.7)
    add_arrow(ax, 4.78, 3.84, 5.22, 3.84, color="#EA580C", lw=1.7)
    add_arrow(ax, 7.18, 3.84, 7.62, 3.84, color="#15803D", lw=1.7)

    # --- BOTTOM LANE: AUTONOMOUS AGENTIC SYSTEM ---
    add_rounded_box(ax, 0.15, 0.15, 9.70, 2.60, edge="#1E3A8A", bg="#EFF6FF", lw=1.2, pad=0.07, zorder=1)
    ax.text(0.45, 2.48, "LEVEL 3: AUTONOMOUS AGENTIC AI (DYNAMIC REACT LOOP, TOOLS & PERSISTENT MEMORY)",
            fontsize=8.2, fontweight="bold", color="#1E3A8A", zorder=3)

    # Goal Box
    add_rounded_box(ax, 0.45, 0.40, 1.65, 1.85, edge="#1E3A8A", bg="#FFFFFF", lw=1.3, pad=0.05, zorder=2)
    ax.text(1.275, 1.85, "Declared Goal", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(1.275, 1.15, "Autonomous\nObjective:\nAudit anomalies &\nverify telemetry", ha="center", va="center", fontsize=7.0, color="#334155", zorder=3)

    add_arrow(ax, 2.13, 1.32, 2.52, 1.32, color="#1E3A8A", lw=1.7)

    # ReAct Loop Box
    add_rounded_box(ax, 2.55, 0.40, 2.65, 1.85, edge="#1E3A8A", bg="#DBEAFE", lw=1.4, pad=0.05, zorder=2)
    ax.text(3.875, 1.98, "Autonomous ReAct Loop", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(3.875, 1.60, "1. Thought (Reasoning Step)", ha="center", va="center", fontsize=7.2, color="#1E3A8A", zorder=3)
    ax.text(3.875, 1.32, "2. Action (JSON Tool Call)", ha="center", va="center", fontsize=7.2, color="#EA580C", zorder=3)
    ax.text(3.875, 1.04, "3. Observation (Read Output)", ha="center", va="center", fontsize=7.2, color="#15803D", zorder=3)
    ax.text(3.875, 0.76, "4. Reflection (Self-Heal)", ha="center", va="center", fontsize=7.2, color="#1E3A8A", zorder=3)

    # Tool Execution Box (top right of middle pair — clear 0.25 gap below!)
    add_rounded_box(ax, 5.75, 1.42, 1.85, 0.83, edge="#EA580C", bg="#FFF7ED", lw=1.3, pad=0.05, zorder=2)
    ax.text(6.675, 1.98, "Tool Execution", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#EA580C", zorder=3)
    ax.text(6.675, 1.65, "Telemetry, Spec, Files", ha="center", va="center", fontsize=7.0, color="#334155", zorder=3)

    # ChromaDB Memory Box (bottom right of middle pair — clear 0.25 gap above!)
    add_rounded_box(ax, 5.75, 0.40, 1.85, 0.83, edge="#1E3A8A", bg="#FFFFFF", lw=1.3, pad=0.05, zorder=2)
    ax.text(6.675, 0.96, "ChromaDB Memory", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(6.675, 0.63, "Episodic store & recall", ha="center", va="center", fontsize=7.0, color="#334155", zorder=3)

    # Clean arrows between ReAct and Tool / Memory
    add_arrow(ax, 5.23, 1.95, 5.72, 1.95, color="#EA580C", lw=1.6)
    add_arrow(ax, 5.72, 1.65, 5.23, 1.65, color="#15803D", lw=1.6)
    add_arrow(ax, 5.23, 0.82, 5.72, 0.82, color="#1E3A8A", lw=1.6, style="<->")

    # Verified Goal Box
    add_arrow(ax, 7.63, 1.32, 8.00, 1.32, color="#15803D", lw=1.7)
    add_rounded_box(ax, 8.03, 0.40, 1.55, 1.85, edge="#15803D", bg="#F0FDF4", lw=1.4, pad=0.05, zorder=2)
    ax.text(8.805, 1.85, "Verified Goal", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#15803D", zorder=3)
    ax.text(8.805, 1.15, "Audit Completed\nRoot Cause Solved\nReport Saved", ha="center", va="center", fontsize=7.0, color="#334155", zorder=3)

    out_file = os.path.join(OUTPUT_DIR, "diag_autonomy_spectrum.png")
    plt.tight_layout(pad=0.2)
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")


# ----------------------------------------------------------------------
# 3. DIAGRAM: Vector RAG Architecture (Clean Corridor, Zero Crossing Text)
# ----------------------------------------------------------------------
def generate_rag_architecture():
    fig, ax = plt.subplots(figsize=(9.5, 5.0), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    ax.text(5.0, 5.35, "PROJECT 1: VECTOR RETRIEVAL-AUGMENTED GENERATION (RAG) ARCHITECTURE",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")

    # --- TOP PHASE: INGESTION (y: 3.15 to 5.05) ---
    add_rounded_box(ax, 0.15, 3.15, 9.70, 1.90, edge="#CBD5E1", bg="#F8FAFC", lw=1.0, pad=0.07, zorder=1)
    ax.text(0.45, 4.80, "PHASE 1: DOCUMENT INGESTION & VECTOR INDEXING (OFFLINE PREPARATION)",
            fontsize=8.2, fontweight="bold", color="#1E3A8A", zorder=3)

    p1_boxes = [
        (0.45, 3.35, 1.90, 1.25, "Raw Documents", "Technical Markdown\n& Protocol Text Files", "#64748B", "#FFFFFF"),
        (2.85, 3.35, 1.90, 1.25, "Sentence Chunker", "Splits on sentences\nMax 400 chars + overlap", "#1E3A8A", "#EFF6FF"),
        (5.25, 3.35, 1.90, 1.25, "Embedding Engine", "Generates 384-dim\ndense semantic vectors", "#EA580C", "#FFF7ED"),
        (7.65, 3.35, 1.90, 1.25, "ChromaDB Store", "HNSW Vector Index\n& Metadata Table", "#1E3A8A", "#DBEAFE"),
    ]
    for x, y, w, h, title, sub, edge, bg in p1_boxes:
        add_rounded_box(ax, x, y, w, h, edge=edge, bg=bg, lw=1.3, pad=0.05, zorder=2)
        ax.text(x + w / 2, y + h * 0.72, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=edge, zorder=3)
        ax.text(x + w / 2, y + h * 0.34, sub, ha="center", va="center", fontsize=7.2, color="#334155", zorder=3)

    add_arrow(ax, 2.38, 3.98, 2.82, 3.98, color="#1E3A8A", lw=1.7)
    add_arrow(ax, 4.78, 3.98, 5.22, 3.98, color="#EA580C", lw=1.7)
    add_arrow(ax, 7.18, 3.98, 7.62, 3.98, color="#1E3A8A", lw=1.7)

    # --- WHITE CORRIDOR BETWEEN PHASE 1 AND PHASE 2 (y: 2.30 to 3.15) ---
    # Stepped orthogonal path from ChromaDB Store (x=8.60, y=3.35) -> down to y=2.72 -> left to x=3.80 -> down to Cosine Search (y=1.60)
    # Wait: Phase 2 label sits on the left at y=2.05 (x=0.45..4.8), so let's keep the horizontal line at y=2.75 in the clean white corridor!
    # And drop vertically at x=3.80 AFTER moving Phase 2 title to the bottom or keeping Phase 2 title at x=0.45..3.5 or right-aligned!
    # Even cleaner: Put Phase 2 title at x=0.45, y=2.05, and drop into Cosine Search at x=4.40 (right side of Cosine Search box) or move label cleanly!
    # Let's check: Phase 2 box is y=0.15 to 2.25. Cosine Search is x=2.85 to 4.75, y=0.35 to 1.65.
    # If Phase 2 title is at y=1.98, x=0.45 (shortened cleanly: "PHASE 2: SEMANTIC RETRIEVAL & GENERATION"), it ends around x=3.8.
    # Dropping the vertical connector at x=4.45 (still well inside Cosine Search [2.85, 4.75]) completely avoids the title!

    # --- BOTTOM PHASE: RETRIEVAL & GENERATION (y: 0.15 to 2.25) ---
    add_rounded_box(ax, 0.15, 0.15, 9.70, 2.10, edge="#1E3A8A", bg="#EFF6FF", lw=1.2, pad=0.07, zorder=1)
    ax.text(0.45, 1.96, "PHASE 2: SEMANTIC RETRIEVAL & GENERATION",
            fontsize=8.2, fontweight="bold", color="#EA580C", zorder=3)

    p2_boxes = [
        (0.45, 0.35, 1.90, 1.32, "User Query", "Technical question:\n'Why does EVM fail?'", "#64748B", "#FFFFFF"),
        (2.85, 0.35, 1.90, 1.32, "Cosine Search", "Computes similarity\nRetrieves Top-K chunks", "#1E3A8A", "#FFFFFF"),
        (5.25, 0.35, 1.90, 1.32, "Prompt Assembly", "Injects context chunks\ninto system template", "#EA580C", "#FFF7ED"),
        (7.65, 0.35, 1.90, 1.32, "Groq Cloud LLM", "Llama 3.3 70B emits\ngrounded cited answer", "#15803D", "#F0FDF4"),
    ]
    for x, y, w, h, title, sub, edge, bg in p2_boxes:
        add_rounded_box(ax, x, y, w, h, edge=edge, bg=bg, lw=1.3, pad=0.05, zorder=2)
        ax.text(x + w / 2, y + h * 0.72, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=edge, zorder=3)
        ax.text(x + w / 2, y + h * 0.34, sub, ha="center", va="center", fontsize=7.2, color="#334155", zorder=3)

    add_arrow(ax, 2.38, 1.01, 2.82, 1.01, color="#1E3A8A", lw=1.7)
    add_arrow(ax, 4.78, 1.01, 5.22, 1.01, color="#EA580C", lw=1.7)
    add_arrow(ax, 7.18, 1.01, 7.62, 1.01, color="#15803D", lw=1.7)

    # Clean orthogonal corridor connector: ChromaDB Store (x=8.60, y=3.35) -> down to y=2.70 -> left to x=4.55 -> down to Cosine Search (y=1.69)
    ax.plot([8.60, 8.60, 4.55], [3.33, 2.70, 2.70], color="#1E3A8A", lw=1.7, linestyle="--", zorder=4)
    add_arrow(ax, 4.55, 2.70, 4.55, 1.69, color="#1E3A8A", lw=1.7, ls="--")

    # White pill badge for corridor label so zero line cuts through text
    badge = patches.FancyBboxPatch((5.55, 2.52), 2.15, 0.36, boxstyle="round,pad=0.04",
                                   edgecolor="#1E3A8A", facecolor="#FFFFFF", linewidth=0.9, zorder=5)
    ax.add_patch(badge)
    ax.text(6.625, 2.70, "Indexed Vector Lookup", ha="center", va="center", fontsize=7.4, fontweight="bold", color="#1E3A8A", zorder=6)

    out_file = os.path.join(OUTPUT_DIR, "diag_rag_architecture.png")
    plt.tight_layout(pad=0.2)
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")


# ----------------------------------------------------------------------
# 4. DIAGRAM: ReAct Autonomous Loop with Dual Memory (Proper Cycle Arrows)
# ----------------------------------------------------------------------
def generate_react_loop():
    fig, ax = plt.subplots(figsize=(9.5, 5.0), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    ax.text(5.0, 5.35, "AUTONOMOUS AGENT CONTROL LOOP WITH DUAL-MEMORY FUSION",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")

    add_rounded_box(ax, 0.15, 0.15, 9.70, 4.95, edge="#CBD5E1", bg="#F8FAFC", lw=1.0, pad=0.07, zorder=1)

    # Goal Objective (Left)
    add_rounded_box(ax, 0.40, 2.75, 1.75, 1.85, edge="#1E3A8A", bg="#FFFFFF", lw=1.3, pad=0.05, zorder=2)
    ax.text(1.275, 4.20, "Goal Objective", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(1.275, 3.48, "Engineering Task:\n'Diagnose anomaly\nin sensor cluster'", ha="center", va="center", fontsize=7.2, color="#334155", zorder=3)

    add_arrow(ax, 2.18, 3.68, 2.58, 3.68, color="#1E3A8A", lw=1.8)

    # Central ReAct Engine Box (x: 2.60 to 7.20, y: 1.75 to 4.90 -> spacious!)
    add_rounded_box(ax, 2.60, 1.75, 4.60, 3.15, edge="#1E3A8A", bg="#EFF6FF", lw=1.4, pad=0.06, zorder=2)
    ax.text(4.90, 4.62, "AGENT CONTROL ENGINE (agent.py)", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#1E3A8A", zorder=3)

    # 4 sub-boxes with 0.50 horizontal gap and 0.45 vertical gap for clear cycle arrows!
    # Top-left: 1. Thought
    add_rounded_box(ax, 2.85, 3.40, 1.80, 0.98, edge="#1E3A8A", bg="#FFFFFF", lw=1.2, pad=0.04, zorder=3)
    ax.text(3.75, 4.08, "1. Thought", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#1E3A8A", zorder=4)
    ax.text(3.75, 3.68, "Evaluate state &\nderive sub-goal", ha="center", va="center", fontsize=7.0, color="#334155", zorder=4)

    # Top-right: 2. Action
    add_rounded_box(ax, 5.15, 3.40, 1.80, 0.98, edge="#EA580C", bg="#FFF7ED", lw=1.2, pad=0.04, zorder=3)
    ax.text(6.05, 4.08, "2. Action", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#EA580C", zorder=4)
    ax.text(6.05, 3.68, "Dispatch tool call\nwith JSON params", ha="center", va="center", fontsize=7.0, color="#334155", zorder=4)

    # Bottom-right: 3. Observation
    add_rounded_box(ax, 5.15, 1.98, 1.80, 0.98, edge="#15803D", bg="#F0FDF4", lw=1.2, pad=0.04, zorder=3)
    ax.text(6.05, 2.66, "3. Observation", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#15803D", zorder=4)
    ax.text(6.05, 2.26, "Capture return\nor error string", ha="center", va="center", fontsize=7.0, color="#334155", zorder=4)

    # Bottom-left: 4. Reflection
    add_rounded_box(ax, 2.85, 1.98, 1.80, 0.98, edge="#1E3A8A", bg="#FFFFFF", lw=1.2, pad=0.04, zorder=3)
    ax.text(3.75, 2.66, "4. Reflection", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#1E3A8A", zorder=4)
    ax.text(3.75, 2.26, "Check progress &\nplan next step", ha="center", va="center", fontsize=7.0, color="#334155", zorder=4)

    # All 4 cycle arrows clearly drawn!
    add_arrow(ax, 4.68, 3.89, 5.12, 3.89, color="#EA580C", lw=1.6)  # Thought -> Action
    add_arrow(ax, 6.05, 3.37, 6.05, 2.99, color="#EA580C", lw=1.6)  # Action -> Observation
    add_arrow(ax, 5.12, 2.47, 4.68, 2.47, color="#15803D", lw=1.6)  # Observation -> Reflection
    add_arrow(ax, 3.75, 2.99, 3.75, 3.37, color="#1E3A8A", lw=1.6)  # Reflection -> Thought

    # External Tool Arsenal (Right)
    add_rounded_box(ax, 7.65, 2.45, 1.95, 2.15, edge="#EA580C", bg="#FFFFFF", lw=1.3, pad=0.05, zorder=2)
    ax.text(8.625, 4.22, "Tool Arsenal", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#EA580C", zorder=3)
    ax.text(8.625, 3.35, "1. query_memory\n2. parse_logs\n3. check_spec\n4. make_report", ha="center", va="center", fontsize=7.3, color="#334155", zorder=3)

    # Arrows between ReAct Engine and Tool Arsenal
    add_arrow(ax, 7.23, 3.89, 7.62, 3.89, color="#EA580C", lw=1.7)
    add_arrow(ax, 7.62, 2.75, 7.23, 2.75, color="#15803D", lw=1.7)

    # Bottom Left: Long-Term Vector Memory
    add_rounded_box(ax, 0.40, 0.35, 4.30, 0.98, edge="#1E3A8A", bg="#DBEAFE", lw=1.3, pad=0.05, zorder=2)
    ax.text(2.55, 1.02, "LONG-TERM VECTOR EPISODIC MEMORY (ChromaDB)", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(2.55, 0.62, "store_memory() saves lessons  |  recall_memory() retrieves cases", ha="center", va="center", fontsize=7.1, color="#334155", zorder=3)

    # Bottom Right: Final Verified Output
    add_rounded_box(ax, 5.30, 0.35, 4.30, 0.98, edge="#15803D", bg="#F0FDF4", lw=1.3, pad=0.05, zorder=2)
    ax.text(7.45, 1.02, "FINAL VERIFIED GOAL SATISFACTION", ha="center", va="center", fontsize=8.0, fontweight="bold", color="#15803D", zorder=3)
    ax.text(7.45, 0.62, "Emits 'FINAL ANSWER:' with verified audit report", ha="center", va="center", fontsize=7.1, color="#334155", zorder=3)

    # Clean vertical connectors from Engine to Memory & Final Output
    add_arrow(ax, 3.75, 1.72, 3.75, 1.36, color="#1E3A8A", lw=1.7, style="<->")
    add_arrow(ax, 6.05, 1.72, 6.05, 1.36, color="#15803D", lw=1.7)

    out_file = os.path.join(OUTPUT_DIR, "diag_react_loop.png")
    plt.tight_layout(pad=0.2)
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")


# ----------------------------------------------------------------------
# 5. DIAGRAM: Capstone Architectural Layers (Clean Vertical Gaps)
# ----------------------------------------------------------------------
def generate_capstone_architecture():
    fig, ax = plt.subplots(figsize=(9.5, 4.8), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    ax.text(5.0, 5.35, "PROJECT 2 CAPSTONE SYSTEM ARCHITECTURAL LAYERS",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")

    # 4 layers, height 0.92 each, vertical gap 0.38 between layers -> clean arrow shafts!
    layers = [
        (0.4, 4.10, 9.2, 0.92, "LAYER 1: PROBLEM OBJECTIVE & SENSING INPUT",
         "IoT Telemetry Anomaly Alert  |  5G RF EVM Spec Violation  |  Literature Survey Target", "#1E3A8A", "#EFF6FF"),
        (0.4, 2.80, 9.2, 0.92, "LAYER 2: AUTONOMOUS REASONING CONTROLLER (agent.py)",
         "Pure-Python ReAct While-Loop  |  Step Budget Guardrail (max 10)  |  JSON Tool Dispatcher", "#1E3A8A", "#DBEAFE"),
        (0.4, 1.50, 9.2, 0.92, "LAYER 3: MODULAR TOOL ARSENAL (tools.py)",
         "query_memory()  |  analyze_telemetry() / parse_logs()  |  verify_spec()  |  generate_report()", "#EA580C", "#FFF7ED"),
        (0.4, 0.20, 9.2, 0.92, "LAYER 4: PERSISTENCE & DATASET LAYER (memory.py)",
         "ChromaDB Vector Store (Past Incidents)  |  Telemetry Logs (CSV)  |  3GPP Limits (JSON)", "#15803D", "#F0FDF4"),
    ]

    for x, y, w, h, title, sub, edge, bg in layers:
        add_rounded_box(ax, x, y, w, h, edge=edge, bg=bg, lw=1.3, pad=0.05, zorder=2)
        ax.text(x + w / 2, y + h * 0.67, title, ha="center", va="center", fontsize=8.6, fontweight="bold", color=edge, zorder=3)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=7.5, color="#334155", zorder=3)

    # Clear 0.34-unit vertical arrows centered in each gap!
    add_arrow(ax, 5.0, 4.07, 5.0, 3.75, color="#1E3A8A", lw=1.8, style="->")
    add_arrow(ax, 5.0, 2.77, 5.0, 2.45, color="#EA580C", lw=1.8, style="<->")
    add_arrow(ax, 5.0, 1.47, 5.0, 1.15, color="#15803D", lw=1.8, style="<->")

    out_file = os.path.join(OUTPUT_DIR, "diag_capstone_architecture.png")
    plt.tight_layout(pad=0.2)
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")


# ----------------------------------------------------------------------
# 6. DIAGRAM: Pedagogical Roadmap (Clean Two-Box Role Banner, Clear Arrows)
# ----------------------------------------------------------------------
def generate_pedagogical_roadmap():
    fig, ax = plt.subplots(figsize=(9.5, 4.2), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    ax.text(5.0, 4.15, "5-DAY VALUE ADDED PROGRAM PEDAGOGICAL PROGRESSION ROADMAP",
            ha="center", va="center", fontsize=10.2, fontweight="bold", color="#1E3A8A")

    days_info = [
        ("Day 1:\nFoundations", "Deconstruct Buzzwords\nVector Math Basics\nChromaDB Init", "#1E3A8A", "#EFF6FF"),
        ("Day 2:\nProject 1", "Guided RAG Build\nDocument Ingestion\nQuery with Citations", "#1E3A8A", "#EFF6FF"),
        ("Day 3:\nThe Bridge", "ReAct While-Loop\nEpisodic Memory\nAAR Self-Correction", "#EA580C", "#FFF7ED"),
        ("Day 4:\nProject 2", "Capstone Hackathon\nIndependent Build\nTool Wiring Sprint", "#EA580C", "#FFF7ED"),
        ("Day 5:\nDefense", "Stress Testing\nUnseen Benchmarks\nLive Oral Defense", "#15803D", "#F0FDF4"),
    ]

    # 5 cards: width 1.60, gap 0.40 -> 5*1.60 + 4*0.40 = 9.60 -> start_x = 0.20
    card_w = 1.60
    gap = 0.40
    start_x = 0.20

    for idx, (title, sub, edge, bg) in enumerate(days_info):
        x = start_x + idx * (card_w + gap)
        add_rounded_box(ax, x, 1.30, card_w, 2.45, edge=edge, bg=bg, lw=1.3, pad=0.05, zorder=2)
        ax.text(x + card_w / 2, 3.25, title, ha="center", va="center", fontsize=8.2, fontweight="bold", color=edge, zorder=3)
        ax.text(x + card_w / 2, 2.15, sub, ha="center", va="center", fontsize=7.0, color="#334155", zorder=3)

        if idx < 4:
            add_arrow(ax, x + card_w + 0.04, 2.52, x + card_w + gap - 0.04, 2.52, color=edge, lw=1.7)

    # TWO separate role banners cleanly aligned under Days 1-3 and Days 4-5!
    # Days 1-3 span x = 0.20 to 0.20 + 3*1.60 + 2*0.40 = 5.80 (width 5.60)
    add_rounded_box(ax, 0.20, 0.22, 5.60, 0.80, edge="#1E3A8A", bg="#EFF6FF", lw=1.2, pad=0.05, zorder=2)
    ax.text(3.00, 0.62, "DAYS 1 - 3: INSTRUCTOR = MENTOR & CODE-ALONG LEAD",
            ha="center", va="center", fontsize=8.0, fontweight="bold", color="#1E3A8A", zorder=3)

    # Days 4-5 span x = 6.20 to 9.80 (width 3.60)
    add_rounded_box(ax, 6.20, 0.22, 3.60, 0.80, edge="#EA580C", bg="#FFF7ED", lw=1.2, pad=0.05, zorder=2)
    ax.text(8.00, 0.62, "DAYS 4 - 5: STRICT EVALUATOR\n(ZERO CODE ASSISTANCE)",
            ha="center", va="center", fontsize=7.8, fontweight="bold", color="#EA580C", zorder=3)

    out_file = os.path.join(OUTPUT_DIR, "diag_pedagogical_roadmap.png")
    plt.tight_layout(pad=0.2)
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")


# ----------------------------------------------------------------------
# 7. DIAGRAM: Error Recovery Flowchart (With Clear Return Loop Arrow)
# ----------------------------------------------------------------------
def generate_error_recovery_flow():
    fig, ax = plt.subplots(figsize=(9.5, 4.3), dpi=300)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    ax.text(5.0, 4.25, "AGENT ERROR INTERCEPTION & AUTONOMOUS SELF-HEALING FLOW",
            ha="center", va="center", fontsize=10.2, fontweight="bold", color="#1E3A8A")

    # Step 1: Tool Dispatch
    add_rounded_box(ax, 0.30, 1.35, 1.95, 2.00, edge="#1E3A8A", bg="#EFF6FF", lw=1.3, pad=0.05, zorder=2)
    ax.text(1.275, 2.95, "1. Tool Dispatch", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(1.275, 2.15, "Agent emits JSON\ncall: query_sensor()\nwith parameter args", ha="center", va="center", fontsize=7.2, color="#334155", zorder=3)

    add_arrow(ax, 2.28, 2.35, 2.72, 2.35, color="#1E3A8A", lw=1.7)

    # Step 2: Try / Except Block
    add_rounded_box(ax, 2.75, 1.35, 2.00, 2.00, edge="#EA580C", bg="#FFF7ED", lw=1.3, pad=0.05, zorder=2)
    ax.text(3.75, 2.95, "2. Try / Except", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#EA580C", zorder=3)
    ax.text(3.75, 2.15, "Local execution trap:\nDid function raise\nruntime exception?", ha="center", va="center", fontsize=7.2, color="#334155", zorder=3)

    # Branch A: Success (Top)
    add_arrow(ax, 4.78, 2.75, 5.22, 3.05, color="#15803D", lw=1.6)
    add_rounded_box(ax, 5.25, 2.55, 2.00, 1.25, edge="#15803D", bg="#F0FDF4", lw=1.3, pad=0.05, zorder=2)
    ax.text(6.25, 3.45, "Success Path", ha="center", va="center", fontsize=8.2, fontweight="bold", color="#15803D", zorder=3)
    ax.text(6.25, 2.95, "Appends valid string\nto agent history", ha="center", va="center", fontsize=7.2, color="#334155", zorder=3)

    # Branch B: Error Catch (Bottom)
    add_arrow(ax, 4.78, 1.95, 5.22, 1.65, color="#EA580C", lw=1.6)
    add_rounded_box(ax, 5.25, 0.95, 2.00, 1.25, edge="#EA580C", bg="#FFF7ED", lw=1.3, pad=0.05, zorder=2)
    ax.text(6.25, 1.85, "Error Catch Hook", ha="center", va="center", fontsize=8.2, fontweight="bold", color="#EA580C", zorder=3)
    ax.text(6.25, 1.35, "Wraps traceback as\n'Tool Error: <msg>'", ha="center", va="center", fontsize=7.2, color="#334155", zorder=3)

    # Step 3: Self-Reflection
    add_arrow(ax, 7.28, 1.58, 7.67, 1.58, color="#1E3A8A", lw=1.7)
    add_rounded_box(ax, 7.70, 0.95, 2.00, 2.85, edge="#1E3A8A", bg="#DBEAFE", lw=1.4, pad=0.05, zorder=2)
    ax.text(8.70, 3.38, "3. Self-Reflection", ha="center", va="center", fontsize=8.4, fontweight="bold", color="#1E3A8A", zorder=3)
    ax.text(8.70, 2.25, "LLM diagnoses fault:\n'Argument invalid.'\nFormulates repaired\ntool call.\nZero system crash.", ha="center", va="center", fontsize=7.2, color="#1E3A8A", zorder=3)

    # Return loop arrow along bottom corridor (y = 0.42) from Self-Reflection back to Tool Dispatch
    ax.plot([8.70, 8.70, 1.275], [0.92, 0.42, 0.42], color="#1E3A8A", lw=1.7, linestyle="--", zorder=4)
    add_arrow(ax, 1.275, 0.42, 1.275, 1.32, color="#1E3A8A", lw=1.7, ls="--")

    badge = patches.FancyBboxPatch((3.65, 0.25), 2.70, 0.34, boxstyle="round,pad=0.04",
                                   edgecolor="#1E3A8A", facecolor="#FFFFFF", linewidth=0.9, zorder=5)
    ax.add_patch(badge)
    ax.text(5.00, 0.42, "Next Autonomous Iteration", ha="center", va="center", fontsize=7.4, fontweight="bold", color="#1E3A8A", zorder=6)

    out_file = os.path.join(OUTPUT_DIR, "diag_error_recovery_flow.png")
    plt.tight_layout(pad=0.2)
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_file}")


if __name__ == "__main__":
    print("Regenerating all 7 diagrams with strict non-overlapping geometry...")
    generate_cover_graphic()
    generate_autonomy_spectrum()
    generate_rag_architecture()
    generate_react_loop()
    generate_capstone_architecture()
    generate_pedagogical_roadmap()
    generate_error_recovery_flow()
    print("All 7 diagrams regenerated successfully.")
