"""Generate 12 high-resolution (300 DPI) visuals and terminal/report outputs for Days 1-5 VAP slides."""

from __future__ import annotations

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt

OUTPUT_DIR = r"C:\Users\lapto\Desktop\demo\BEN\VAP\images\ppt"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BLUE = "#1E3A8A"
BLUE_LT = "#EFF6FF"
BLUE_MID = "#3B82F6"
ORANGE = "#EA580C"
ORANGE_LT = "#FFF7ED"
GREEN = "#15803D"
GREEN_LT = "#F0FDF4"
SLATE_DARK = "#0F172A"
SLATE_MED = "#334155"
SLATE_MUTED = "#64748B"
BORDER = "#CBD5E1"
BG_LIGHT = "#F8FAFC"


def rbox(ax, x, y, w, h, edge=BLUE, bg="#FFFFFF", lw=1.6, pad=0.06, zorder=2):
    p = patches.FancyBboxPatch(
        (x + pad, y + pad),
        w - 2 * pad,
        h - 2 * pad,
        boxstyle=f"round,pad={pad}",
        edgecolor=edge,
        facecolor=bg,
        linewidth=lw,
        zorder=zorder,
    )
    ax.add_patch(p)
    return p


def arrow(ax, x1, y1, x2, y2, color=BLUE, lw=1.8, style="->", ls="solid", zorder=5):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle=f"{style},head_width=0.28,head_length=0.38",
            color=color,
            lw=lw,
            linestyle=ls,
            shrinkA=2,
            shrinkB=2,
        ),
        zorder=zorder,
    )


def render_terminal_card(filename: str, title: str, lines: list[tuple[str, str]], figsize=(11.0, 5.2), font_size=9.3):
    """Render a crisp dark PowerShell terminal output card."""
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    # Terminal outer shell
    rbox(ax, 0.1, 0.1, 9.8, 5.0, edge="#1E293B", bg="#0B1220", lw=1.8, pad=0.08, zorder=1)
    # Title bar
    rbox(ax, 0.1, 4.55, 9.8, 0.55, edge="#1E293B", bg="#1E293B", lw=1.0, pad=0.04, zorder=2)
    # Window dots
    for idx, col in enumerate(("#EF4444", "#F59E0B", "#22C55E")):
        ax.add_patch(patches.Circle((0.42 + idx * 0.26, 4.82), 0.085, facecolor=col, zorder=3))
    ax.text(5.0, 4.82, title, ha="center", va="center", fontsize=10, fontweight="bold", color="#E2E8F0", fontfamily="DejaVu Sans Mono", zorder=3)

    y = 4.25
    step = (4.25 - 0.30) / max(len(lines), 1)
    for text, color in lines:
        ax.text(0.32, y, text, ha="left", va="center", fontsize=font_size, color=color, fontfamily="DejaVu Sans Mono", zorder=4)
        y -= step

    out_path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(out_path, dpi=300, bbox_inches="tight", pad_inches=0.04, facecolor="#FFFFFF")
    plt.close(fig)


def make_1_env_setup_pipeline():
    fig, ax = plt.subplots(figsize=(12.2, 3.2), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 14.6)
    ax.set_ylim(0, 3.6)
    ax.axis("off")

    steps = [
        ("1", "Python 3.13", "Add to PATH\npython --version", BLUE, BLUE_LT),
        ("2", "uv Manager", "pip install uv\nuv init / uv add", BLUE, BLUE_LT),
        ("3", "Git & GitHub", "Git for Windows\ngit config user", BLUE, BLUE_LT),
        ("4", "Antigravity x64", "Standalone IDE\nTerminal + Editor", BLUE, BLUE_LT),
        ("5", "Groq API Key", "console.groq.com\nFree Tier Account", ORANGE, ORANGE_LT),
        ("6", ".env + ignore", "GROQ_API_KEY=...\nZero Secret Leaks", ORANGE, ORANGE_LT),
        ("7", "verify.py", "HTTPS Check\nHello! Response", GREEN, GREEN_LT),
    ]

    w = 1.78
    gap = 0.25
    x0 = 0.30
    for i, (num, title, desc, ec, bg) in enumerate(steps):
        x = x0 + i * (w + gap)
        rbox(ax, x, 0.45, w, 2.55, edge=ec, bg="#FFFFFF", lw=1.7, pad=0.06, zorder=2)
        ax.add_patch(patches.Circle((x + w / 2, 2.75), 0.22, facecolor=ec, zorder=3))
        ax.text(x + w / 2, 2.75, num, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#FFFFFF", zorder=4)
        ax.text(x + w / 2, 2.15, title, ha="center", va="center", fontsize=9.2, fontweight="bold", color=SLATE_DARK, zorder=3)
        ax.text(x + w / 2, 1.25, desc, ha="center", va="center", fontsize=7.9, color=SLATE_MED, linespacing=1.45, zorder=3)
        if i < len(steps) - 1:
            arrow(ax, x + w + 0.02, 1.72, x + w + gap - 0.02, 1.72, color=ec, lw=1.8)

    ax.text(7.3, 3.35, "7-STEP ZERO-GPU WINDOWS ENVIRONMENT & API PIPELINE", ha="center", va="center", fontsize=10.5, fontweight="bold", color=BLUE)
    fig.savefig(os.path.join(OUTPUT_DIR, "visual_env_setup_pipeline.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_2_cosine_similarity_2d():
    fig, ax = plt.subplots(figsize=(6.2, 5.0), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Vectors in normalized 2D projection
    q = np.array([0.82, 0.57])
    q = q / np.linalg.norm(q)
    d1 = np.array([0.55, 0.83])
    d1 = d1 / np.linalg.norm(d1) * 0.92
    d2 = np.array([0.96, 0.02])
    d2 = d2 / np.linalg.norm(d2) * 0.82
    d3 = np.array([-0.38, 0.72])
    d3 = d3 / np.linalg.norm(d3) * 0.76

    # Grid & axes
    ax.axhline(0, color="#CBD5E1", lw=1.0, zorder=1)
    ax.axvline(0, color="#CBD5E1", lw=1.0, zorder=1)
    ax.grid(True, linestyle="--", alpha=0.4, color="#CBD5E1", zorder=0)

    def draw_vec(v, color, label, offx=0.02, offy=0.03, lw=2.5):
        ax.annotate("", xy=(v[0], v[1]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color=color, lw=lw), zorder=4)
        ax.text(v[0] + offx, v[1] + offy, label, fontsize=8.3, fontweight="bold", color=color,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor=color, alpha=0.95), zorder=5)

    draw_vec(q, ORANGE, 'Query: "How does a transistor work?"', offx=-0.22, offy=-0.16, lw=2.8)
    draw_vec(d1, GREEN, 'Doc 1: "MOSFET gate voltage..."\ncos(theta) = 0.89 (TOP MATCH)', offx=-0.32, offy=0.05)
    draw_vec(d2, BLUE, 'Doc 2: "Capacitor stores energy..."\ncos(theta) = 0.54 (Moderate)', offx=-0.42, offy=-0.17)
    draw_vec(d3, SLATE_MUTED, 'Doc 3: "Python programming..."\ncos(theta) = 0.12 (Unrelated)', offx=-0.22, offy=0.06)

    # Arc between Q and Doc 1
    theta_q = np.degrees(np.arctan2(q[1], q[0]))
    theta_d1 = np.degrees(np.arctan2(d1[1], d1[0]))
    arc = patches.Arc((0, 0), 0.55, 0.55, angle=0, theta1=min(theta_q, theta_d1), theta2=max(theta_q, theta_d1),
                      color=GREEN, lw=2.0, linestyle="--", zorder=3)
    ax.add_patch(arc)
    ax.text(0.24, 0.30, "Small\nAngle", fontsize=7.8, fontweight="bold", color=GREEN, ha="center")

    ax.set_xlim(-0.65, 1.18)
    ax.set_ylim(-0.32, 1.12)
    ax.set_xlabel("Latent Dimension 1 (Hardware / Physics Axis)", fontsize=9, fontweight="bold", color=SLATE_MED)
    ax.set_ylabel("Latent Dimension 2 (Semantic Concept Axis)", fontsize=9, fontweight="bold", color=SLATE_MED)
    ax.set_title("Cosine Similarity in 2D Embedding Space (Zero Shared Keywords!)", fontsize=10.5, fontweight="bold", color=BLUE, pad=10)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_cosine_similarity_2d.png"), dpi=300, bbox_inches="tight", pad_inches=0.06, facecolor="#FFFFFF")
    plt.close(fig)


def make_3_chunking_sliding_window():
    fig, ax = plt.subplots(figsize=(11.0, 4.0), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.3)
    ax.axis("off")

    ax.text(6.0, 4.02, "SENTENCE-AWARE CHUNKING + OVERLAP + HNSW INDEXING", ha="center", va="center", fontsize=11, fontweight="bold", color=BLUE)

    # Source Document
    rbox(ax, 0.3, 2.75, 11.4, 0.95, edge=BLUE, bg=BLUE_LT, lw=1.6)
    ax.text(0.55, 3.45, "SOURCE DOCUMENT: power_electronics_handbook.md (1,420 chars)", ha="left", va="center", fontsize=9.2, fontweight="bold", color=BLUE)
    ax.text(0.55, 3.05, "[S1] MOSFETs control drain current via gate voltage.  [S2] Threshold Vgs triggers conduction.  [S3] Gate drivers need decoupling.  [S4] Flyback diodes protect coils.", ha="left", va="center", fontsize=8.3, color=SLATE_DARK)

    # Overlap Chunks
    chunks = [
        (0.3, "Chunk 0 (max_chars=500)", "[S1] + [S2]\nmeta: {source: handbook, chunk: 0}", BLUE, "#FFFFFF"),
        (4.1, "Chunk 1 (Overlap Window)", "[S2] + [S3]\nmeta: {source: handbook, chunk: 1}", ORANGE, ORANGE_LT),
        (7.9, "Chunk 2 (Trailing Window)", "[S3] + [S4]\nmeta: {source: handbook, chunk: 2}", BLUE, "#FFFFFF"),
    ]
    for cx, title, body, ec, bg in chunks:
        rbox(ax, cx, 1.35, 3.5, 1.05, edge=ec, bg=bg, lw=1.6)
        ax.text(cx + 1.75, 2.15, title, ha="center", va="center", fontsize=9.0, fontweight="bold", color=ec)
        ax.text(cx + 1.75, 1.70, body, ha="center", va="center", fontsize=8.0, color=SLATE_MED, linespacing=1.35)
        arrow(ax, cx + 1.75, 2.74, cx + 1.75, 2.42, color=ec, lw=1.6)
        arrow(ax, cx + 1.75, 1.34, 6.0, 0.92, color=GREEN, lw=1.5)

    # HNSW Index Bar
    rbox(ax, 1.5, 0.18, 9.0, 0.72, edge=GREEN, bg=GREEN_LT, lw=1.8)
    ax.text(6.0, 0.64, "ChromaDB HNSW Vector Index  (384-dim Embeddings)", ha="center", va="center", fontsize=9.6, fontweight="bold", color=GREEN)
    ax.text(6.0, 0.36, "Brute-Force Scan: O(N)   --->   HNSW Hierarchical Graph Lookup: O(log N)", ha="center", va="center", fontsize=8.5, fontweight="bold", color=SLATE_DARK)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_chunking_sliding_window.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_4_day1_terminal():
    lines = [
        ("PS C:\\Users\\student\\vap-agentic-ai> python --version", "#38BDF8"),
        ("Python 3.13.2", "#E2E8F0"),
        ("PS C:\\Users\\student\\vap-agentic-ai> uv --version", "#38BDF8"),
        ("uv 0.5.14 (Windows x86_64)", "#E2E8F0"),
        ("PS C:\\Users\\student\\vap-agentic-ai> uv init && uv add chromadb requests python-dotenv pydantic duckduckgo-search", "#38BDF8"),
        ("Resolved 48 packages in 1.42s | Installed 48 packages in 0.85s", "#94A3B8"),
        ("PS C:\\Users\\student\\vap-agentic-ai> uv run python verify.py", "#38BDF8"),
        ("API Connected: Hello!", "#4ADE80"),
        ("PS C:\\Users\\student\\vap-agentic-ai> uv run python chroma_demo.py", "#38BDF8"),
        ("Query: 'How does a transistor work?'", "#FBBF24"),
        ("Top Match [dist=0.22]: 'The MOSFET gate voltage controls the drain current.'", "#4ADE80"),
        ("Runner-Up [dist=0.91]: 'A capacitor stores energy in an electric field.'", "#CBD5E1"),
    ]
    render_terminal_card("output_day1_terminal.png", "Windows PowerShell — Day 1 Environment & ChromaDB Verification", lines, figsize=(11.2, 4.6), font_size=8.9)


def make_5_project1_folder_tree():
    fig, ax = plt.subplots(figsize=(11.2, 4.4), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    # Left: Folder Tree
    rbox(ax, 0.25, 0.25, 4.35, 4.1, edge=SLATE_DARK, bg="#0F172A", lw=1.6)
    ax.text(0.5, 4.02, "PROJECT 1 WORKSPACE", ha="left", va="center", fontsize=10, fontweight="bold", color="#F97316", fontfamily="DejaVu Sans Mono")
    tree_lines = [
        ("vap-agentic-ai/", "#38BDF8"),
        ("  |-- .env               # GROQ_API_KEY", "#4ADE80"),
        ("  |-- .gitignore         # hides .env & .venv", "#94A3B8"),
        ("  |-- pyproject.toml     # uv deps", "#E2E8F0"),
        ("  |-- verify.py          # Day 1 API test", "#E2E8F0"),
        ("  |-- ingest.py          # Day 2 chunk & index", "#FBBF24"),
        ("  |-- query.py           # Day 2 RAG + Groq", "#FBBF24"),
        ("  |-- knowledge_base/    # .md / .txt manuals", "#CBD5E1"),
        ("  +-- chroma_db/         # Persistent HNSW", "#38BDF8"),
    ]
    y = 3.55
    for txt, col in tree_lines:
        ax.text(0.45, y, txt, ha="left", va="center", fontsize=8.8, color=col, fontfamily="DejaVu Sans Mono")
        y -= 0.37

    # Right: Data Flow
    nodes = [
        (5.15, 2.8, 2.9, 1.35, "1. INGESTION (ingest.py)", "Load .md/.txt files\nSplit on sentence bounds\nAttach source + chunk ID", BLUE, BLUE_LT),
        (8.7, 2.8, 2.95, 1.35, "2. VECTOR DB (chroma_db/)", "PersistentClient storage\n384-dim HNSW index\nCosine similarity metric", GREEN, GREEN_LT),
        (8.7, 0.55, 2.95, 1.35, "3. RETRIEVAL (query.py)", "Embed user question\nFetch top-k chunks\nFilter out irrelevant hits", ORANGE, ORANGE_LT),
        (5.15, 0.55, 2.9, 1.35, "4. GENERATION (Groq LLM)", "Llama 3.3 70B Versatile\nStrict context grounding\n[Source: file (chunk N)]", BLUE, BLUE_LT),
    ]
    for nx, ny, nw, nh, title, body, ec, bg in nodes:
        rbox(ax, nx, ny, nw, nh, edge=ec, bg=bg, lw=1.7)
        ax.text(nx + nw / 2, ny + nh - 0.25, title, ha="center", va="center", fontsize=9.0, fontweight="bold", color=ec)
        ax.text(nx + nw / 2, ny + 0.52, body, ha="center", va="center", fontsize=8.2, color=SLATE_DARK, linespacing=1.35)

    arrow(ax, 8.08, 3.48, 8.67, 3.48, color=BLUE, lw=2.0)
    arrow(ax, 10.17, 2.77, 10.17, 1.93, color=GREEN, lw=2.0)
    arrow(ax, 8.67, 1.22, 8.08, 1.22, color=ORANGE, lw=2.0)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_project1_folder_tree.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_6_day2_rag_tests():
    fig, ax = plt.subplots(figsize=(11.4, 4.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.0)
    ax.axis("off")

    panels = [
        (0.2, "TEST 1: IN-DOMAIN QUERY (GROUNDED)", GREEN, [
            ("> uv run python query.py", "#38BDF8"),
            ("Q: How do you protect an inductive load?", "#FBBF24"),
            ("Top-k retrieved: power_notes.md [0, 2]", "#94A3B8"),
            ("Answer: Place a flyback diode across the", "#4ADE80"),
            ("coil terminals to clamp voltage spikes", "#4ADE80"),
            ("during MOSFET turn-off transients.", "#4ADE80"),
            ("[Source: power_notes.md (chunk 2)]", "#A7F3D0"),
        ]),
        (4.1, "TEST 2: OUT-OF-DOMAIN (NO HALLUCINATION)", ORANGE, [
            ("> uv run python query.py", "#38BDF8"),
            ("Q: Who won the 2024 FIFA World Cup?", "#FBBF24"),
            ("Max cosine similarity = 0.14 (< 0.45)", "#94A3B8"),
            ("Answer: I don't have enough information", "#FB923C"),
            ("in the provided technical documents to", "#FB923C"),
            ("answer that question.", "#FB923C"),
            ("[Status: SAFE REFUSAL VERIFIED]", "#FDE68A"),
        ]),
        (8.0, "TEST 3: AMBIGUOUS QUERY + GIT PUSH", BLUE, [
            ("> uv run python query.py", "#38BDF8"),
            ("Q: Explain threshold behavior.", "#FBBF24"),
            ("Retrieved: mosfet.md [1] & adc.md [3]", "#94A3B8"),
            ("Answer: Clarifies both MOSFET Vgs(th)", "#E2E8F0"),
            ("and ADC comparator hysteresis bounds.", "#E2E8F0"),
            ("> git commit -m 'Project 1 RAG' && push", "#38BDF8"),
            ("[main 8a4f2c1] Pushed to origin/main", "#4ADE80"),
        ]),
    ]

    for px, title, ec, lines in panels:
        rbox(ax, px, 0.2, 3.75, 4.6, edge=ec, bg="#0B1220", lw=1.8)
        rbox(ax, px, 4.28, 3.75, 0.52, edge=ec, bg=ec, lw=1.0, pad=0.02)
        ax.text(px + 1.875, 4.54, title, ha="center", va="center", fontsize=8.0, fontweight="bold", color="#FFFFFF")
        y = 3.85
        for txt, col in lines:
            ax.text(px + 0.15, y, txt, ha="left", va="center", fontsize=7.6, color=col, fontfamily="DejaVu Sans Mono")
            y -= 0.52

    fig.savefig(os.path.join(OUTPUT_DIR, "output_day2_rag_tests.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_7_dual_memory_architecture():
    fig, ax = plt.subplots(figsize=(11.2, 4.6), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    ax.text(6.0, 4.52, "DUAL-MEMORY AGENT ARCHITECTURE (memory.py)", ha="center", va="center", fontsize=11, fontweight="bold", color=BLUE)

    # Left: Short-Term Memory
    rbox(ax, 0.35, 1.35, 4.5, 2.85, edge=ORANGE, bg=ORANGE_LT, lw=1.8)
    ax.text(2.6, 3.88, "SHORT-TERM WORKING MEMORY", ha="center", va="center", fontsize=10, fontweight="bold", color=ORANGE)
    ax.text(2.6, 3.55, "LLM Context Window & Messages List", ha="center", va="center", fontsize=8.5, fontweight="bold", color=SLATE_MED)
    ax.text(2.6, 2.55, "- Holds current goal & active step trace\n- Stores recent tool_calls & Observations\n- Fast, exact, in-session reasoning\n- LIMITATION: Volatile (wiped on exit)", ha="center", va="center", fontsize=8.6, color=SLATE_DARK, linespacing=1.55)

    # Right: Long-Term Episodic Memory
    rbox(ax, 7.15, 1.35, 4.5, 2.85, edge=BLUE, bg=BLUE_LT, lw=1.8)
    ax.text(9.4, 3.88, "LONG-TERM EPISODIC MEMORY", ha="center", va="center", fontsize=10, fontweight="bold", color=BLUE)
    ax.text(9.4, 3.55, "ChromaDB Persistent Vector Store (./agent_memory)", ha="center", va="center", fontsize=8.5, fontweight="bold", color=SLATE_MED)
    ax.text(9.4, 2.55, "- Survives restarts across sessions\n- Indexed by cosine similarity embeddings\n- Stores past root causes & operational rules\n- Metadata categories: incident / aar_lesson", ha="center", va="center", fontsize=8.6, color=SLATE_DARK, linespacing=1.55)

    # Center Tools
    rbox(ax, 5.15, 2.95, 1.7, 0.9, edge=GREEN, bg=GREEN_LT, lw=1.6)
    ax.text(6.0, 3.53, "recall_memory()", ha="center", va="center", fontsize=8.4, fontweight="bold", color=GREEN)
    ax.text(6.0, 3.20, "Query top-k\nprior lessons", ha="center", va="center", fontsize=7.6, color=SLATE_MED)

    rbox(ax, 5.15, 1.65, 1.7, 0.9, edge=BLUE, bg="#FFFFFF", lw=1.6)
    ax.text(6.0, 2.23, "store_memory()", ha="center", va="center", fontsize=8.4, fontweight="bold", color=BLUE)
    ax.text(6.0, 1.90, "Persist verified\nobservations", ha="center", va="center", fontsize=7.6, color=SLATE_MED)

    arrow(ax, 7.12, 3.40, 6.88, 3.40, color=GREEN, lw=1.8)
    arrow(ax, 5.12, 3.40, 4.88, 3.40, color=GREEN, lw=1.8)
    arrow(ax, 4.88, 2.10, 5.12, 2.10, color=BLUE, lw=1.8)
    arrow(ax, 6.88, 2.10, 7.12, 2.10, color=BLUE, lw=1.8)

    # Bottom AAR bar
    rbox(ax, 1.6, 0.25, 8.8, 0.82, edge=GREEN, bg=GREEN_LT, lw=1.7)
    ax.text(6.0, 0.78, "POST-EXECUTION AFTER ACTION REVIEW (AAR)", ha="center", va="center", fontsize=9.2, fontweight="bold", color=GREEN)
    ax.text(6.0, 0.48, "Compares Goal vs Trace -> Extracts 1-Sentence Operational Rule -> Commits to Long-Term ChromaDB Memory", ha="center", va="center", fontsize=8.3, color=SLATE_DARK)
    arrow(ax, 9.4, 0.85, 9.4, 1.32, color=GREEN, lw=1.8)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_dual_memory_architecture.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_8_day3_react_trace():
    lines = [
        ("Enter goal: Diagnose thermal anomaly on Node-14 and save summary.", "#FBBF24"),
        ("--- Step 1 --- Action: recall_memory({'query': 'Node-14 thermal anomaly', 'top_k': 2})", "#38BDF8"),
        ("Observation: [aar_lesson] Check data/ subfolder for telemetry CSV logs.", "#4ADE80"),
        ("--- Step 2 --- Action: read_file({'filepath': 'sensor_logs.csv'})", "#38BDF8"),
        ("Observation: Tool execution error: File 'sensor_logs.csv' not found.", "#F87171"),
        ("--- Step 3 --- (Self-Healing Retry using memory hint!)", "#FB923C"),
        ("Action: read_file({'filepath': 'data/sensor_logs.csv'})", "#38BDF8"),
        ("Observation: node_id,temp_c,vbat | N14,68.4,2.71V (voltage brownout spike)", "#E2E8F0"),
        ("--- Step 4 --- Action: store_memory({'category': 'incident', 'observation': 'N14 spike from Vbat<2.8V'})", "#38BDF8"),
        ("Observation: Stored memory under category 'incident'.", "#4ADE80"),
        ("--- Step 5 --- FINAL ANSWER: Node-14 thermal drift correlates with Vbat drop (2.71V). Replace battery.", "#4ADE80"),
        ("[AAR Stored]: Always verify path 'data/sensor_logs.csv' when root CSV lookup fails.", "#A7F3D0"),
    ]
    render_terminal_card("output_day3_react_trace.png", "agent.py — Live ReAct Execution, Self-Healing & AAR Trace", lines, figsize=(11.4, 4.9), font_size=8.3)


def make_9_capstone_3_tracks():
    fig, ax = plt.subplots(figsize=(11.6, 4.9), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.1)
    ax.axis("off")

    ax.text(6.0, 4.82, "CAPSTONE PROJECT 2 — CHOOSE 1 OF 3 PROBLEM STATEMENTS", ha="center", va="center", fontsize=11.5, fontweight="bold", color=BLUE)

    tracks = [
        (0.25, "TRACK 1: ECE EMBEDDED", "IoT Sensor Diagnostic Agent", BLUE, BLUE_LT,
         "Scenario:\n50-node campus sensor network\nshows intermittent anomalies.\nDiagnose drift vs power vs RF.",
         "Required Tools (4):\n1. query_incident_memory\n2. analyze_sensor_telemetry\n3. check_network_topology\n4. generate_diagnostic_report",
         "Mock Data:\nsensor_logs.csv (500 rows)\npast_incidents.json (15)\nnetwork_topology.json"),
        (4.15, "TRACK 2: ECE TELECOM", "5G/3GPP Compliance Agent", ORANGE, ORANGE_LT,
         "Scenario:\nVerify 5G NR base station logs\n(EVM, Tx power, freq offset)\nagainst 3GPP spec thresholds.",
         "Required Tools (4):\n1. query_compliance_memory\n2. parse_test_log\n3. verify_against_spec\n4. generate_compliance_report",
         "Mock Data:\nfirmware_test_output.json (50)\n3gpp_spec_thresholds.json\npast_compliance_tests.json (20)"),
        (8.05, "TRACK 3: ACADEMIC CORE", "Research Literature Survey Agent", GREEN, GREEN_LT,
         "Scenario:\nSurvey paper corpus + live web\nfor Edge AI / Neuromorphic\n8th-sem project & find gaps.",
         "Required Tools (4):\n1. query_literature_memory\n2. search_web\n3. extract_themes\n4. generate_literature_review",
         "Mock Data:\npaper_abstracts.json (40 papers)\n+ Live DuckDuckGo Search"),
    ]

    for x, tag, title, ec, bg, scen, tools, data in tracks:
        rbox(ax, x, 0.25, 3.7, 4.3, edge=ec, bg="#FFFFFF", lw=1.8)
        rbox(ax, x, 3.82, 3.7, 0.73, edge=ec, bg=ec, lw=1.0, pad=0.02)
        ax.text(x + 1.85, 4.30, tag, ha="center", va="center", fontsize=8.2, fontweight="bold", color="#E2E8F0")
        ax.text(x + 1.85, 4.00, title, ha="center", va="center", fontsize=9.8, fontweight="bold", color="#FFFFFF")

        rbox(ax, x + 0.14, 2.65, 3.42, 1.05, edge=BORDER, bg=bg, lw=1.0)
        ax.text(x + 0.25, 3.17, scen, ha="left", va="center", fontsize=8.0, color=SLATE_DARK, linespacing=1.32)

        rbox(ax, x + 0.14, 1.32, 3.42, 1.22, edge=BORDER, bg="#FFFFFF", lw=1.0)
        ax.text(x + 0.25, 1.93, tools, ha="left", va="center", fontsize=8.0, color=SLATE_DARK, fontweight="bold", linespacing=1.35)

        rbox(ax, x + 0.14, 0.38, 3.42, 0.84, edge=BORDER, bg=BG_LIGHT, lw=1.0)
        ax.text(x + 0.25, 0.80, data, ha="left", va="center", fontsize=7.8, color=SLATE_MED, fontfamily="DejaVu Sans Mono", linespacing=1.3)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_capstone_3_tracks.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_10_day4_smoke_test():
    lines = [
        ("PS C:\\Users\\student\\capstone-agent> uv run python ingest_domain.py", "#38BDF8"),
        ("Indexed 35 historical records + specs into ./capstone_memory (ChromaDB)", "#4ADE80"),
        ("PS C:\\Users\\student\\capstone-agent> uv run python main.py --smoke-test", "#38BDF8"),
        ("[Step 1/10] Thought -> Call: query_incident_memory(query='high EVM and Tx drift')", "#E2E8F0"),
        ("[Step 1] Observation: Returned 3 matching prior RF firmware incidents.", "#94A3B8"),
        ("[Step 2/10] Thought -> Call: parse_test_log(filepath='data/firmware_test_output.json')", "#E2E8F0"),
        ("[Step 2] Observation: Extracted 50 RF measurements (Channel 1..50).", "#94A3B8"),
        ("[Step 3/10] Thought -> Call: verify_against_spec(params_json='...')", "#E2E8F0"),
        ("[Step 3] Observation: 2 FAILURES (EVM 4.8% > 3.5% limit; ACLR -41dBc < -45dBc).", "#FBBF24"),
        ("[Step 4/10] Thought -> Call: generate_compliance_report(filename='out/report.md')", "#E2E8F0"),
        ("Smoke Test PASS: 4 autonomous tool calls executed, zero unhandled exceptions.", "#4ADE80"),
        ("PS C:\\Users\\student\\capstone-agent> git add . && git commit -m 'Day 4 Milestone' && git push", "#38BDF8"),
    ]
    render_terminal_card("output_day4_smoke_test.png", "Day 4 Session 3 (16:30) — Unassisted Milestone Smoke Test & Git Checkpoint", lines, figsize=(11.4, 4.9), font_size=8.4)


def make_11_grading_rubric_chart():
    fig, ax = plt.subplots(figsize=(7.8, 4.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    labels = [
        "P2: Code Quality & Docs",
        "P2: Live Defense Benchmark",
        "P2: Self-Healing & Recovery",
        "P2: Tool Calling & Schemas",
        "P2: Vector Memory Integration",
        "P2: True Agentic Control Flow*",
        "P1: RAG-Augmented Generation",
        "P1: Semantic Retrieval",
        "P1: Document Ingestion",
    ]
    scores = [5, 10, 10, 10, 15, 20, 10, 10, 10]
    bar_colors = [ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, "#B91C1C", BLUE, BLUE, BLUE]

    y = np.arange(len(labels))
    bars = ax.barh(y, scores, color=bar_colors, height=0.62, edgecolor="#0F172A", linewidth=0.7)

    for bar, s in zip(bars, scores):
        ax.text(s + 0.4, bar.get_y() + bar.get_height() / 2, f"{s} pts", va="center", ha="left", fontsize=9.0, fontweight="bold", color=SLATE_DARK)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.8, fontweight="bold", color=SLATE_DARK)
    ax.set_xlim(0, 24.5)
    ax.set_xlabel("Maximum Points (Total = 100 Points: Project 1 = 30 pts | Project 2 = 70 pts)", fontsize=8.8, fontweight="bold", color=SLATE_MED)
    ax.set_title("VAP Evaluation & Grading Rubric Breakdown (*Hardcoded Pipeline = 0 pts)", fontsize=10.2, fontweight="bold", color=BLUE, pad=10)
    ax.grid(axis="x", linestyle="--", alpha=0.45, color="#CBD5E1")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_grading_rubric_chart.png"), dpi=300, bbox_inches="tight", pad_inches=0.06, facecolor="#FFFFFF")
    plt.close(fig)


def make_12_day5_defense_outputs():
    fig, ax = plt.subplots(figsize=(11.6, 4.9), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.1)
    ax.axis("off")

    # Left: Unseen Prompt Live Run
    rbox(ax, 0.2, 0.2, 5.65, 4.7, edge=BLUE, bg="#0B1220", lw=1.8)
    rbox(ax, 0.2, 4.35, 5.65, 0.55, edge=BLUE, bg=BLUE, lw=1.0, pad=0.02)
    ax.text(3.025, 4.62, "DAY 5 UNSEEN BENCHMARK RUN (LIVE DEFENSE)", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#FFFFFF")
    left_lines = [
        ("> uv run python main.py", "#38BDF8"),
        ("Evaluator Prompt: 'Audit node_batch_B.json;", "#FBBF24"),
        ("corrupt fields may exist. Recall past fixes.'", "#FBBF24"),
        ("Step 1: recall_memory('corrupt telemetry') -> hit", "#4ADE80"),
        ("Step 2: parse_log -> ERR: NaN voltage on ch_04", "#F87171"),
        ("Step 3: Self-Healed -> skipped NaN, flagged ch_04", "#FB923C"),
        ("Step 4: verify_against_spec -> 3 pass, 1 FAIL", "#E2E8F0"),
        ("Step 5: generate_report -> out/audit_B.md", "#4ADE80"),
        ("Step 6: AAR stored + FINAL ANSWER emitted (4.8s)", "#A7F3D0"),
    ]
    y = 3.98
    for txt, col in left_lines:
        ax.text(0.38, y, txt, ha="left", va="center", fontsize=8.0, color=col, fontfamily="DejaVu Sans Mono")
        y -= 0.43

    # Right: Generated Markdown Report Artifact
    rbox(ax, 6.15, 0.2, 5.65, 4.7, edge=GREEN, bg=BG_LIGHT, lw=1.8)
    rbox(ax, 6.15, 4.35, 5.65, 0.55, edge=GREEN, bg=GREEN, lw=1.0, pad=0.02)
    ax.text(8.975, 4.62, "GENERATED ARTIFACT: out/audit_B.md", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#FFFFFF")
    right_lines = [
        ("# Autonomous Diagnostic & Compliance Report", BLUE, "bold"),
        ("- Target Dataset: node_batch_B.json", SLATE_DARK, "normal"),
        ("- Overall Verdict: FAIL (Action Required)", "#B91C1C", "bold"),
        ("", SLATE_DARK, "normal"),
        ("## Root Cause Analysis", ORANGE, "bold"),
        ("1. Sensor ch_04 reported NaN (ADC dropout).", SLATE_DARK, "normal"),
        ("2. Tx EVM measured 4.9% (Limit <= 3.5%).", SLATE_DARK, "normal"),
        ("", SLATE_DARK, "normal"),
        ("## Recalled Episodic Precedent [INC-2025-07]", BLUE, "bold"),
        ("Matches Feb-2025 PA bias thermal drift event.", SLATE_MED, "normal"),
        ("Action: Re-run calibration + inspect LDO rail.", GREEN, "bold"),
    ]
    y = 3.98
    for txt, col, weight in right_lines:
        if txt:
            ax.text(6.35, y, txt, ha="left", va="center", fontsize=8.3, color=col, fontweight=weight, fontfamily="DejaVu Sans")
        y -= 0.34

    fig.savefig(os.path.join(OUTPUT_DIR, "output_day5_defense_outputs.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_13_ground_rules():
    fig, ax = plt.subplots(figsize=(11.6, 5.0), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    rules = [
        (0.25, 2.75, "01", "Understand Every Line", "Never copy-paste blindly.\nRead how each line executes.", BLUE),
        (6.15, 2.75, "02", "Zero Leaked Secrets", "Never hardcode gsk_... keys\nor stage .env to GitHub.", "#B91C1C"),
        (0.25, 0.25, "03", "Debug From Traces", "Treat Python tracebacks as\nclues, not failures.", ORANGE),
        (6.15, 0.25, "04", "Mentor -> Evaluator", "Days 1-3: Ask anything.\nDays 4-5: Unassisted sprint.", GREEN),
    ]
    for x, y, num, title, body, ec in rules:
        rbox(ax, x, y, 5.6, 2.2, edge=BORDER, bg="#FFFFFF", lw=1.6)
        rbox(ax, x + 0.25, y + 1.25, 0.72, 0.65, edge=ec, bg=ec, lw=1.0, pad=0.02)
        ax.text(x + 0.61, y + 1.57, num, ha="center", va="center", fontsize=14, fontweight="bold", color="#FFFFFF")
        ax.text(x + 1.18, y + 1.57, title, ha="left", va="center", fontsize=13.5, fontweight="bold", color=SLATE_DARK)
        ax.text(x + 1.18, y + 0.72, body, ha="left", va="center", fontsize=11.0, color=SLATE_MED, linespacing=1.4)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_ground_rules.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_14_failure_modes_2x2():
    fig, ax = plt.subplots(figsize=(11.6, 5.0), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    modes = [
        (0.25, 2.75, "1. Chunk Too Small (<100 chars)", "Loses component & unit context.\nFix: Target 400-600 chars cleanly.", ORANGE),
        (6.15, 2.75, "2. Chunk Too Large (>2000 chars)", "Averages 5 topics into 1 blurry vector.\nFix: Keep 1 concept per chunk.", BLUE),
        (0.25, 0.25, "3. Zero Boundary Overlap", "Answer straddles chunk split cleanly.\nFix: Carry 1-sentence overlap.", ORANGE),
        (6.15, 0.25, "4. Missing Distance Cutoff", "Chroma always returns top_k garbage.\nFix: Filter out dist > max_distance.", "#B91C1C"),
    ]
    for x, y, title, body, ec in modes:
        rbox(ax, x, y, 5.6, 2.2, edge=ec, bg="#FFFFFF", lw=1.8)
        ax.text(x + 0.35, y + 1.62, title, ha="left", va="center", fontsize=12.5, fontweight="bold", color=ec)
        ax.text(x + 0.35, y + 0.80, body, ha="left", va="center", fontsize=11.0, color=SLATE_DARK, linespacing=1.48)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_failure_modes_2x2.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_15_upsert_vs_add():
    fig, ax = plt.subplots(figsize=(11.4, 4.6), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    rbox(ax, 0.3, 0.3, 5.4, 4.2, edge="#B91C1C", bg="#FFFFFF", lw=1.8)
    ax.text(3.0, 4.05, "collection.add() — Breaks on Re-Run", ha="center", va="center", fontsize=12.5, fontweight="bold", color="#B91C1C")
    ax.text(3.0, 2.35, "Run 1: Writes doc_chunk_0 -> OK\n\nEdit knowledge_base/ -> Re-run ingest.py\n\nRun 2: Duplicate ID warning / stale text kept!",
            ha="center", va="center", fontsize=10.5, color=SLATE_DARK, linespacing=1.45)

    rbox(ax, 6.3, 0.3, 5.4, 4.2, edge=GREEN, bg="#FFFFFF", lw=1.8)
    ax.text(9.0, 4.05, "collection.upsert() — Idempotent", ha="center", va="center", fontsize=12.5, fontweight="bold", color=GREEN)
    ax.text(9.0, 2.35, "Run 1: Inserts doc_chunk_0 -> OK\n\nEdit knowledge_base/ -> Re-run ingest.py\n\nRun 2: Cleanly updates vector & metadata!",
            ha="center", va="center", fontsize=10.5, color=SLATE_DARK, linespacing=1.45)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_upsert_vs_add.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_16_topk_distance_curve():
    fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ks = np.array([1, 2, 3, 5, 8, 10])
    recall = np.array([0.62, 0.81, 0.92, 0.95, 0.96, 0.96])
    noise = np.array([0.05, 0.08, 0.12, 0.28, 0.55, 0.72])
    ax.plot(ks, recall, marker="o", lw=2.6, color=BLUE, label="Answer Recall")
    ax.plot(ks, noise, marker="s", lw=2.6, color=ORANGE, label="Prompt Noise Risk")
    ax.axvspan(2.6, 3.4, color="#EFF6FF", alpha=0.8)
    ax.text(3.0, 0.50, "Sweet Spot\ntop_k = 3\nmax_dist <= 1.15", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color=BLUE, bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFFFF", edgecolor=BLUE))
    ax.set_xlabel("top_k Chunks Injected", fontsize=10, fontweight="bold", color=SLATE_MED)
    ax.set_ylabel("Normalized Score (0 - 1)", fontsize=10, fontweight="bold", color=SLATE_MED)
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle="--", alpha=0.45, color=BORDER)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor=BORDER, fontsize=9)
    fig.savefig(os.path.join(OUTPUT_DIR, "visual_topk_distance_curve.png"), dpi=300, bbox_inches="tight", pad_inches=0.06, facecolor="#FFFFFF")
    plt.close(fig)


def make_17_tool_handshake():
    fig, ax = plt.subplots(figsize=(11.4, 4.6), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    cols = [(2.0, "Groq Llama 3.3", BLUE), (6.0, "Python Dispatcher", ORANGE), (10.0, "Local Tool", GREEN)]
    for cx, label, ec in cols:
        rbox(ax, cx - 1.35, 3.85, 2.7, 0.65, edge=ec, bg="#FFFFFF", lw=1.8)
        ax.text(cx, 4.175, label, ha="center", va="center", fontsize=10.5, fontweight="bold", color=ec)
        ax.plot([cx, cx], [0.4, 3.85], linestyle="--", color=BORDER, lw=1.4)

    msgs = [
        (2.0, 6.0, 3.15, "1. assistant.tool_calls [id='call_9f2a']", BLUE),
        (6.0, 10.0, 2.35, "2. read_file(filepath='data/log.json')", ORANGE),
        (10.0, 6.0, 1.55, "3. 'Error: not found, try data/sensor_logs.csv'", GREEN),
        (6.0, 2.0, 0.75, "4. role='tool', tool_call_id='call_9f2a'", BLUE),
    ]
    for x1, x2, y, txt, col in msgs:
        arrow(ax, x1, y, x2, y, color=col, lw=2.2)
        ax.text((x1 + x2) / 2, y + 0.25, txt, ha="center", va="center", fontsize=9.3, fontweight="bold",
                color=col, bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=BORDER))

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_tool_handshake.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_18_memory_hygiene():
    fig, ax = plt.subplots(figsize=(11.4, 4.6), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.8)
    ax.axis("off")

    rbox(ax, 0.3, 0.35, 5.4, 4.1, edge=GREEN, bg="#FFFFFF", lw=1.8)
    ax.text(3.0, 4.0, "DO: Actionable 1-Sentence Lesson", ha="center", va="center", fontsize=12, fontweight="bold", color=GREEN)
    ax.text(3.0, 2.25, "[category: 'aar_lesson']\n\n'When root CSV fails in IoT tasks,\ninspect data/ before retrying.'\n\nHigh cosine signal -> Clean recall!",
            ha="center", va="center", fontsize=10.5, color=SLATE_DARK, linespacing=1.45)

    rbox(ax, 6.3, 0.35, 5.4, 4.1, edge="#B91C1C", bg="#FFFFFF", lw=1.8)
    ax.text(9.0, 4.0, "DON'T: Raw Log Pollution", ha="center", va="center", fontsize=12, fontweight="bold", color="#B91C1C")
    ax.text(9.0, 2.25, "[500 lines of raw CSV numbers +]\n['Run started OK at 14:02:11...']\n\nDilutes 384-dim embeddings ->\nBuries real fixes in noise!",
            ha="center", va="center", fontsize=10.5, color=SLATE_DARK, linespacing=1.45)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_memory_hygiene.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_19_trace_anatomy():
    fig, ax = plt.subplots(figsize=(11.4, 4.4), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    rbox(ax, 0.3, 1.5, 11.4, 2.6, edge=SLATE_DARK, bg="#0B1220", lw=1.8)
    line = '{"step": 3, "tool": "read_file", "args": {"filepath": "data/sensor_logs.csv"}, "status": "recovered", "elapsed_ms": 14.2}'
    ax.text(6.0, 2.8, line, ha="center", va="center", fontsize=9.8, fontweight="bold", color="#4ADE80", fontfamily="DejaVu Sans Mono")

    tags = [
        (1.4, "Dynamic Loop Step\n(proves non-hardcoded)", BLUE),
        (4.1, "Tool + Validated Args\n(JSON schema audit)", ORANGE),
        (7.5, "Recovery Status\n(Self-heal evidence)", GREEN),
        (10.4, "Latency ms\n(Local timing)", BLUE),
    ]
    for tx, lbl, ec in tags:
        rbox(ax, tx - 1.15, 0.2, 2.3, 0.95, edge=ec, bg="#FFFFFF", lw=1.5)
        ax.text(tx, 0.675, lbl, ha="center", va="center", fontsize=8.5, fontweight="bold", color=ec, linespacing=1.35)
        arrow(ax, tx, 1.18, tx, 1.48, color=ec, lw=1.6)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_trace_anatomy.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_20_fault_matrix():
    fig, ax = plt.subplots(figsize=(11.6, 5.0), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    items = [
        (0.25, 2.75, "Fault 1: Missing File Path", "Typo 'log_v2.json' -> Tool hints data/ -> Recovers", BLUE),
        (6.15, 2.75, "Fault 2: Corrupt / NaN Field", "Bad CSV/JSON row flagged safely without ValueError", ORANGE),
        (0.25, 0.25, "Fault 3: Cold Memory Restart", "Fresh process recalls Run 1 AAR rule on Step 1", GREEN),
        (6.15, 0.25, "Fault 4: Impossible Goal Cap", "Exits cleanly at MAX_ITERATIONS=10; zero hang", "#B91C1C"),
    ]
    for x, y, title, body, ec in items:
        rbox(ax, x, y, 5.6, 2.2, edge=ec, bg="#FFFFFF", lw=1.8)
        ax.text(x + 0.35, y + 1.55, title, ha="left", va="center", fontsize=12.5, fontweight="bold", color=ec)
        ax.text(x + 0.35, y + 0.78, body, ha="left", va="center", fontsize=10.8, color=SLATE_DARK)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_fault_matrix.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_21_5day_journey():
    fig, ax = plt.subplots(figsize=(11.8, 3.8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 4.0)
    ax.axis("off")

    days = [
        ("DAY 1", "Setup & Vectors", "Python 3.13 + uv\nGroq Key + ChromaDB", BLUE),
        ("DAY 2", "Vector RAG", "ingest.py + query.py\nGrounded Citations", BLUE),
        ("DAY 3", "ReAct + Memory", "While-Loop + Tools\nSelf-Heal + AAR", ORANGE),
        ("DAY 4", "Capstone Build", "Unassisted Sprint\n4 Tools + Trace", ORANGE),
        ("DAY 5", "Live Defense", "Fault Injection Tests\nViva Evaluation", GREEN),
    ]
    w, gap, x0 = 2.15, 0.3, 0.22
    for i, (d, title, body, ec) in enumerate(days):
        x = x0 + i * (w + gap)
        rbox(ax, x, 0.45, w, 3.0, edge=ec, bg="#FFFFFF", lw=1.8)
        rbox(ax, x, 2.85, w, 0.60, edge=ec, bg=ec, lw=1.0, pad=0.02)
        ax.text(x + w / 2, 3.15, d, ha="center", va="center", fontsize=10.5, fontweight="bold", color="#FFFFFF")
        ax.text(x + w / 2, 2.25, title, ha="center", va="center", fontsize=10.5, fontweight="bold", color=SLATE_DARK)
        ax.text(x + w / 2, 1.25, body, ha="center", va="center", fontsize=8.8, color=SLATE_MED, linespacing=1.45)
        if i < len(days) - 1:
            arrow(ax, x + w + 0.03, 1.95, x + w + gap - 0.03, 1.95, color=ec, lw=1.8)

    fig.savefig(os.path.join(OUTPUT_DIR, "visual_5day_journey.png"), dpi=300, bbox_inches="tight", pad_inches=0.05, facecolor="#FFFFFF")
    plt.close(fig)


def make_22_extra_terminal_outputs():
    """Generate 7 exact terminal output cards mapped to Day 1-5 command slides."""
    specs = [
        (
            "output_day1_uv_sync.png",
            "Windows PowerShell — uv sync (pyproject.toml)",
            [
                ("PS C:\\Users\\student\\agentic-ai-vap> uv sync", "#38BDF8"),
                ("Using CPython 3.13.2", "#94A3B8"),
                ("Creating virtual environment at: .venv", "#E2E8F0"),
                ("Resolved 62 packages in 420ms", "#94A3B8"),
                ("Installed 62 packages in 1.84s", "#4ADE80"),
                (" + chromadb==1.0.7  + python-dotenv==1.0.1", "#CBD5E1"),
                (" + pytest==8.3.4    + qrcode==8.0", "#CBD5E1"),
                ("PS C:\\Users\\student\\agentic-ai-vap> uv run python --version", "#38BDF8"),
                ("Python 3.13.2", "#4ADE80"),
            ],
        ),
        (
            "output_day1_chroma_demo.png",
            "Windows PowerShell — uv run python chroma_demo.py",
            [
                ("PS C:\\Users\\student\\agentic-ai-vap> uv run python chroma_demo.py", "#38BDF8"),
                ("Query: 'How does a transistor work?'", "#FBBF24"),
                ("  dist=1.323 | The MOSFET gate voltage controls the channel drain current.", "#4ADE80"),
                ("  dist=1.534 | A capacitor stores electrostatic energy inside an electric field.", "#E2E8F0"),
                ("  dist=1.938 | Python uses indentation cleanly to delimit code blocks.", "#94A3B8"),
                ("# Top-1 matched MOSFET even though 'transistor' never appears in doc1.", "#A7F3D0"),
            ],
        ),
        (
            "output_day2_ingest_run.png",
            "Windows PowerShell — Idempotent ingest.py Check",
            [
                ("PS C:\\Users\\student\\vap-day2> uv run python ingest.py", "#38BDF8"),
                ("Ingestion complete. Collection 'ece_knowledge' now holds 12 chunks.", "#4ADE80"),
                ("PS C:\\Users\\student\\vap-day2> uv run python ingest.py", "#38BDF8"),
                ("Ingestion complete. Collection 'ece_knowledge' now holds 12 chunks.", "#4ADE80"),
                ("# Run 1 count == Run 2 count -> fixed IDs + upsert() verified!", "#A7F3D0"),
            ],
        ),
        (
            "output_day2_query_run.png",
            "Windows PowerShell — Cited Query Output (query.py)",
            [
                ("PS C:\\Users\\student\\vap-day2> uv run python query.py \"What is max Vds of IRF540N?\"", "#38BDF8"),
                ("Retrieved 2 chunks:", "#94A3B8"),
                (" - [irf540n_mosfet.md] dist=0.7241", "#4ADE80"),
                (" - [lorawan_bms_notes.md] dist=1.4812", "#CBD5E1"),
                ("", "#E2E8F0"),
                ("Grounded Answer (from [irf540n_mosfet.md], dist=0.7241):", "#FBBF24"),
                ("Absolute Maximum Drain-Source Voltage (Vds): 100 V [irf540n_mosfet.md].", "#4ADE80"),
            ],
        ),
        (
            "output_day3_agent_run.png",
            "Windows PowerShell — agent.py / demo_cross_session.py --mock-llm",
            [
                ("PS C:\\Users\\student\\vap-day3> uv run python demo_cross_session.py --mock-llm", "#38BDF8"),
                ("Run 1 (Cold Start): 4 steps | Recalled: 0 | AAR: Inspect 'data/iot_sensor_log.json'...", "#FBBF24"),
                ("  [Step 1] read_file('sensor.csv') -> error (FileNotFoundError)", "#F87171"),
                ("  [Step 2] list_dir('data') -> ok -> ['iot_sensor_log.json']", "#CBD5E1"),
                ("  [Step 3] read_file('data/iot_sensor_log.json') -> recovered", "#4ADE80"),
                ("  [Step 4] write_report('out/audit_report.md') -> ok", "#4ADE80"),
                ("Run 2 (Warm Recall): 2 steps | Recalled: 1 | AAR: Inspect 'data/iot_sensor_log.json'...", "#4ADE80"),
            ],
        ),
        (
            "output_day4_trace_cat.png",
            "Windows PowerShell — trace.jsonl Step Log Schema",
            [
                ("PS C:\\Users\\student\\vap-day4> Get-Content capstone_3_research\\trace.jsonl", "#38BDF8"),
                ("{\"step\": 1, \"tool\": \"read_papers\", \"status\": \"error\", \"elapsed_ms\": 1.8}", "#F87171"),
                ("{\"step\": 2, \"tool\": \"list_dir\", \"args\": {\"directory\": \"data\"}, \"status\": \"recovered\"}", "#FBBF24"),
                ("{\"step\": 3, \"tool\": \"read_papers\", \"args\": {\"filepath\": \"data/paper_abstracts.json\"}, \"status\": \"recovered\"}", "#4ADE80"),
                ("{\"step\": 4, \"tool\": \"query_standards\", \"status\": \"recovered\", \"elapsed_ms\": 6.4}", "#E2E8F0"),
                ("{\"step\": 5, \"tool\": \"write_report\", \"status\": \"recovered\", \"elapsed_ms\": 2.1}", "#4ADE80"),
            ],
        ),
        (
            "output_day5_grader_cli.png",
            "Windows PowerShell — Automated Evaluator CLI Score",
            [
                ("PS C:\\Users\\student\\auto-evaluator> uv run python -m evaluator.cli evaluate ./sub_01", "#38BDF8"),
                ("{", "#E2E8F0"),
                ("  \"rag_pipeline\": 25,", "#4ADE80"),
                ("  \"react_loop\": 20,", "#4ADE80"),
                ("  \"fault_recovery\": 25,", "#4ADE80"),
                ("  \"episodic_memory\": 20,", "#4ADE80"),
                ("  \"hygiene_and_docs\": 10,", "#4ADE80"),
                ("  \"total\": 100,  \"grade\": \"A+\"", "#FBBF24"),
                ("}", "#E2E8F0"),
            ],
        ),
    ]
    for fname, title, lines in specs:
        render_terminal_card(fname, title, lines, figsize=(11.4, 4.7), font_size=8.4)


def main():
    make_1_env_setup_pipeline()
    make_2_cosine_similarity_2d()
    make_3_chunking_sliding_window()
    make_4_day1_terminal()
    make_5_project1_folder_tree()
    make_6_day2_rag_tests()
    make_7_dual_memory_architecture()
    make_8_day3_react_trace()
    make_9_capstone_3_tracks()
    make_10_day4_smoke_test()
    make_11_grading_rubric_chart()
    make_12_day5_defense_outputs()
    make_13_ground_rules()
    make_14_failure_modes_2x2()
    make_15_upsert_vs_add()
    make_16_topk_distance_curve()
    make_17_tool_handshake()
    make_18_memory_hygiene()
    make_19_trace_anatomy()
    make_20_fault_matrix()
    make_21_5day_journey()
    make_22_extra_terminal_outputs()
    files = sorted(os.listdir(OUTPUT_DIR))
    print(f"Generated {len(files)} PPT visual files in {OUTPUT_DIR}:")
    for f in files:
        print(" -", f)


if __name__ == "__main__":
    main()
