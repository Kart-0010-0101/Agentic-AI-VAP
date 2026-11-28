"""
build_instructor_prep_pdfs.py
Generates 5 standalone A4 Instructor Preparation PDFs (one per workshop day) in:
    C:\\Users\\lapto\\Desktop\\demo\\BEN\\VAP\\instructor_guides\\

Reuses typography, tables, callouts, and numbered A4 canvas from
build_comprehensive_a4_vap_pdfs.py, with dark (#0B1220) slide-matched code boxes.
"""

from __future__ import annotations

import io
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image as PILImage

VAP_DIR = Path(r"C:\Users\lapto\Desktop\demo\BEN\VAP")
OUT_DIR = VAP_DIR / "instructor_guides"
OUT_DIR.mkdir(parents=True, exist_ok=True)
if str(VAP_DIR) not in sys.path:
    sys.path.insert(0, str(VAP_DIR))

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from build_comprehensive_a4_vap_pdfs import (
    CONTENT_W,
    add_chapter_header,
    get_a4_canvas_class,
    make_callout,
    make_table,
    setup_styles,
)


def make_formula_box(latex_str: str, styles, width: float = CONTENT_W):
    """Render publication-grade math notation (superscripts, fractions, roots) via matplotlib mathtext."""
    dpi = 300
    fig = plt.figure(figsize=(8.0, 0.9), dpi=dpi)
    fig.patch.set_facecolor("#EFF6FF")
    fig.text(0.5, 0.5, latex_str, fontsize=13.5, ha="center", va="center", color="#0F172A")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight", pad_inches=0.05, facecolor="#EFF6FF")
    plt.close(fig)
    buf.seek(0)
    with PILImage.open(buf) as im:
        px_w, px_h = im.size
    buf.seek(0)
    scale = min(72.0 / dpi * 0.88, (width - 24.0) / px_w)
    img = Image(buf, width=px_w * scale, height=px_h * scale)
    img.hAlign = "LEFT"

    c_title = ParagraphStyle("CT_FORMULA", parent=styles["CalloutTitle"], textColor=colors.HexColor("#1E3A8A"))
    t = Table([[Paragraph("KEY FORMULA", c_title)], [img]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
        ("LINELEFT", (0, 0), (-1, -1), 3.5, colors.HexColor("#1E3A8A")),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
        ("TOPPADDING", (0, 1), (-1, 1), 2),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def make_dark_code_box(title: str, lines: list[str], styles, width: float = CONTENT_W):
    """Splittable dark (#0B1220) code block matching slide deck aesthetics."""
    hdr_style = ParagraphStyle(
        "DarkCodeHdr", parent=styles["CodeTitle"], textColor=colors.HexColor("#EA580C")
    )
    line_style = ParagraphStyle(
        "DarkCodeLine", parent=styles["CodeLine"], fontSize=8.3, leading=11.5,
        textColor=colors.HexColor("#E2E8F0"),
    )
    rows = []
    if title:
        rows.append([Paragraph(f"<b>{title}</b>", hdr_style)])
    for ln in lines:
        esc = ln.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;")
        rows.append([Paragraph(esc or "&nbsp;", line_style)])

    t = Table(rows, colWidths=[width], repeatRows=1 if title else 0)
    ts = [
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0B1220")),
        ("LINEBEFORE", (0, 0), (0, -1), 3.0, colors.HexColor("#EA580C")),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#334155")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 1.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.0),
    ]
    if title:
        ts.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
            ("TOPPADDING", (0, 0), (-1, 0), 5),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
            ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#334155")),
        ])
        if len(rows) > 1:
            ts.append(("TOPPADDING", (0, 1), (-1, 1), 6))
    else:
        ts.append(("TOPPADDING", (0, 0), (-1, 0), 6))
    ts.append(("BOTTOMPADDING", (0, -1), (-1, -1), 6))
    t.setStyle(TableStyle(ts))
    return t


def build_instructor_cover(story, day_num: int, title: str, subtitle: str, total_slides: int, styles):
    bar = Table([["", ""]], colWidths=[125, CONTENT_W - 125])
    bar.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (0, 0), 5.0, colors.HexColor("#EA580C")),
        ("LINEBELOW", (1, 0), (1, 0), 5.0, colors.HexColor("#1E3A8A")),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    warn_style = ParagraphStyle(
        "WarnBanner", parent=styles["CoverYear"], fontSize=10,
        textColor=colors.HexColor("#B91C1C"), alignment=TA_CENTER,
    )
    meta_style = ParagraphStyle(
        "CoverMeta", parent=styles["Body"], alignment=TA_CENTER,
        fontSize=10.5, textColor=colors.HexColor("#334155"),
    )

    story.append(Spacer(1, 24))
    story.append(bar)
    story.append(Spacer(1, 36))
    story.append(Paragraph(f"AGENTIC AI VAP  |  DAY {day_num} INSTRUCTOR GUIDE", styles["CoverProgram"]))
    story.append(Paragraph(title, styles["CoverTitle"]))
    story.append(Paragraph(subtitle, styles["CoverSubtitle"]))
    story.append(Spacer(1, 20))
    story.append(make_callout(
        "CONFIDENTIALITY NOTICE",
        "INSTRUCTOR ONLY — NOT FOR STUDENT DISTRIBUTION. Contains grading answer keys, live demo scripts, "
        "viva rubrics, and unseen fault datasets.",
        styles, border_color="#B91C1C", bg_color="#FEF2F2",
    ))
    story.append(Spacer(1, 28))
    story.append(Paragraph(
        f"<b>Deck Size:</b> {total_slides} Slides  |  <b>Session Date:</b> __________________  |  <b>Batch:</b> ECE 5th Sem",
        meta_style,
    ))
    story.append(Spacer(1, 90))
    story.append(HRFlowable(width="55%", thickness=1.2, color=colors.HexColor("#CBD5E1"), hAlign="CENTER", spaceAfter=16))
    story.append(Paragraph("Department of Electronics and Communication Engineering", styles["CoverDept"]))
    story.append(Paragraph("Acharya Institute of Technology, Bengaluru", styles["CoverCollege"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("INSTRUCTOR PREPARATION GUIDE — NOT FOR STUDENT DISTRIBUTION", warn_style))
    story.append(PageBreak())


def render_day_pdf(spec: dict) -> Path:
    day = spec["day"]
    out_path = OUT_DIR / f"Instructor_Day{day}_Prep.pdf"
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=54, rightMargin=54, topMargin=56, bottomMargin=54,
    )
    styles = setup_styles()
    story = []

    build_instructor_cover(
        story, day, spec["cover_title"], spec["cover_sub"], spec["slide_count"], styles
    )

    # 1. Timeline + Pre-session checklist
    add_chapter_header(story, f"Day {day}  |  Section 1", "Session Timeline & Pre-Session Checklist", styles)
    story.append(make_table(
        ["Time", "Dur.", "Slides", "Activity", "Instructor Action"],
        spec["timeline"],
        [66, 36, 48, 128, CONTENT_W - 278],
        styles,
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Pre-Session Verification Checklist", styles["H2"]))
    story.append(make_dark_code_box(f"VERIFY BEFORE 09:00 AM — DAY {day}", spec["checklist"], styles))

    # 2. Core Theoretical Knowledge (Instructor Study Primer)
    if spec.get("theory"):
        story.append(PageBreak())
        add_chapter_header(
            story, f"Day {day}  |  Section 2",
            "Core Theoretical Knowledge (Instructor Study Primer)", styles,
        )
        for topic in spec["theory"]:
            story.append(Paragraph(topic["title"], styles["H2"]))
            story.append(Paragraph(topic["summary"], styles["Body"]))
            for pt in topic["points"]:
                story.append(Paragraph(f"&bull;&nbsp;&nbsp;{pt}", styles["Bullet"]))
            if topic.get("formula"):
                fm = topic["formula"]
                story.append(Spacer(1, 3))
                if fm.get("latex"):
                    story.append(make_formula_box(fm["latex"], styles))
                else:
                    story.append(make_callout(
                        "KEY FORMULA", f"<b>{fm['expr']}</b>",
                        styles, border_color="#1E3A8A", bg_color="#EFF6FF",
                    ))
                if fm.get("terms"):
                    story.append(Spacer(1, 4))
                    story.append(make_table(
                        ["Term / Symbol", "Meaning &amp; Physical / System Role"],
                        fm["terms"],
                        [125, CONTENT_W - 125],
                        styles, header_bg="#334155",
                    ))
                if fm.get("example"):
                    story.append(Spacer(1, 4))
                    story.append(make_callout(
                        "WORKED EXAMPLE / WHITEBOARD NOTE", fm["example"],
                        styles, border_color="#15803D", bg_color="#F0FDF4",
                    ))
            elif topic.get("formula_or_note"):
                story.append(Spacer(1, 3))
                story.append(make_callout(
                    "TEACHING KEY / FORMULA", topic["formula_or_note"],
                    styles, border_color="#1E3A8A", bg_color="#EFF6FF",
                ))
            story.append(Spacer(1, 6))

    # 3. Talking Points
    story.append(PageBreak())
    add_chapter_header(story, f"Day {day}  |  Section 3", "Slide-by-Slide Talking Points", styles)
    story.append(make_table(
        ["Slide / Topic", "Say This", "Do Not Say"],
        spec["talking_points"],
        [96, 200, CONTENT_W - 296],
        styles,
    ))

    # 4. Live Demo Scripts
    story.append(PageBreak())
    add_chapter_header(story, f"Day {day}  |  Section 4", "Live Demo Scripts & Expected Output", styles)
    for d_title, priority, cmd_lines in spec["demos"]:
        story.append(Paragraph(f"{d_title} [{priority}]", styles["H3"]))
        story.append(make_dark_code_box(d_title, cmd_lines, styles))
        story.append(Spacer(1, 8))

    # 5. FAQs & Mistakes
    add_chapter_header(story, f"Day {day}  |  Section 5", "Expected Student Questions & Common Mistakes", styles)
    story.append(make_table(
        ["#", "Student Question", "Concise Answer"],
        spec["faqs"],
        [24, 155, CONTENT_W - 179],
        styles,
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Common Mistakes & Live Fixes", styles["H2"]))
    story.append(make_table(
        ["#", "Symptom", "Root Cause", "Exact Live Fix"],
        spec["mistakes"],
        [24, 125, 130, CONTENT_W - 279],
        styles, header_bg="#B91C1C",
    ))

    # 6. Skip list + Answer Key
    story.append(Spacer(1, 14))
    add_chapter_header(story, f"Day {day}  |  Section 6", "Pacing Skip List & Answer Key", styles)
    story.append(make_table(
        ["Priority", "Slide(s) to Cut", "Justification"],
        spec["skip_list"],
        [75, 165, CONTENT_W - 240],
        styles, header_bg="#EA580C",
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(spec["answer_key_title"], styles["H2"]))
    story.append(make_table(
        spec["answer_key_headers"],
        spec["answer_key_rows"],
        spec["answer_key_widths"],
        styles, header_bg="#15803D",
    ))

    # 6. Optional Day-specific sections (Day 4 Track Cheat Sheets, Day 5 Batch B / Rubric / Viva)
    for extra in spec.get("extras", []):
        story.append(PageBreak())
        add_chapter_header(story, f"Day {day}  |  Reference", extra["heading"], styles)
        if extra.get("callout"):
            title_c, body_c, col_c, bg_c = extra["callout"]
            story.append(make_callout(title_c, body_c, styles, border_color=col_c, bg_color=bg_c))
            story.append(Spacer(1, 8))
        for block in extra["blocks"]:
            kind = block["type"]
            if kind == "h2":
                story.append(Paragraph(block["text"], styles["H2"]))
            elif kind == "table":
                story.append(make_table(
                    block["headers"], block["rows"], block["widths"], styles,
                    header_bg=block.get("bg", "#1E3A8A"),
                ))
                story.append(Spacer(1, 8))
            elif kind == "code":
                story.append(make_dark_code_box(block["title"], block["lines"], styles))
                story.append(Spacer(1, 8))
            elif kind == "bullets":
                for b in block["items"]:
                    story.append(Paragraph(f"&bull;&nbsp;&nbsp;{b}", styles["Bullet"]))
                story.append(Spacer(1, 6))

    # 7. Next-Day Bridge
    story.append(Spacer(1, 12))
    story.append(make_callout(
        spec["bridge_title"], spec["bridge_text"], styles, border_color="#1E3A8A", bg_color="#EFF6FF"
    ))

    canvas_cls = get_a4_canvas_class(
        f"DAY {day} INSTRUCTOR PREP GUIDE",
        "INSTRUCTOR ONLY — NOT FOR STUDENT DISTRIBUTION",
    )
    doc.build(story, canvasmaker=canvas_cls)
    return out_path


DAY_SPECS = [
    # ------------------------------------------------------------------ DAY 1
    {
        "day": 1,
        "slide_count": 51,
        "cover_title": "Day 1: Orientation, Setup,<br/>RAG Intro &amp; Vectors",
        "cover_sub": "Instructor Session Plan, Poll Operation, Live Labs &amp; Setup Triage",
        "timeline": [
            ["09:00-09:20", "20m", "1-5", "Cover, AI timeline & 3 live polls", "Open /poll (ECEKART/WasteOfTimeGG). Wait for 60%+ phone votes."],
            ["09:20-10:05", "45m", "6-14", "Rules, Friday goal, LLM internals, ReAct video", "Play anim_closed_loop (S14). Pause for 1 question."],
            ["10:05-11:00", "55m", "15-19", "What is RAG, Keyword vs Vector, RAG video", "Play anim_rag_pipeline (S17). Show hallucination slide (S19)."],
            ["11:00-11:30", "30m", "20", "Morning Tea Break", "Keep QR poll summary visible if students ask."],
            ["11:30-12:35", "65m", "21-28", "384-D vectors, cosine math, 3D video, HNSW", "Play anim_cosine_search (S26). Compare exact vs ANN."],
            ["12:35-13:00", "25m", "29", "7-Step Windows setup flow", "Remind batch: complete any missing setup during lunch before 2 PM."],
            ["13:00-14:00", "60m", "30", "Lunch Break", "Walk room and unblock Python/uv/Groq installs."],
            ["14:00-14:45", "45m", "31-38", "uv, .env, pyproject.toml, verify.py demo", "Run uv sync + verify.py live on projector."],
            ["14:45-15:30", "45m", "39-43", "chroma_demo.py lab + live ECE drill", "Run chroma_demo.py; students add 2 ECE notes (S43)."],
            ["15:30-15:40", "10m", "44", "Afternoon Break", "Confirm lagging students finished verify.py."],
            ["15:40-16:45", "65m", "45-51", "Search compare, fixes, Git, exit check", "Confirm 5+ students pass verify.py and chroma_demo.py."],
        ],
        "checklist": [
            "[ ] Projector set to 16:9 native 1920x1080 or 1280x720 (avoid 4:3 crop)",
            "[ ] https://agentic-ai-vap.onrender.com/poll loads with ECEKART / WasteOfTimeGG",
            "[ ] https://agentic-ai-vap.onrender.com/vote loads with ECE / december30",
            "[ ] Campus Wi-Fi verified (> 5 Mbps) + personal 4G/5G hotspot on standby",
            "[ ] Day 1 branch checked out: uv sync clean, verify.py replies, chroma_demo.py runs",
            "[ ] USB drive carries offline Python 3.13 installer + uv binary",
            "[ ] Open PPTX in Microsoft PowerPoint desktop (NOT Google Slides — videos won't play)",
        ],
        "theory": [
            {
                "title": "1. Autoregressive LLMs, Self-Attention &amp; Why Hallucinations Happen",
                "summary": (
                    "A Large Language Model is a stateless next-token predictor built on the Transformer decoder "
                    "architecture (Vaswani et al., 2017). It computes probability distributions over vocabulary tokens "
                    "using stacked causal self-attention and feed-forward MLP layers — not a structured fact table."
                ),
                "points": [
                    "<b>Autoregressive Generation:</b> Given prompt tokens x<sub>1</sub>..x<sub>t</sub>, the model outputs logits across ~32K-128K vocabulary items, samples x<sub>t+1</sub>, appends it to the context window, and repeats token by token.",
                    "<b>Sub-Word Tokenization (~1.3 tokens/word):</b> Technical identifiers split unevenly ('IRF540N' becomes 3-4 sub-word tokens). Context window limits apply to total tokens (input prompt + retrieved chunks + generated reply).",
                    "<b>Why Hallucinations Happen:</b> Training minimizes cross-entropy prediction loss over internet text, not factual verification. When a query asks for an unseen voltage rating or IEEE citation, attention interpolates statistically plausible patterns and invents confident-sounding falsehoods.",
                ],
                "formula": {
                    "latex": r"$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$",
                    "expr": "Attention(Q, K, V) = softmax((Q K<sup>T</sup>) / sqrt(d<sub>k</sub>)) V",
                    "terms": [
                        ["Q (Query matrix)", "Vectors encoding what each current token is searching for in prior context."],
                        ["K (Key matrix)", "Vectors advertising what information each earlier token contains."],
                        ["K<sup>T</sup> (Transpose of K)", "Aligns dimensions so Q · K<sup>T</sup> computes pairwise dot-product affinity scores."],
                        ["d<sub>k</sub> (Key dimension)", "Width of each attention head (e.g., 64 or 128 floats per head)."],
                        ["1 / &radic;d<sub>k</sub> (Scaling)", "Prevents large dot products from pushing softmax into tiny-gradient saturation."],
                        ["softmax(...)", "Normalizes alignment scores across prior tokens into positive weights summing to 1.0."],
                        ["V (Value matrix)", "Actual token representations weighted and summed to form the layer output."],
                    ],
                    "example": (
                        "Whiteboard check: Explain that attention blends weighted information strictly from tokens inside "
                        "the current prompt window. If verified specs are absent from the prompt, Q has nothing factual in K/V to attend to."
                    ),
                },
            },
            {
                "title": "2. Control Theory Analogy: Open-Loop Scripts vs. Closed-Loop ReAct",
                "summary": (
                    "Fifth-semester ECE students already study feedback control. Framing ReAct agents as discrete-time "
                    "closed-loop controllers strips away AI buzzwords and highlights why error handling determines reliability."
                ),
                "points": [
                    "<b>Open-Loop Failure Mode:</b> A single prompt or linear script behaves like open-loop PWM driving a DC motor with no encoder. Any disturbance (renamed file, schema change, missing folder) stalls execution with zero recovery.",
                    "<b>Closed-Loop Mapping:</b> LLM Planner = Controller, Python tool = Actuator, file/API output = Sensor, and Goal Verification = Comparator. Observations stay in context so each iteration corrects the trajectory.",
                    "<b>Bounded Stability (max_steps=10):</b> Just as physical systems need saturation limits and watchdogs, an explicit loop counter prevents runaway API cost when a goal is unsolvable.",
                ],
                "formula": {
                    "latex": r"$e(t) = r(t) - y(t) \;\Rightarrow\; \Delta_t = \mathrm{Goal} - \mathrm{Observation}_t \quad (t \leq \mathrm{max\_steps})$",
                    "expr": "e(t) = r(t) - y(t)   =&gt;   Delta<sub>t</sub> = Goal - Observation<sub>t</sub>  (t &lt;= max_steps)",
                    "terms": [
                        ["r(t) / Goal", "Desired target state (reference setpoint or user engineering task)."],
                        ["y(t) / Observation<sub>t</sub>", "Measured state returned after tool execution at discrete step t."],
                        ["e(t) / Delta<sub>t</sub>", "Remaining discrepancy driving the controller/LLM's next action u(t)."],
                        ["max_steps (e.g. 10)", "Hard discrete iteration cap acting as a stability watchdog."],
                    ],
                    "example": (
                        "Classroom contrast: Linear pipeline u<sub>1</sub> -&gt; u<sub>2</sub> -&gt; u<sub>3</sub> crashes at step 1 on FileNotFoundError; "
                        "closed-loop agent sees e<sub>1</sub> = missing file + hints=['data/'], emits u<sub>2</sub> = list_dir('data'), and converges."
                    ),
                },
            },
            {
                "title": "3. Keyword Search (Ctrl+F / BM25) vs. Dense Vector RAG",
                "summary": (
                    "Before morning break you introduce RAG conceptually; after break you replace brittle keyword matching "
                    "with dense neural sentence embeddings running completely on CPU."
                ),
                "points": [
                    "<b>Lexical Mismatch Problem:</b> Exact string search and TF-IDF match exact character forms. Querying 'transistor heat limit' fails completely against a datasheet stating 'MOSFET T<sub>j</sub> max = 175 °C'.",
                    "<b>Dense Bi-Encoder (all-MiniLM-L6-v2):</b> ChromaDB embeds queries and text chunks into a shared 384-dimensional vector space using a 22M-parameter Transformer trained via contrastive learning so paraphrases land nearby.",
                    "<b>Zero-GPU Deployment Math:</b> Model size is ~90 MB quantized ONNX (~5-20 ms per query on laptop CPUs). No VRAM, PyTorch GPU drivers, or external vector cloud accounts are required.",
                ],
                "formula": {
                    "latex": r"$\mathrm{RAM}_{\mathrm{vectors}} = N \times d \times 4\ \mathrm{bytes} \qquad (d = 384)$",
                    "expr": "RAM<sub>vectors</sub> = N &times; d &times; 4 bytes   |   ChromaDB CPU default: d = 384",
                    "terms": [
                        ["N", "Number of indexed text chunks stored in the ChromaDB collection."],
                        ["d", "Embedding vector dimensionality (384 floats for all-MiniLM-L6-v2)."],
                        ["4 bytes (float32)", "Storage size per standard IEEE-754 single-precision coordinate."],
                    ],
                    "example": (
                        "Worked capacity calculation: 10,000 ECE datasheet chunks &times; 384 dims &times; 4 bytes = 15,360,000 bytes (~14.6 MB RAM), "
                        "versus ~58.6 MB for 1536-D cloud embeddings — easily fitting in any student laptop."
                    ),
                },
            },
            {
                "title": "4. Cosine Similarity, Euclidean L2 Distance &amp; HNSW Indexing",
                "summary": (
                    "Students frequently ask why Chroma returns distance numbers like 1.323 instead of 0-100% percentages "
                    "and how search remains sub-10ms as collections grow."
                ),
                "points": [
                    "<b>Direction Over Magnitude:</b> Two sentences sharing topic meaning point in similar directions regardless of length. Normalized dot product yields cos(theta) in [-1, 1].",
                    "<b>Chroma Default Metric (Squared L2):</b> On unit-length vectors (||A|| = ||B|| = 1), squared Euclidean distance simplifies cleanly to d<sub>L2</sub><sup>2</sup> = 2(1 - cos(theta)), explaining why smaller distance means tighter semantic alignment.",
                    "<b>HNSW Hierarchical Skip Graphs:</b> Upper layers hold sparse long-range hub links (coarse jumps); lower layer L0 holds dense local neighbors (fine convergence), cutting complexity from O(N) brute-force to O(log N) at ~99.5% recall.",
                ],
                "formula": {
                    "latex": r"$\cos(\theta) = \frac{A \cdot B}{\|A\|\,\|B\|} \qquad\quad d_{L2}^2(A, B) = \sum_{i=1}^{d} (A_i - B_i)^2$",
                    "expr": "cos(theta) = (A · B) / (||A|| ||B||)   |   d<sub>L2</sub><sup>2</sup>(A, B) = sum((A<sub>i</sub> - B<sub>i</sub>)<sup>2</sup>)",
                    "terms": [
                        ["A, B", "384-D float embedding vectors for the user query and a stored chunk."],
                        ["A · B", "Inner dot product sum(A<sub>i</sub> · B<sub>i</sub>) measuring directional overlap."],
                        ["||A||, ||B||", "L2 vector norms sqrt(sum(A<sub>i</sub><sup>2</sup>)), equal to 1.0 when unit-normalized."],
                        ["theta (angle)", "Angle between query and document vectors in radians/degrees."],
                        ["d<sub>L2</sub><sup>2</sup>", "Squared Euclidean distance printed by ChromaDB (0 = identical; &gt; 1.7 = unrelated)."],
                    ],
                    "example": (
                        "Worked 2D numerical example: Let unit vectors A=[0.8, 0.6] (MOSFET) and B=[0.6, 0.8] (Transistor). "
                        "A · B = 0.48 + 0.48 = 0.96 -&gt; angle = 16.3 deg, d<sub>L2</sub><sup>2</sup> = 2(1 - 0.96) = 0.08 (tight match). "
                        "For orthogonal C=[-0.6, 0.8] (Python), A · C = 0.0 -&gt; angle = 90 deg, d<sub>L2</sub><sup>2</sup> = 2.0 (reject)."
                    ),
                },
            },
            {
                "title": "5. Preempting 4 Common Day 1 Student Misconceptions",
                "summary": (
                    "Address these four conceptual blind spots explicitly before starting hands-on labs so students do not "
                    "build false mental models."
                ),
                "points": [
                    "<b>Misconception 1 ('Vectors encrypt text'):</b> Clarify that embeddings are lossy semantic fingerprints, not reversible encryption; original chunk text must still be stored in Chroma alongside vectors.",
                    "<b>Misconception 2 ('ChromaDB calls the cloud'):</b> ChromaDB + ONNX MiniLM execute 100% locally offline once downloaded; only the final LLM synthesis call hits Groq HTTPS.",
                    "<b>Misconception 3 ('Distance 1.9 means 19% match'):</b> Remind students Chroma prints distance (lower is better), NOT similarity score; ~1.0-1.4 is strong for unnormalized MiniLM queries.",
                    "<b>Misconception 4 ('Temperature 0 prevents hallucination'):</b> Temperature=0 only makes outputs deterministic/repeatable; without RAG grounding, an LLM deterministically outputs the same hallucination.",
                ],
            },
        ],
        "talking_points": [
            ["Poll Slides (S3-5)", "Scan QR. Log in with ECE / december30. Completely anonymous.", "Do not read options before students vote."],
            ["System Levels (S8)", "By Friday you ship Level 3. Level 4 is research scope — ignore it.", "Do not promise Level 4 multi-agent swarms in 5 days."],
            ["ECE Analogy (S11-12)", "LLM = controller, tool = actuator/plant, output = feedback sensor.", "Do not derive Laplace or Z-transforms."],
            ["Closed-Loop Video (S14)", "Click to play. Left cube crashes; right packet self-heals via memory.", "Let animation run without talking over it."],
            ["RAG Intro (S15-17)", "RAG means read your local files first, then answer with citations.", "Do not mention HyDE, RAG-Fusion, or rerankers yet."],
            ["Hallucination (S19)", "Models fill gaps with plausible fiction, even fake IEEE DOIs.", "Avoid saying 'AI lies' — explain probabilistic completion."],
            ["Setup Flow (S29)", "If you skipped pre-workshop install, finish it during lunch.", "Do not stop afternoon lecture for individual installs."],
            ["verify.py & Lab (S37-43)", "Watch dist=1.323: 'transistor' ranks 'MOSFET' first without overlap.", "Do not skip S43 lab drill — walk the rows."],
        ],
        "demos": [
            ("Demo 1: Verify Setup", "MANDATORY", [
                "PS> uv run python verify.py",
                "# Expected output:",
                "API Connected: Hello!",
                "ChromaDB Version: 1.0.7",
            ]),
            ("Demo 2: Vector Search Lab", "MANDATORY", [
                "PS> uv run python chroma_demo.py",
                "# Expected output:",
                "Query: 'How does a transistor work?'",
                "  dist=1.323 | The MOSFET gate voltage controls the channel drain current.",
                "  dist=1.534 | A capacitor stores electrostatic energy inside an electric field.",
                "  dist=1.938 | Python uses indentation cleanly to delimit code blocks.",
            ]),
        ],
        "faqs": [
            ["1", "Why Groq instead of OpenAI?", "Free tier handles class-wide API traffic fast. Endpoint is OpenAI-compatible."],
            ["2", "Do I need a dedicated GPU?", "No. ChromaDB runs CPU-only ONNX all-MiniLM-L6-v2 (~90 MB download once)."],
            ["3", "Why Python 3.13?", "uv.lock pins 3.13 for reproducible installs across Windows lab machines."],
            ["4", "Why uv instead of pip?", "uv resolves and creates .venv in under 2 seconds with deterministic lockfiles."],
            ["5", "My Groq key gives HTTP 401", "Remove quotes around GROQ_API_KEY in .env and verify no trailing spaces."],
            ["6", "chroma_demo.py appears stuck", "First run downloads ~90 MB ONNX model. Use phone hotspot if campus Wi-Fi stalls."],
            ["7", "What does dist=1.323 mean?", "L2/cosine distance: lower is closer. 1.0-1.4 is relevant; above 1.7 is noise."],
            ["8", "Why 384 dimensions?", "Best balance: ~1.5 KB RAM per vector on laptops while keeping technical meaning."],
            ["9", "Can I use VS Code instead of Antigravity?", "Yes. Any editor plus PowerShell works with all uv commands."],
        ],
        "mistakes": [
            ["1", "python: not found", "Python missing from PATH", "uv python install 3.13 ; restart shell"],
            ["2", "No module 'chromadb'", "Ran system python outside .venv", "uv sync ; uv run python verify.py"],
            ["3", "GROQ_API_KEY missing", "Left .env.example uncopied", "Copy-Item .env.example .env"],
            ["4", "HTTP 401 Unauthorized", "Quotes or bad key in .env", "Edit .env -> GROQ_API_KEY=gsk_... (no quotes)"],
            ["5", "Slow/stalled first run", "90 MB ONNX download blocked", "Switch to mobile hotspot for 1st download"],
        ],
        "skip_list": [
            ["Cut 1st", "S2 (AI Timeline)", "Historical context; safe to read offline."],
            ["Cut 2nd", "S23 (Why 384-D)", "Conceptual detail; does not block coding."],
            ["Cut 3rd", "S28 (Exact vs ANN)", "Algorithm comparison; revisit on Day 2 if asked."],
            ["NEVER CUT", "S37-43 (verify + chroma_demo)", "Core Day 1 readiness gates."],
        ],
        "answer_key_title": "Day 1 Answer Key — chroma_demo.py Distances",
        "answer_key_headers": ["Rank", "Document Text", "Expected Distance", "Why It Ranks Here"],
        "answer_key_rows": [
            ["1", "The MOSFET gate voltage controls...", "~1.32", "Direct semiconductor device match"],
            ["2", "A capacitor stores electrostatic energy...", "~1.53", "Related electrical physics vocabulary"],
            ["3", "Python uses indentation cleanly...", "~1.94", "Software topic — unrelated noise"],
        ],
        "answer_key_widths": [35, 185, 85, CONTENT_W - 305],
        "bridge_title": "END-OF-DAY BRIDGE TO DAY 2",
        "bridge_text": (
            "Tell the class: 'Today you searched 3 short sentences. Tomorrow at 09:00 AM we index entire ECE "
            "datasheets into disk-persisted ChromaDB, enforce a distance noise gate, and build Project 1: Vector RAG.'"
        ),
    },
    # ------------------------------------------------------------------ DAY 2
    {
        "day": 2,
        "slide_count": 39,
        "cover_title": "Day 2: Project 1 —<br/>ECE Vector RAG System",
        "cover_sub": "Instructor Session Plan: Chunking, Idempotent Upsert, Distance Gate &amp; Pytest",
        "timeline": [
            ["09:00-09:50", "50m", "1-5", "Cover, Why RAG, Fake-cases demo, blueprint, splitting", "Highlight 384-D continuity from Day 1 (S2) and lawyer case (S3)."],
            ["09:50-11:00", "70m", "6-8", "Sliding window, tokenization theory, 3D video", "Play anim_chunking_window (S8). Explain BPE sub-word splits."],
            ["11:00-11:30", "30m", "9", "Morning Tea Break", "Verify day-2 branch pulled by students."],
            ["11:30-13:00", "90m", "10-17", "Idempotency, fixed IDs, ingest.py + live demo, KB", "Run ingest.py twice live to prove identical chunk count."],
            ["13:00-14:00", "60m", "18", "Lunch Break", "Help students whose ingest.py indexed 0 files."],
            ["14:00-14:55", "55m", "19-28", "Distance curve, Precision/Recall, query.py, Temp, Mock", "Demo distance=1.65 noise gate and temperature=0.1."],
            ["14:55-15:30", "35m", "29-33", "Automated tests, pytest live run & negative test", "Show cricket world cup refusal BEFORE break (S33)."],
            ["15:30-15:40", "10m", "34", "Afternoon Break", "Check test_rag.py passes on laptops."],
            ["15:40-16:45", "65m", "35-39", "Code quality, bugs, Day 2 gate, Day 3 gap", "Verify all 3 gate commands pass cleanly."],
        ],
        "checklist": [
            "[ ] Branch day-2 checked out cleanly; uv sync green",
            "[ ] uv run python ingest.py runs clean twice (identical chunk count)",
            "[ ] uv run python query.py \"What is max Vds of IRF540N?\" --mock-llm cites irf540n_mosfet.md",
            "[ ] uv run pytest test_rag.py -v shows 3 passed",
            "[ ] knowledge_base/ holds 4 non-empty .md files",
            "[ ] Prepared out-of-scope demo query ('Who won the cricket world cup?')",
        ],
        "theory": [
            {
                "title": "1. Signal Dilution, Sliding-Window Chunking &amp; BPE Tokenization",
                "summary": (
                    "Embedding models pool an entire input string into one fixed 384-D vector (encoder cap ~256 word-pieces). "
                    "Chunking controls information density so individual ratings stand out sharply in vector space."
                ),
                "points": [
                    "<b>Semantic Dilution (Curse of Averaging):</b> Pooling an entire 20-page manual into one vector blends MOSFET Vds limits, package pins, and thermal graphs into one blurry centroid with poor recall.",
                    "<b>Sliding-Window Overlap Mechanics:</b> Setting <i>chunk_size=500</i> and <i>overlap=50</i> repeats the trailing 50 characters of chunk k at the head of chunk k+1, preventing split formulas ('Drain-Source Voltage' / '100 V').",
                    "<b>BPE Sub-Word Splitting:</b> Byte-Pair Encoding merges common byte sequences (~1.3 tokens/word). Part strings like 'IRF540N' fracture into 3-4 tokens, making character budgets distinct from token budgets.",
                ],
                "formula": {
                    "latex": r"$\mathrm{step} = \max(1,\; \mathrm{chunk\_size} - \mathrm{overlap}) \qquad N_{\mathrm{chunks}} = 1 + \left\lceil \frac{\max(0,\; L - \mathrm{chunk\_size})}{\mathrm{step}} \right\rceil$",
                    "expr": "step = max(1, chunk_size - overlap)   |   N<sub>chunks</sub> = 1 + ceil(max(0, L - chunk_size) / step)",
                    "terms": [
                        ["L", "Total normalized whitespace-collapsed length of the source document (characters)."],
                        ["chunk_size", "Maximum characters per chunk window (default = 500 chars)."],
                        ["overlap", "Trailing characters shared with the next window (default = 50 chars)."],
                        ["step", "Forward stride per iteration; max(1, ...) guarantees forward progress if overlap &gt;= chunk_size."],
                        ["N<sub>chunks</sub>", "Total vector chunks generated for that file."],
                    ],
                    "example": (
                        "Worked example: A datasheet of L = 1,420 chars with chunk_size=500, overlap=50 uses step = 450. "
                        "Slices span [0:500], [450:950], [900:1400], [1350:1420] -&gt; N<sub>chunks</sub> = 4 overlapping chunks."
                    ),
                },
            },
            {
                "title": "2. Database Idempotency &amp; Deterministic Primary Keys",
                "summary": (
                    "Pipeline reliability depends on idempotency: running ingest.py once or ten times must leave the vector "
                    "database in an identical state with zero stale or duplicate entries."
                ),
                "points": [
                    "<b>Why .add() Breaks Pipelines:</b> Using random UUIDs silently doubles chunk count every run (polluting Top-K with copies of the same chunk); reusing fixed IDs with .add() logs duplicate warnings and drops edits.",
                    "<b>Why .upsert() + Deterministic IDs Win:</b> Generating <i>f'{path.name}::chunk_{idx}'</i> enables in-place updates of text, vector embeddings, and metadata dictionaries.",
                    "<b>Note on Shrinking Files:</b> Teach advanced students that if an edited file drops from 5 chunks to 3, stale chunk_3/chunk_4 remain unless old prefix IDs are pruned first.",
                ],
                "formula": {
                    "latex": r"$f(f(x)) = f(x) \qquad\quad \mathrm{doc\_id} = \mathrm{filename}::\mathrm{chunk}_{idx}$",
                    "expr": "f(f(x)) = f(x)   |   doc_id = f\"{filename}::chunk_{idx}\"",
                    "terms": [
                        ["f(x)", "Idempotent ingestion operator (ingest_directory) mapping corpus state x to DB state."],
                        ["filename", "Canonical source basename (e.g., 'irf540n_mosfet.md') stored in metadata['source']."],
                        ["idx", "Zero-based integer chunk position along that file."],
                    ],
                    "example": (
                        "Verification check: Run 'uv run python ingest.py' twice in class. Output must print the exact same "
                        "chunk count (e.g., 12 chunks -&gt; 12 chunks) on both runs."
                    ),
                },
            },
            {
                "title": "3. Information Retrieval Trade-offs: Precision, Recall &amp; Noise Gates",
                "summary": (
                    "ChromaDB performs unconditional nearest-neighbor search: even a completely unrelated question returns "
                    "top_k chunks unless gated by a distance cutoff."
                ),
                "points": [
                    "<b>Precision vs. Recall Balance:</b> Tightening <i>max_distance</i> boosts Precision (fewer irrelevant chunks) but risks dropping paraphrased answers (lower Recall). Loosening it boosts Recall at the cost of noisy prompts.",
                    "<b>Empty-Hit Short-Circuiting:</b> When zero chunks satisfy <i>dist &lt;= 1.65</i>, returning 'Insufficient evidence' in Python saves an API call and enforces zero-hallucination safety.",
                ],
                "formula": {
                    "latex": r"$\mathrm{Precision} = \frac{TP}{TP + FP} \qquad \mathrm{Recall} = \frac{TP}{TP + FN} \qquad (\mathrm{keep\ iff}\; d \leq 1.65)$",
                    "expr": "Precision = TP / (TP + FP)   |   Recall = TP / (TP + FN)   |   Keep iff d &lt;= 1.65",
                    "terms": [
                        ["TP (True Positive)", "Retrieved chunks that genuinely answer the user's engineering query."],
                        ["FP (False Positive)", "Off-topic chunks slipped into context (noise causing hallucination)."],
                        ["FN (False Negative)", "Relevant chunks present in knowledge_base/ but missed by retrieval."],
                        ["d", "Chroma distance of candidate chunk; 1.65 acts as empirical ECE cutoff."],
                    ],
                    "example": (
                        "Worked trade-off: Query returns 3 hits at d=[0.72, 1.18, 1.81] where the 3rd is unrelated Python text. "
                        "Unfiltered Precision = 2/3 (66.7%). With d &lt;= 1.65 gate, the 1.81 hit is dropped -&gt; Precision = 2/2 (100%)."
                    ),
                },
            },
            {
                "title": "4. Softmax Temperature, Nucleus Sampling &amp; Grounded Prompting",
                "summary": (
                    "Instructors should connect neural next-token probabilities directly to why query.py sets "
                    "temperature=0.1 and strict system instructions."
                ),
                "points": [
                    "<b>Temperature Logit Scaling:</b> Dividing raw logits z<sub>i</sub> by T &lt; 1 exaggerates differences before softmax, collapsing probability onto the single highest-scoring token.",
                    "<b>Top-P (Nucleus) Safety Net:</b> Truncates low-probability tail words once cumulative mass reaches p (e.g., 0.9), blocking erratic token picks.",
                    "<b>Two-Stage Failure Isolation:</b> Always teach students to debug RAG in two halves: inspect retrieved chunks + distances first (Retrieval), then inspect synthesized wording + citations (Generation) using <b>--mock-llm</b>.",
                ],
                "formula": {
                    "latex": r"$P(\mathrm{token}_i) = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$",
                    "expr": "P(token<sub>i</sub>) = e<sup>z<sub>i</sub> / T</sup> / sum<sub>j</sub>(e<sup>z<sub>j</sub> / T</sup>)",
                    "terms": [
                        ["z<sub>i</sub>", "Raw unnormalized score (logit) output by the LLM head for candidate token i."],
                        ["T (Temperature)", "Sampling scale (&gt; 0). Lower T (&lt;= 0.2) gives deterministic facts; higher T (&gt;= 0.7) adds variety."],
                        ["e<sup>z<sub>i</sub>/T</sup>", "Exponential scaling magnifying logit gaps when T is small."],
                        ["sum<sub>j</sub> e<sup>z<sub>j</sub>/T</sup>", "Partition normalizer across all vocabulary tokens ensuring probabilities sum to 1."],
                    ],
                    "example": (
                        "Worked math: Suppose 3 token logits are z = [2.0, 1.0, 0.0]. At T=1.0, e<sup>z</sup> = [7.39, 2.72, 1.0] -&gt; "
                        "top token probability = 66.5% (33.5% chance of alternatives). At T=0.1, z/T = [20, 10, 0] -&gt; "
                        "top token probability = 99.995% (steady engineering answers)."
                    ),
                },
            },
            {
                "title": "5. Debugging Mental Model: Retrieval Bugs vs. Synthesis Bugs",
                "summary": (
                    "When a student reports 'RAG gave the wrong answer', diagnose which pipeline stage failed before touching prompts."
                ),
                "points": [
                    "<b>Stage 1 Fault (Zero/Wrong Chunks Retrieved):</b> Inspect collection.count() and chunk distances. Typical causes: forgot ingest.py, chunk_size &gt; 1500 diluting specs, or max_distance set too tight (&lt; 1.1).",
                    "<b>Stage 2 Fault (Right Chunk Retrieved, Bad Answer):</b> Verify --mock-llm cites [filename.md] correctly. Typical causes: temperature &gt; 0.5, weak system prompt, or missing [source] tag inside context_block formatting.",
                ],
            },
        ],
        "talking_points": [
            ["Fake Cases (S3)", "Real 2023 court sanction from ungrounded ChatGPT output.", "Avoid mocking the lawyer; focus on missing verification."],
            ["Tokenization (S7)", "'IRF540N' splits into 4 sub-word tokens — chars != tokens.", "Do not dive into BPE training merge tables."],
            ["Chunking Video (S8)", "Watch edge words repeat across adjacent chunks via 50-char overlap.", "Skip heavy HNSW parameter math (M, efConstruction)."],
            ["ingest.py (S14-15)", "Look at fixed ID: path.name::chunk_idx + upsert() = idempotent.", "Do not let students switch to .add()."],
            ["Distance Gate (S21-23)", "Drop dist > 1.65 BEFORE calling Groq; return refusal if empty.", "Never pass low-similarity noise into prompt context."],
            ["Negative Test (S33)", "Refusal is success in RAG. Never answer cricket questions from MOSFET docs.", "Keep refusal message consistent for Day 5 tests."],
        ],
        "demos": [
            ("Demo 1: Idempotent Ingestion (Run Twice)", "MANDATORY", [
                "PS> uv run python ingest.py",
                "Ingestion complete. Collection 'ece_knowledge' now holds 12 chunks.",
                "PS> uv run python ingest.py",
                "Ingestion complete. Collection 'ece_knowledge' now holds 12 chunks.",
            ]),
            ("Demo 2: Grounded Semantic Query", "MANDATORY", [
                "PS> uv run python query.py \"What is max Vds of IRF540N?\" --mock-llm",
                "Retrieved 2 chunks:",
                " - [irf540n_mosfet.md] dist=0.7241",
                "Grounded Answer (from [irf540n_mosfet.md], dist=0.7241): ... 100 V ...",
            ]),
            ("Demo 3: Out-of-Scope Negative Test", "MANDATORY", [
                "PS> uv run python query.py \"Who won the cricket world cup?\"",
                "Retrieved 0 chunks:",
                "Insufficient evidence in the indexed knowledge base to answer that question.",
            ]),
            ("Demo 4: Automated Pytest Verification", "MANDATORY", [
                "PS> uv run pytest test_rag.py -v",
                "3 passed in ~2.1s",
            ]),
        ],
        "faqs": [
            ["1", "Why chunk_size=500 instead of 2000?", "500 chars keeps one spec focused. 2000 chars blends unrelated tables into weak embeddings."],
            ["2", "Why overlap=50?", "Stops key specs ('max Vds' + '100 V') from getting split across chunk boundaries."],
            ["3", "Why upsert() instead of add()?", "add() duplicates rows or warns on repeated IDs. upsert() keeps total chunks constant."],
            ["4", "Why max_distance=1.65?", "Noise gate: anything above 1.65 is irrelevant text that causes hallucinations."],
            ["5", "Why does --mock-llm exist?", "Enables deterministic offline pytest runs and grading without Groq rate limits."],
            ["6", "ingest.py indexes 0 chunks?", "Check knowledge_base/ contains .md files and check cwd is repo root."],
            ["7", "Can I add custom PDFs/notes?", "Export text to .md in knowledge_base/ and re-run ingest.py."],
            ["8", "What is PersistentClient?", "Writes SQLite + HNSW vectors to chroma_db/ on disk instead of volatile RAM."],
        ],
        "mistakes": [
            ["1", "0 chunks indexed", "Wrong cwd or empty .md files", "cd repo root ; check knowledge_base/*.md"],
            ["2", "Duplicate chunk count grows", "Used .add() or random UUID ids", "Switch to .upsert() with f'{name}::chunk_{idx}'"],
            ["3", "chroma_db/ pushed to Git", "Missing .gitignore entry", "Add chroma_db/ to .gitignore ; git rm -r --cached chroma_db/"],
            ["4", "Bad Top-1 match", "chunk_size set > 1500", "Reset chunk_size=500, overlap=50"],
            ["5", "FileNotFoundError on query", "Relative DB path bug", "Use Path(__file__).resolve().parent / 'chroma_db'"],
        ],
        "skip_list": [
            ["Cut 1st", "S27 (Temperature & top_p)", "Quick rule: keep temperature=0.1; explain in 30s."],
            ["Cut 2nd", "S7 (BPE Tokenization)", "Interesting theory; cut if running > 15 min behind."],
            ["Cut 3rd", "S30 (Why Automated Tests)", "Students see pytest work live on S31-32."],
            ["NEVER CUT", "S14-15, S22-23, S31-33", "Core Project 1 ingest, query, pytest, negative gate."],
        ],
        "answer_key_title": "Day 2 Answer Key — Expected Query Results",
        "answer_key_headers": ["Query", "Top-1 Source", "Distance", "Expected Text Fragment"],
        "answer_key_rows": [
            ["What is max Vds of IRF540N?", "irf540n_mosfet.md", "~0.6-0.9", "Drain-Source Voltage (Vds): 100 V"],
            ["ESP32 ADC limit during Wi-Fi", "esp32_s3_datasheet.md", "~0.8-1.1", "ADC2 channels cannot be used while Wi-Fi is active"],
            ["5G NR PRB utilization threshold", "5g_nr_prb_spec.md", "~0.7-1.0", "PRB utilization > 85%"],
            ["LiFePO4 battery max charge", "lorawan_bms_notes.md", "~0.8-1.1", "14.6 V charge cutoff"],
            ["Who won the cricket world cup?", "(none — hits = [])", "> 1.65", "Insufficient evidence in indexed KB"],
        ],
        "answer_key_widths": [125, 110, 62, CONTENT_W - 297],
        "bridge_title": "END-OF-DAY BRIDGE TO DAY 3",
        "bridge_text": (
            "Close with: 'Project 1 answers questions when files never move. What happens tomorrow if "
            "sensor.csv moves into data/iot_sensor_log.json? Static RAG fails. Day 3 builds an autonomous loop that heals itself.'"
        ),
    },
    # ------------------------------------------------------------------ DAY 3
    {
        "day": 3,
        "slide_count": 40,
        "cover_title": "Day 3: Closed-Loop ReAct<br/>Agents &amp; Vector Memory",
        "cover_sub": "Instructor Session Plan: Safe Tools, Exception Recovery, trace.jsonl &amp; AAR",
        "timeline": [
            ["09:00-10:00", "60m", "1-5", "Control loop, ReAct paper (ICLR 23), JSON handshake", "Emphasize interleaved Thought + Action + Observation."],
            ["10:00-11:00", "60m", "6-9", "4 tools, error dicts vs crashes, sandbox safety, recovery", "Show why uncaught tracebacks kill autonomy."],
            ["11:00-11:30", "30m", "10", "Morning Tea Break", "Confirm students checked out day-3."],
            ["11:30-12:30", "60m", "11-18", "3D self-heal video, error hints, step engine, threat model", "Play anim_react_self_heal (S11). Highlight prompt injection."],
            ["12:30-13:00", "30m", "19-22", "trace.jsonl anatomy, AST check, industry uses, caps", "Warn: linear print() scripts score 0/20 on Friday."],
            ["13:00-14:00", "60m", "23", "Lunch Break", "Verify _resolve_safe() questions."],
            ["14:00-14:50", "50m", "24-31", "Dual memory, Tulving brain model, AAR engine, 3D video", "Play anim_cross_session_memory (S30)."],
            ["14:50-15:30", "40m", "32-35", "Scaling, demo output, Trace Diff & Check Today lab", "Students run demo_cross_session.py + pytest BEFORE break."],
            ["15:30-15:40", "10m", "36", "Afternoon Break", "Confirm trace_run1 and trace_run2 files generated."],
            ["15:40-16:45", "65m", "37-40", "Threshold tip, Day 4 preview, 3 Capstone tracks", "Explain unassisted sprint rules for Thursday morning."],
        ],
        "checklist": [
            "[ ] Branch day-3 checked out; uv sync clean",
            "[ ] uv run python demo_cross_session.py --mock-llm prints 4 -> 2 steps",
            "[ ] uv run pytest test_agent.py -v passes all checks",
            "[ ] trace_run1.jsonl (4 lines) and trace_run2.jsonl (2 lines) inspected",
            "[ ] Reviewed Yao et al. (ICLR 2023) ReAct core claim for Q&A",
        ],
        "theory": [
            {
                "title": "1. The ReAct Paradigm (Yao et al., ICLR 2023)",
                "summary": (
                    "Chain-of-Thought (CoT) prompting alone reasons over static training memory and propagates early errors; "
                    "ReAct interleaves internal reasoning traces with real Python observations in a stateful loop."
                ),
                "points": [
                    "<b>Why Interleaving Beats Open-Loop CoT:</b> Grounding each reasoning step in an external environment observation lets the agent discover missing filenames, adjust parameters, and avoid hallucinating unverified file contents.",
                    "<b>Finite Trajectory Horizon:</b> Every step appends (Thought, Action, Observation) to running state s<sub>t</sub> until either tool == 'FINAL_ANSWER' / terminal report or t reaches max_steps.",
                ],
                "formula": {
                    "latex": r"$s_{t+1} = s_t \cup \{(\mathrm{Thought}_t,\; \mathrm{Action}_t,\; \mathrm{Observation}_t)\}, \quad 1 \leq t \leq \mathrm{max\_steps}$",
                    "expr": "s<sub>t+1</sub> = s<sub>t</sub> U { (Thought<sub>t</sub>, Action<sub>t</sub>, Observation<sub>t</sub>) },   1 &lt;= t &lt;= max_steps",
                    "terms": [
                        ["s<sub>t</sub>", "Accumulated agent trajectory context up to iteration step t."],
                        ["Thought<sub>t</sub>", "Short natural-language rationale emitted by the LLM diagnosing current state."],
                        ["Action<sub>t</sub>", "JSON tool selection {'tool': name, 'args': {...}} validated before execution."],
                        ["Observation<sub>t</sub>", "Structured Python dict returned by the tool (data or recoverable error)."],
                        ["max_steps", "Upper bound (default 10) preventing infinite retry cycles on impossible goals."],
                    ],
                    "example": (
                        "Whiteboard distinction: Hardcoded scripts score 0/20 on Day 5 because they never branch on "
                        "Observation<sub>t</sub> inside a loop — even if they print '[Step 1]..[Step 4]' to stdout."
                    ),
                },
            },
            {
                "title": "2. Structured JSON Contracts, Dispatch &amp; Latency Decomposition",
                "summary": (
                    "Production agents treat LLM output as untrusted JSON across an RPC interface and instrument every step "
                    "to separate network inference latency from local vector/tool speed."
                ),
                "points": [
                    "<b>JSON Object Mode (response_format):</b> Constrains Groq sampling logits to valid JSON syntax, eliminating fragile regex extraction bugs when models prepend prose.",
                    "<b>TOOL_REGISTRY Whitelist:</b> Looking up <i>TOOL_REGISTRY.get(tool)</i> ensures unknown hallucinated tool names return <i>{'ok': False, 'error': 'UnknownTool'}</i> cleanly instead of executing eval/exec.",
                    "<b>Perf Counter Profiling:</b> Measuring <i>elapsed_ms</i> around each step shows students that 95%+ of latency lives in cloud API round-trips rather than local ChromaDB or Python file I/O.",
                ],
                "formula": {
                    "latex": r"$T_{\mathrm{total}} = T_{\mathrm{recall}} + \sum_{t=1}^{S} (T_{\mathrm{llm},t} + T_{\mathrm{tool},t}) + T_{\mathrm{aar}}$",
                    "expr": "T<sub>total</sub> = T<sub>recall</sub> + sum<sub>t=1..S</sub>(T<sub>llm,t</sub> + T<sub>tool,t</sub>) + T<sub>aar</sub>",
                    "terms": [
                        ["T<sub>recall</sub>", "Step 0 episodic AAR query time in ChromaDB on disk (typically 5-15 ms)."],
                        ["S", "Actual executed steps (4 cold vs. 2 warm in Day 3 lab)."],
                        ["T<sub>llm,t</sub>", "Groq API JSON policy inference latency (~300-800 ms live; &lt; 1 ms mock)."],
                        ["T<sub>tool,t</sub>", "Local Python tool I/O latency (typically 1-5 ms)."],
                        ["T<sub>aar</sub>", "Post-run AAR distillation + Chroma upsert time (~5-15 ms)."],
                    ],
                    "example": (
                        "Speedup impact: Cutting 2 redundant error/discovery steps saves ~1,000 ms of live LLM round-trips "
                        "plus ~2x prompt token spend per task."
                    ),
                },
            },
            {
                "title": "3. Self-Healing Error Dicts, Sandboxing &amp; Prompt Injection Defense",
                "summary": (
                    "Tools must protect the host OS from both accidental wrong paths and adversarial text hidden inside "
                    "data files (indirect prompt injection)."
                ),
                "points": [
                    "<b>Recoverable Sensor Errors:</b> Catching FileNotFoundError and listing <i>hints=sorted(...)</i> converts fatal tracebacks into actionable steering cues for step t+1.",
                    "<b>Canonical Path Containment:</b> Always resolve symlinks and '..' segments before checking workspace containment; naive string prefix checks ('../' substring check) are easily bypassed.",
                    "<b>Indirect Prompt Injection Defense:</b> Never interpolate tool outputs into shell commands or eval(). Restrict capabilities strictly to the whitelisted 4 tools inside workdir.",
                ],
                "formula": {
                    "latex": r"$\mathrm{safe\_access} \;\Longleftrightarrow\; \mathrm{resolve}(\mathrm{workdir} / \mathrm{rel}) \subseteq \mathrm{resolve}(\mathrm{workdir})$",
                    "expr": "safe_access  &lt;=&gt;  (workdir / rel).resolve() inside workdir.resolve()",
                    "terms": [
                        ["workdir", "Root directory assigned to the agent run (resolved canonically)."],
                        ["rel", "Untrusted relative path string supplied in Action<sub>t</sub>['args']."],
                        [".resolve()", "OS-level path normalization collapsing '..', '.', and symlinks."],
                        ["inside check", "workdir.resolve() in target.parents or target == workdir.resolve()."],
                    ],
                    "example": (
                        "Attack rejection example: If LLM passes filepath='../../.env', target.resolve() resolves outside "
                        "workdir.resolve(). _resolve_safe() raises/returns PermissionError dict without touching host files."
                    ),
                },
            },
            {
                "title": "4. Dual Memory (Tulving 1972), AAR Hygiene &amp; Cross-Session Speedup",
                "summary": (
                    "Cognitive psychologist Endel Tulving separated timeless fact memory from lived event memory. Day 3 "
                    "implements both cleanly in separate ChromaDB collections."
                ),
                "points": [
                    "<b>Collection Separation:</b> <i>ece_knowledge</i> stores unchanging datasheet limits (Semantic); <i>episodic_aar</i> stores operational lessons learned from errors (Episodic). Keeping them separate prevents old bug logs from polluting spec queries.",
                    "<b>1-Sentence AAR Compression:</b> Raw multi-line logs dilute 384-D vector similarity. Compressing a multi-step trace into a single directive sentence maximizes Step 0 recall signal.",
                    "<b>Deterministic Goal Keying:</b> Using SHA-1 hash prefixes ensures re-running the same goal updates the rule in place via upsert().",
                ],
                "formula": {
                    "latex": r"$\mathrm{Speedup} = \frac{S_{\mathrm{cold}} - S_{\mathrm{warm}}}{S_{\mathrm{cold}}} \times 100\% \qquad\quad \mathrm{doc\_id} = \mathrm{aar\_} + \mathrm{SHA1}(\mathrm{goal})_{[:12]}$",
                    "expr": "Speedup = ((S<sub>cold</sub> - S<sub>warm</sub>) / S<sub>cold</sub>) &times; 100%   |   doc_id = 'aar_' + sha1(goal)[:12]",
                    "terms": [
                        ["S<sub>cold</sub>", "Steps taken on Run 1 with empty episodic_aar (blind guess + recovery)."],
                        ["S<sub>warm</sub>", "Steps taken on Run 2 after cold Python restart recalls AAR rule on Step 0."],
                        ["sha1(goal)[:12]", "12-hex-char deterministic hash prefix creating an idempotent primary key per goal."],
                    ],
                    "example": (
                        "Day 3 benchmark: S<sub>cold</sub> = 4 steps (missing sensor.csv -&gt; list_dir -&gt; read data/ -&gt; report). "
                        "S<sub>warm</sub> = 2 steps (recall AAR -&gt; direct read -&gt; report). Speedup = (4 - 2) / 4 &times; 100% = 50%."
                    ),
                },
            },
            {
                "title": "5. Whiteboard Trace Walkthrough: Cold Self-Heal vs. Warm Recall",
                "summary": (
                    "Sketch both timelines side-by-side on the whiteboard before running demo_cross_session.py so students "
                    "spot the exact transition from 'error' to 'recovered'."
                ),
                "points": [
                    "<b>Run 1 Timeline:</b> Step 1 read_file('sensor.csv') [status='error'] -&gt; Step 2 list_dir('data') [status='recovered'] -&gt; Step 3 read_file('data/iot_sensor_log.json') [status='recovered'] -&gt; Step 4 write_report() [status='recovered'] -&gt; store AAR on disk.",
                    "<b>Cold Process Restart + Run 2:</b> All Python RAM variables vanish; Step 0 queries PersistentClient('agent_memory'), injects AAR lesson into Step 1 prompt, skips Steps 1-2 completely, and finishes in 2 steps.",
                ],
            },
        ],
        "talking_points": [
            ["ReAct Paper (S3)", "Interleaving reasoning thoughts with tool calls beats chain-of-thought.", "Avoid long transformer attention math."],
            ["Sandbox Why (S8)", "Always validate path stays inside workdir via _resolve_safe().", "Do not encourage running raw shell tools in agent."],
            ["3D Self-Heal (S11)", "Watch Step 1 return hints instead of crashing; Step 2 recovers.", "Let video play completely first."],
            ["Grader Check (S20)", "Day 5 inspects AST: zero loop in agent.py = automatic 0/20 marks.", "Do not name exact AST test internal variables."],
            ["Dual Memory (S24-26)", "Semantic = textbook specs; Episodic = yesterday's bug fix.", "Never mix ece_knowledge and episodic_aar collections."],
            ["Check Today (S35)", "Ensure every student sees 4 -> 2 step reduction before leaving.", "Do not skip trace_run1 vs trace_run2 check."],
        ],
        "demos": [
            ("Demo 1: Cross-Session Memory Speedup", "MANDATORY", [
                "PS> uv run python demo_cross_session.py --mock-llm",
                "# Expected output:",
                "Run 1 (Cold Start): 4 steps | Recalled: 0 | AAR: Inspect 'data/iot_sensor_log.json'...",
                "Run 2 (Warm Recall): 2 steps | Recalled: 1 | AAR: Inspect 'data/iot_sensor_log.json'...",
            ]),
            ("Demo 2: Inspecting Step Traces Side by Side", "MANDATORY", [
                "PS> Get-Content trace_run1.jsonl   # 4 JSON lines (Step 1 error -> Step 2 list_dir -> recovered)",
                "PS> Get-Content trace_run2.jsonl   # 2 JSON lines (Direct hit via Step 0 AAR precedent)",
            ]),
            ("Demo 3: Agent Unit Tests", "MANDATORY", [
                "PS> uv run pytest test_agent.py -v",
                "# Expected: recovery test, max_steps cap test, and memory persistence test pass",
            ]),
        ],
        "faqs": [
            ["1", "What is the ReAct paper?", "Yao et al., ICLR 2023 — Thought -> Action -> Observation outperforms isolated CoT."],
            ["2", "Why max_steps=10?", "Hard loop budget stops infinite LLM loops and prevents runaway Groq API billing."],
            ["3", "What does _resolve_safe() block?", "Resolves absolute paths and returns PermissionError dict if path leaves workdir ('../')."],
            ["4", "Why two Chroma collections?", "Static datasheets vs runtime AAR lessons avoid injecting fault logs into spec Q&A."],
            ["5", "What if a stored AAR lesson is stale?", "Deterministic SHA-1 doc_id on goal overwrites prior rule cleanly on upsert()."],
            ["6", "Can agents fix hardware or missing Wi-Fi?", "No — self-healing works strictly within the local tools and error hints exposed."],
            ["7", "Why record trace.jsonl?", "Proves loop execution to Day 5 AST/trace graders and aids live oral defense."],
            ["8", "How does prompt injection happen?", "Untrusted data strings like 'Ignore rules' confuse naive models; tool arg validation stops it."],
        ],
        "mistakes": [
            ["1", "Infinite tool loop", "Tool repeats failing call blindly", "Enforce max_steps=10 + return hints in error dict"],
            ["2", "Zero step reduction on Run 2", "Used non-persistent Client()", "Switch to chromadb.PersistentClient(path=...)"],
            ["3", "JSONDecodeError on LLM reply", "Parsed free-form markdown text", "Set response_format={'type': 'json_object'}"],
            ["4", "Cross-task wrong recall", "Recall distance cutoff too loose (>1.8)", "Tighten recall distance cutoff cleanly"],
            ["5", "Unhandled crash on bad file", "Raised FileNotFoundError uncaught", "Wrap tool body in try/except returning ok=False dict"],
        ],
        "skip_list": [
            ["Cut 1st", "S21 (Industry Agents)", "Motivational context only."],
            ["Cut 2nd", "S25 (Cognitive Science)", "Quick analogy; Day 2/3 dual diagram already explains it."],
            ["Cut 3rd", "S32 (Memory Scaling)", "Brief mention suffices if ahead of Afternoon Break."],
            ["NEVER CUT", "S11-14, S28-35 (Demos & Checks)", "Core ReAct loop + AAR memory speedup proofs."],
        ],
        "answer_key_title": "Day 3 Answer Key — Cold vs Warm Run Metrics",
        "answer_key_headers": ["Metric", "Run 1 (Cold Start)", "Run 2 (Warm Recall)"],
        "answer_key_rows": [
            ["Total Steps", "4 steps", "2 steps (50% reduction)"],
            ["Error Steps", "1 (FileNotFoundError on sensor.csv)", "0 errors"],
            ["Recovered Steps", "1 (via list_dir('data'))", "0 needed"],
            ["AAR Stored / Recalled", "Stored = Yes | Recalled = No", "Stored = Updated | Recalled = Yes"],
            ["trace.jsonl Lines", "4 lines", "2 lines"],
        ],
        "answer_key_widths": [135, 175, CONTENT_W - 310],
        "bridge_title": "END-OF-DAY BRIDGE TO DAY 4",
        "bridge_text": (
            "Tell students: 'Starting tomorrow at 09:00 AM, step-by-step code handouts stop. Pick IoT Fleet, "
            "5G NR Radio, or Literature Research, and ship your own modular agent before 16:45 PM code freeze.'"
        ),
    },
    # ------------------------------------------------------------------ DAY 4
    {
        "day": 4,
        "slide_count": 35,
        "cover_title": "Day 4: Unassisted Capstone<br/>Architecture &amp; Build Sprint",
        "cover_sub": "Instructor &amp; Mentor Triage Playbook, Track Thresholds &amp; Sprint Milestones",
        "timeline": [
            ["09:00-11:00", "120m", "1-8", "Sprint rules, 3 tracks, starter cmd, contracts, AI tests", "Project git checkout day-4 + uv sync live; teams select track."],
            ["11:00-11:30", "30m", "9", "Morning Tea Break", "Confirm every team declared IoT, 5G, or Research track."],
            ["11:30-12:15", "45m", "10-16", "Deep dive: Track 1 IoT, Track 2 5G, Track 3 Research, Registry", "Clarify exact numerical thresholds for all 3 tracks."],
            ["12:15-13:00", "45m", "18-30", "Mistakes, trace schema, tests, Batch B preview, pacing", "Walk trace.jsonl schema (S21-22) and defensive code (S27)."],
            ["13:00-14:00", "60m", "17", "Lunch Break", "Verify all laptops have clean day-4 branch."],
            ["14:00-15:30", "90m", "—", "UNASSISTED BUILD SPRINT (Mentors triage only)", "Do NOT write student code; check 14:15 tools + 15:15 loop milestones."],
            ["15:30-15:40", "10m", "31", "Afternoon Break", "Check ReAct loop + trace.jsonl running on team repos."],
            ["15:40-16:45", "65m", "32-35", "Hardening, Git cleanup & 16:45 CODE FREEZE", "Confirm all pytest suites pass & no .env staged before freeze."],
        ],
        "checklist": [
            "[ ] Branch day-4 checked out and uv sync verified on instructor machine",
            "[ ] uv run pytest capstone_*/test_tools.py -v passes cleanly on starter reference",
            "[ ] Projector shows S6 starter commands (git checkout day-4 ; uv sync)",
            "[ ] Track selection sheet / board ready for team sign-ups",
            "[ ] Reviewed IoT, 5G, and Research exact thresholds in Reference section below",
        ],
        "theory": [
            {
                "title": "1. Software Architecture: Isolating Determinism From Stochasticity",
                "summary": (
                    "The core engineering rule for Day 4's unassisted sprint is fault containment: because LLM outputs vary "
                    "across runs, every safety guard, threshold check, and persistence guarantee must live in deterministic Python."
                ),
                "points": [
                    "<b>Deterministic Layer (tools.py, ingest.py, memory.py):</b> Schema checks, NaN filtering, path sandboxing, threshold math, and Chroma persistence are pure Python functions testable in milliseconds with pytest.",
                    "<b>Stochastic Layer (agent.py):</b> Only policy selection calls Groq HTTPS APIs, isolating prompt tuning cleanly from data-parsing correctness.",
                    "<b>Package Hygiene (__init__.py):</b> Including <i>__init__.py</i> plus fallback relative/local imports lets both pytest package discovery and direct script execution succeed reliably.",
                ],
            },
            {
                "title": "2. Tool Registry Pattern &amp; Verification Under Non-Determinism",
                "summary": (
                    "Mapping tool names via a dictionary decouples the control loop from domain functions, while --mock-llm "
                    "enables repeatable tests of the full control loop."
                ),
                "points": [
                    "<b>Open/Closed Dispatch:</b> <i>TOOL_REGISTRY = {'list_dir': list_dir, ...}</i> lets teams swap domain tools across IoT, 5G, and Research tracks without rewriting loop infrastructure.",
                    "<b>Why --mock-llm Preserves Real Tools:</b> Mock mode replaces ONLY the next-action policy function while running the actual while-loop, real JSON parsing, and disk ChromaDB — proving true integration.",
                    "<b>Structural Invariant Assertions:</b> Assert stable system invariants (quarantine count, trace step monotonicity, flagged IDs in Markdown) rather than brittle exact English phrasing.",
                ],
            },
            {
                "title": "3. Track 1 Domain Physics: Power Electronics &amp; IoT Fleet Limits",
                "summary": (
                    "Coach Track 1 students on why the IRF540N MOSFET and 24 V bus thresholds exist physically in motor-drive nodes."
                ),
                "points": [
                    "<b>Inductive V<sub>ds</sub> Avalanche (&gt; 100 V):</b> Motor windings store energy (0.5 · L · I<sup>2</sup>). Switching off without flyback clamping spikes V<sub>ds</sub> above IRF540N's 100 V rating.",
                    "<b>Ohmic Conduction Heating (&gt; 85 °C):</b> Excessive R<sub>ds(on)</sub> drop causes P<sub>cond</sub> loss, raising PCB/junction temperature toward derating limits; below 18 V on a 24 V rail indicates power supply brownout.",
                ],
                "formula": {
                    "latex": r"$P_{\mathrm{cond}} = I_d^2 \cdot R_{\mathrm{ds(on)}} \qquad\quad T_j = T_a + (P_{\mathrm{cond}} + P_{\mathrm{sw}}) \cdot R_{\theta JA}$",
                    "expr": "P<sub>cond</sub> = I<sub>d</sub><sup>2</sup> · R<sub>ds(on)</sub>   |   T<sub>j</sub> = T<sub>a</sub> + (P<sub>cond</sub> + P<sub>sw</sub>) · R<sub>thetaJA</sub>",
                    "terms": [
                        ["I<sub>d</sub>", "Continuous MOSFET drain current flowing through the motor phase (Amperes)."],
                        ["R<sub>ds(on)</sub>", "Drain-to-source on-state resistance (0.044 Ohm max for IRF540N at V<sub>gs</sub>=10 V)."],
                        ["P<sub>cond</sub>", "Static ohmic power dissipated as heat in the silicon channel (Watts)."],
                        ["P<sub>sw</sub>", "Dynamic switching loss during PWM transitions (depends on frequency &amp; Q<sub>g</sub>=71 nC)."],
                        ["T<sub>a</sub>, T<sub>j</sub>", "Ambient / sensor board temp vs. silicon junction temp (max 175 °C, warn &gt; 85 °C)."],
                        ["R<sub>&theta;JA</sub> (theta-JA)", "Junction-to-ambient thermal resistance (°C/W, ~62 °C/W bare TO-220)."],
                    ],
                    "example": (
                        "Worked IRF540N calc: At I<sub>d</sub> = 16 A and R<sub>ds(on)</sub> = 0.044 Ohm, P<sub>cond</sub> = 16<sup>2</sup> &times; 0.044 = 11.26 W. "
                        "Without a heatsink (R<sub>thetaJA</sub> = 62 °C/W), junction temperature rises far past +175 °C -&gt; matches NODE-02 fault (108.5 V, 94.8 °C)."
                    ),
                },
            },
            {
                "title": "4. Track 2 Domain Physics: 5G NR Band n78 Radio Link KPIs",
                "summary": (
                    "Coach Track 2 students on the three physical-layer / MAC metrics inside gnb_kpis.json for 3GPP Band n78 (3.5 GHz TDD)."
                ),
                "points": [
                    "<b>Spectrum Saturation (PRB &gt; 85%):</b> High Physical Resource Block occupancy leaves zero scheduling headroom for incoming UEs and latency-critical traffic.",
                    "<b>Interference &amp; Link Failure (SINR &lt; 3.0 dB, BLER &gt; 10%):</b> Neighbor-cell interference collapses Signal-to-Interference-plus-Noise Ratio, forcing lower MCS modulation and failing 3GPP's 10% initial-BLER target.",
                ],
                "formula": {
                    "latex": r"$\mathrm{PRB} = \frac{N_{\mathrm{used}}}{N_{\mathrm{total}}} \times 100\% \qquad \mathrm{SINR}_{\mathrm{dB}} = 10\log_{10}\left(\frac{S}{I+N}\right) \qquad \mathrm{BLER} = \frac{N_{\mathrm{err}}}{N_{\mathrm{blk}}} \times 100\%$",
                    "expr": "PRB = (N<sub>used</sub> / N<sub>total</sub>) &times; 100%  |  SINR<sub>dB</sub> = 10 log<sub>10</sub>(S / (I+N))  |  BLER = (N<sub>err</sub> / N<sub>blk</sub>) &times; 100%",
                    "terms": [
                        ["N<sub>used</sub>, N<sub>total</sub>", "Allocated vs. total Physical Resource Blocks per slot (e.g., 273 PRBs at 100 MHz SCS=30 kHz)."],
                        ["S / (I + N)", "Linear ratio of desired serving-cell signal power to interference + thermal noise power."],
                        ["SINR<sub>dB</sub>", "Decibel link quality; below 3.0 dB prevents reliable QPSK/16-QAM decoding."],
                        ["N<sub>err</sub>, N<sub>blk</sub>", "CRC-failed transport blocks vs. total received transport blocks (BLER &gt; 10% flags fault)."],
                    ],
                    "example": (
                        "GNB-BLR-02 diagnosis: PRB=94.1% (congested), SINR=1.4 dB (heavy interference), BLER=14.6% (excessive HARQ retries) "
                        "— all three thresholds trip simultaneously while GNB-BLR-01/03 remain nominal."
                    ),
                },
            },
            {
                "title": "5. Track 3 Theory: Edge AI Pareto Latency vs. F1 Filtering",
                "summary": (
                    "Coach Track 3 students on multi-objective Pareto screening across edge deployment candidates."
                ),
                "points": [
                    "<b>Dual Constraint Gate:</b> A study qualifies as Production-Ready strictly when real-time speed (latency_ms &lt;= 50.0, i.e., &gt;= 20 Hz inference) AND balanced accuracy (f1_score &gt;= 0.85) hold simultaneously.",
                    "<b>Why F<sub>1</sub> Instead of Accuracy:</b> Hardware anomaly classes are heavily imbalanced (99% normal, 1% faults); F<sub>1</sub> harmonic mean penalizes classifiers that miss rare faults.",
                ],
                "formula": {
                    "latex": r"$F_1 = \frac{2 \cdot \mathrm{Precision} \cdot \mathrm{Recall}}{\mathrm{Precision} + \mathrm{Recall}} \qquad (\mathrm{latency} \leq 50\ \mathrm{ms},\; F_1 \geq 0.85)$",
                    "expr": "F<sub>1</sub> = 2 · (Precision · Recall) / (Precision + Recall)   |   Pass iff latency &lt;= 50 ms &amp; F<sub>1</sub> &gt;= 0.85",
                    "terms": [
                        ["Precision", "Fraction of predicted anomalies/detections that are true positives."],
                        ["Recall", "Fraction of actual target events successfully detected by the edge model."],
                        ["F<sub>1</sub>", "Harmonic mean balancing Precision and Recall (drops sharply if either is low)."],
                        ["latency_ms", "Per-sample forward-pass inference time on target edge MCU/NPU."],
                    ],
                    "example": (
                        "Worked comparison: If Precision=0.90 and Recall=0.82, F<sub>1</sub> = 2 &times; (0.90 &times; 0.82) / 1.72 = 0.858 (&gt;= 0.85). "
                        "In paper_abstracts.json, ECE-2025-101 (14.2 ms, 0.94) and 103 (22.8 ms, 0.96) qualify; 102 (480 ms, 0.52) rejects."
                    ),
                },
            },
        ],
        "talking_points": [
            ["Sprint Rules (S2)", "Today we review architecture, never type code for your team.", "Do not touch student keyboards to fix bugs directly."],
            ["Modularity (S3)", "Keep tools.py pure Python, agent.py policy-only, memory.py persistent.", "Do not merge all logic into one 300-line script."],
            ["Starter Cmds (S6)", "Run git checkout day-4 and uv sync cleanly before inspecting track folders.", "Do not edit files directly on main branch."],
            ["Testing AI (S8)", "Verify with --mock-llm so loop and trace pass without Groq rate limits.", "Do not mock out ChromaDB or read_telemetry inside tests."],
            ["Track Specs (S10-15)", "All 3 tracks share one contract: 4 tools, loop, trace, out/*.md.", "Do not invent custom thresholds beyond the JSON/KB."],
            ["Tool Registry (S16)", "Dispatch via TOOL_REGISTRY[tool] so adding tools takes zero loop edits.", "Do not write huge if/elif tool chains inside agent.py."],
            ["Trace Schema (S21-22)", "Every step logs 7 exact keys. Grader reads trace.jsonl directly.", "Never omit elapsed_ms or 'recovered' status keys."],
            ["Sprint Pacing (S28)", "14:15 tools pass; 15:15 loop runs; 16:30 clean Git freeze.", "Never allow .env or chroma_db binaries in Day 4 commits."],
        ],
        "demos": [
            ("Demo 1: Verify Starter Branch Baseline", "MANDATORY", [
                "PS> git checkout day-4 ; uv sync",
                "PS> uv run pytest capstone_*/test_tools.py -v",
                "# Expected: reference unit tests run cleanly",
            ]),
            ("Demo 2: Track 3 End-to-End Mock Run", "OPTIONAL (Morning)", [
                "PS> uv run python capstone_3_research/agent.py --mock-llm",
                "# Inspect trace.jsonl: Steps 1-5 -> status='recovered' -> out/research_report.md",
            ]),
        ],
        "faqs": [
            ["1", "Can two teams pick the same track?", "Yes. Each team builds in its own repository on Track 1, 2, or 3."],
            ["2", "How much starter code can we keep?", "Keep data/, ingest.py base, and tool stubs; you must implement and explain loop/quarantine/tests."],
            ["3", "Why --mock-llm during the sprint?", "Keeps offline testing fast and immune to Groq 429 rate limits when 60 students run loops."],
            ["4", "ModuleNotFoundError when running agent.py?", "Add empty __init__.py in capstone folder or run from repo root with -m."],
            ["5", "Where should reports save?", "Always under out/&lt;track&gt;_report.md relative to workdir."],
            ["6", "My tool crashes on 'NaN' string?", "Check isinstance(v, (int, float)) AND not math.isnan(float(v)) before appending valid."],
            ["7", "What if trace.jsonl is empty?", "Check while-loop appends dicts to trace[] and writes trace.jsonl after loop break."],
            ["8", "Should I commit capstone_memory/ before freeze?", "No! Delete runtime DBs, out/, and trace.jsonl before git commit."],
        ],
        "mistakes": [
            ["1", "KeyError reading JSON rows", "Raw dict['key'] access", "Replace with row.get('key', default) + key check"],
            ["2", "Relative path fails in test", "Run from inside capstone folder", "Pass workdir: Path explicitly to every tool"],
            ["3", "ImportError between scripts", "Missing __init__.py", "Touch empty __init__.py + try/except relative import"],
            ["4", "Report uses stale memory", "Hardcoded metrics in prompt", "Force read_file tool call before write_report"],
            ["5", "trace.jsonl lacks 'recovered'", "Set 'ok' without checking prior error", "Check any(e['status']=='error' for e in trace)"],
        ],
        "skip_list": [
            ["Cut 1st", "S3 (Why Modular Design)", "Covered implicitly in S5 & S16."],
            ["Cut 2nd", "S16 (Tool Registry Pattern)", "Point directly to TOOL_REGISTRY dict during walkthrough."],
            ["Cut 3rd", "S27 (Defensive Code)", "S26 covers SchemaError; reinforce S27 only if time allows."],
            ["NEVER CUT", "S6, S10-15, S21-25, S28", "Starter cmd, all 3 track specs, trace schema, pacing."],
        ],
        "answer_key_title": "Day 4 Milestones & Verification Commands",
        "answer_key_headers": ["Clock Time", "Sprint Milestone", "Verification Command"],
        "answer_key_rows": [
            ["14:15 PM", "ingest.py + 4 tools pass unit tests", "uv run pytest capstone_*/test_tools.py -v"],
            ["15:15 PM", "ReAct loop runs + trace.jsonl written", "uv run python capstone_*/agent.py --mock-llm"],
            ["16:00 PM", "Cross-session speedup verified", "Run twice -> check Run 2 step count < Run 1"],
            ["16:30 PM", "Working tree clean, zero secrets", "git status --short (no .env or DB binaries)"],
            ["16:45 PM", "CODE FREEZE — commit & push", "git commit -m 'Day 4 capstone freeze'"],
        ],
        "answer_key_widths": [65, 185, CONTENT_W - 250],
        "extras": [
            {
                "heading": "Day 4 Mentor Reference: Track Thresholds, Starter Boundaries & Triage",
                "blocks": [
                    {"type": "h2", "text": "Starter Code vs. Student-Written Work"},
                    {"type": "table", "headers": ["File", "Provided in day-4", "Student Responsibility"],
                     "widths": [135, 165, CONTENT_W - 300], "rows": [
                         ["capstone_*/data/*.json + .md", "Full baseline datasets & docs", "Read-only inputs (never alter baseline truth)"],
                         ["capstone_*/ingest.py", "Chunking + upsert template", "Ensure collection name & idempotent count"],
                         ["capstone_*/tools.py", "Stubs & path safety", "Implement NaN/type quarantine & hints"],
                         ["capstone_*/agent.py", "Skeleton CLI/LLM wrapper", "Wire ReAct loop, trace.jsonl, --mock-llm"],
                         ["capstone_*/test_tools.py", "Starter test layout", "Verify missing-file recovery & NaN quarantine"],
                     ]},
                    {"type": "h2", "text": "Track 1 (IoT Fleet) Ground Truth: fleet_telemetry.json"},
                    {"type": "table", "headers": ["node_id", "bus_v", "vds_peak_v", "temp_c", "Expected Verdict"],
                     "widths": [75, 55, 70, 55, CONTENT_W - 255], "rows": [
                         ["NODE-01", "24.1", "48.0", "46.2", "[OK] Within limits"],
                         ["NODE-02", "24.4", "108.5", "94.8", "[FLAG] vds > 100 V AND temp > 85 C"],
                         ["NODE-03", "23.9", "52.3", "49.0", "[OK] Within limits"],
                         ["NODE-04", "11.2", "31.0", "79.5", "[FLAG] bus_v < 18 V (brownout)"],
                     ]},
                    {"type": "h2", "text": "Track 2 (5G NR) Ground Truth: gnb_kpis.json"},
                    {"type": "table", "headers": ["cell_id", "prb_pct", "sinr_db", "bler_pct", "Expected Verdict"],
                     "widths": [80, 55, 55, 58, CONTENT_W - 248], "rows": [
                         ["GNB-BLR-01", "62.4", "18.2", "1.8", "[OK] Nominal Band n78"],
                         ["GNB-BLR-02", "94.1", "1.4", "14.6", "[FLAG] PRB > 85%, SINR < 3.0, BLER > 10%"],
                         ["GNB-BLR-03", "58.0", "16.5", "2.4", "[OK] Nominal Band n78"],
                     ]},
                    {"type": "h2", "text": "Track 3 (Research) Ground Truth: paper_abstracts.json"},
                    {"type": "table", "headers": ["paper_id", "latency_ms", "f1_score", "Expected Verdict"],
                     "widths": [95, 75, 70, CONTENT_W - 240], "rows": [
                         ["ECE-2025-101", "14.2", "0.94", "[QUALIFIED] latency <= 50 ms and F1 >= 0.85"],
                         ["ECE-2025-102", "480.0", "0.52", "[REJECTED] Fails both latency & F1 thresholds"],
                         ["ECE-2025-103", "22.8", "0.96", "[QUALIFIED] latency <= 50 ms and F1 >= 0.85"],
                     ]},
                    {"type": "h2", "text": "Mentor Debugging Flowchart (Do Not Type For Students)"},
                    {"type": "code", "title": "6-STEP MENTOR TRIAGE PROTOCOL", "lines": [
                        "Student: 'My agent is broken' -> Ask these questions in order:",
                        "1. 'Read the last line of the Python traceback aloud.'",
                        "2. ImportError?    -> Verify __init__.py exists & run from repo root.",
                        "3. FileNotFound?   -> Check cwd and whether data/ JSON exists.",
                        "4. KeyError/Value? -> Check .get() defaults & math.isnan() guard.",
                        "5. Empty trace?    -> Verify while-loop appends & saves trace.jsonl.",
                        "6. Failing test?   -> Run single test: uv run pytest <file>::<fn> -v",
                    ]},
                ],
            }
        ],
        "bridge_title": "END-OF-DAY BRIDGE TO DAY 5",
        "bridge_text": (
            "Announce at 16:45 PM: 'Freeze commits now. Tomorrow morning we inject unseen Batch B corrupt telemetry "
            "into your code, run the 100-point AST auto-grader, and begin 5-minute live viva defenses.'"
        ),
    },
    # ------------------------------------------------------------------ DAY 5
    {
        "day": 5,
        "slide_count": 34,
        "cover_title": "Day 5: Fault Injection,<br/>Auto-Grading &amp; Viva Defense",
        "cover_sub": "Instructor Confidentiality Guide: Batch B Datasets, Rubric &amp; Viva Bank",
        "timeline": [
            ["09:00-11:00", "120m", "1-7", "Chaos eng, 4-fault matrix, 3D sandbox video, data quality", "Play anim_fault_recovery (S5). Do NOT show Batch B JSON."],
            ["11:00-11:30", "30m", "8", "Morning Tea Break", "Prepare Batch B release for 11:30 session."],
            ["11:30-12:20", "50m", "9-16", "Release Batch B, run_all_tests.py, AST, rubric, grader CLI", "Unlock testing/unseen_benchmarks/ for students (or merge day-5)."],
            ["12:20-13:00", "40m", "—", "PRE-DEFENSE AUDIT: Students run run_all_tests.py & fix faults", "Run cohort batch grader while teams verify fixes."],
            ["13:00-14:00", "60m", "17", "Lunch Break", "Prepare projector terminal at 18pt+ font + score sheet."],
            ["14:00-14:30", "30m", "18-28", "What is a Viva, 5-min plan, senior habits, AST/cold restart", "Walk through exact viva scoring rules."],
            ["14:30-15:30", "60m", "—", "BATCH 1 LIVE DEFENSES (5 minutes per team)", "Ask 3 mandatory + 2 follow-up questions per team."],
            ["15:30-15:40", "10m", "29", "Rotation Break (Batch 1 Complete -> Batch 2 Ready)", "Tally Batch 1 leaderboard scores."],
            ["15:40-16:25", "45m", "—", "BATCH 2 LIVE DEFENSES (5 minutes per team)", "Maintain strict 5-min timer per team."],
            ["16:25-16:45", "20m", "30-34", "What Next (MCP/Teams), 5-day journey, certificates & wrap", "Announce A+/A/B certificate tiers & close."],
        ],
        "checklist": [
            "[ ] Branch day-5 & auto-evaluator tested cleanly on instructor machine",
            "[ ] testing/unseen_benchmarks/ contains all 4 Batch B files",
            "[ ] Evaluator verified on clean reference repo: 100 / 100 Grade A+",
            "[ ] Printed viva team rotation schedule (5 min slots)",
            "[ ] Projector terminal font set >= 18pt for viva visibility",
            "[ ] Cohort USB backup ready in case campus Wi-Fi drops",
        ],
        "theory": [
            {
                "title": "1. Chaos Engineering &amp; Fault Injection Principles",
                "summary": (
                    "Happy-path testing verifies author assumptions, not system robustness. Inspired by Netflix Chaos Monkey, "
                    "Day 5 injects realistic operational disturbances to measure graceful degradation under stress."
                ),
                "points": [
                    "<b>Four Orthogonal Fault Axes:</b> (1) Renamed/missing file path testing path discovery, (2) Corrupt syntax or NaN fields testing schema quarantine, (3) Cold subprocess restarts testing disk persistence, and (4) Unsolvable goals verifying loop caps.",
                    "<b>Graceful Degradation Contract:</b> When 1 out of 4 telemetry records fails validation, tools must quarantine the broken row and continue auditing the remaining 3 valid devices cleanly.",
                ],
            },
            {
                "title": "2. Production Data Quality &amp; IEEE-754 'NaN' Traps",
                "summary": (
                    "Real-world IoT and 5G logs contain 10-30% defective records from RF dropouts, ADC rails, and truncated "
                    "packets. Naive Python type checks silently fail on IEEE-754 floating-point NaN."
                ),
                "points": [
                    "<b>Why Naive Float Checks Fail:</b> Calling <i>float('NaN')</i> succeeds without raising ValueError, and any ordering comparison (&gt;, &lt;, ==) against NaN evaluates to False — silently hiding faults!",
                    "<b>Mandatory Defensive Pattern:</b> Guard every numeric metric with <i>isinstance(v, (int, float)) and not math.isnan(float(v))</i> (plus bool exclusion if strict) and wrap <i>json.loads()</i> inside try/except JSONDecodeError.",
                ],
                "formula": {
                    "latex": r"$\mathrm{NaN} == \mathrm{NaN} \to \mathrm{False} \qquad \mathrm{NaN} > 100 \to \mathrm{False} \qquad \mathrm{isnan}(\mathrm{NaN}) \to \mathrm{True}$",
                    "expr": "float('nan') == float('nan') -&gt; False  |  nan &gt; 100.0 -&gt; False  |  math.isnan(nan) -&gt; True",
                    "terms": [
                        ["float('nan')", "IEEE-754 Quiet Not-a-Number bit pattern accepted by float() without ValueError."],
                        ["Unordered compare", "Per IEEE-754 standard, every &lt;, &lt;=, &gt;, &gt;=, == comparison with NaN returns False."],
                        ["isinstance(v, (int,float))", "Rejects string payloads like 'NaN' or null (None) before math checks."],
                        ["math.isnan(float(v))", "Explicit exponent/mantissa check returning True iff v is IEEE-754 NaN."],
                    ],
                    "example": (
                        "Batch B trap: BATCHB-02 has bus_v='NaN'. Without isinstance() + math.isnan(), brownout test "
                        "'float(bus_v) &lt; 18.0' evaluates to False and skips the defect instead of quarantining it!"
                    ),
                },
            },
            {
                "title": "3. Abstract Syntax Trees (AST) &amp; Automated Grader Scoring",
                "summary": (
                    "Understand exact evaluator internals before answering student score disputes during pre-defense audit."
                ),
                "points": [
                    "<b>Why Static AST Before Execution:</b> Parsing <i>agent.py</i> with <i>ast.parse()</i> builds an immutable syntax tree (Module -&gt; FunctionDef -&gt; While/For -&gt; Call) in milliseconds, exposing hardcoded linear print() scripts.",
                    "<b>Zero-Trust Security Audit:</b> Tracked git blobs and working trees are scanned for <i>.env</i> files and <i>'gsk_'</i> prefixes before awarding hygiene points.",
                    "<b>Partial Credit Mechanics:</b> Evaluator separates loop structure, recovery, RAG, memory speedup, and hygiene cleanly into deterministic sub-checks totaling 100 points.",
                ],
                "formula": {
                    "latex": r"$\mathrm{Total} = S_{\mathrm{RAG}}(25) + S_{\mathrm{ReAct}}(20) + S_{\mathrm{Fault}}(25) + S_{\mathrm{Mem}}(20) + S_{\mathrm{Hygiene}}(10)$",
                    "expr": "Total = S<sub>RAG</sub>(25) + S<sub>ReAct</sub>(20) + S<sub>Fault</sub>(25) + S<sub>Mem</sub>(20) + S<sub>Hygiene</sub>(10)",
                    "terms": [
                        ["S<sub>RAG</sub> (0-25)", "12 pts for idempotent collection.upsert() + 13 pts for semantic spec hit &amp; citation."],
                        ["S<sub>ReAct</sub> (0-20)", "20 pts if AST finds while/for loop dispatching tools + valid trace; 0 pts if linear script."],
                        ["S<sub>Fault</sub> (0-25)", "13 pts self-healing missing path + 12 pts quarantining NaN &amp; corrupt JSON without crash."],
                        ["S<sub>Mem</sub> (0-20)", "20 pts if cold-restart Run 2 cuts steps via AAR; 10 pts if recalled without step speedup."],
                        ["S<sub>Hygiene</sub> (0-10)", "6 pts zero .env/gsk_ leaks + 4 pts clean README.md &amp; pyproject.toml."],
                    ],
                    "example": (
                        "AST tree rule check: Python inspects isinstance(node, (ast.While, ast.For)) inside run_agent() "
                        "containing nested ast.Call nodes — comments or print('Step 1') never satisfy the tree check."
                    ),
                },
            },
            {
                "title": "4. Subprocess Cold-Restart Persistence &amp; Technical Viva Pedagogy",
                "summary": (
                    "Combine black-box automated scoring with live 5-minute oral examination to confirm every student "
                    "genuinely understands their team's architecture."
                ),
                "points": [
                    "<b>OS Process Isolation Proof:</b> Launching Run 1 and Run 2 in fresh Python subprocesses clears all heap objects, module globals, and in-memory caches; only SQLite/parquet data persisted inside PersistentClient survives.",
                    "<b>5-Minute Viva Discipline:</b> Do not let students talk through slides — force live terminal execution on Batch B, live trace.jsonl narration, and direct line-by-line code navigation.",
                ],
            },
        ],
        "talking_points": [
            ["Chaos Eng (S3)", "Breaking your own code before evaluators do is senior engineering.", "Keep Batch B answers private until demo run."],
            ["Batch B &amp; Quarantine (S6-9)", "Expect NaN strings, extreme faults, and broken JSON syntax in unseen files.", "Do not project Batch B file contents before testing."],
            ["Test Harness (S10)", "Run testing/run_all_tests.py to execute all 9 suites in one command.", "Clarify that pytest expands Windows globs internally."],
            ["Auto-Grader (S11-14)", "AST inspects agent.py first; zero loop or leaked gsk_ = auto-deduction.", "Do not share evaluator bypass quirks."],
            ["What is a Viva (S18-19)", "No slides! Project terminal, run Batch B, read trace.jsonl live.", "Reward code comprehension over jargon."],
            ["Viva Habits (S20)", "Calmly read [Step 2] observation dicts before editing any code.", "Interrupt rambling and ask for exact line numbers."],
            ["Cold Restarts (S24-25)", "Grader spawns fresh Python processes; RAM variables vanish on exit.", "Never accept RAM-cached globals as episodic memory."],
            ["Day Releases &amp; Close (S30-34)", "Export student day ZIPs via auto-evaluator release-day CLI only.", "Removed Day Releases from student slides (D2.5) to prevent clutter."],
        ],
        "demos": [
            ("Demo 1: Master 9-Suite Verification", "MANDATORY", [
                "PS> uv run python testing/run_all_tests.py",
                "# Expected: Summary: 9/9 suites passed.",
            ]),
            ("Demo 2: Evaluator CLI (Single Repo & Cohort CSV)", "MANDATORY — INSTRUCTOR TERMINAL", [
                "PS> uv run python -m evaluator.cli evaluate C:\\path\\to\\repo --out reports/",
                "PS> uv run python -m evaluator.cli batch C:\\path\\to\\submissions --out reports/leaderboard.csv",
                "# Daily branch ZIP export (instructor-only command):",
                "PS> uv run python -m evaluator.cli release-day --repo . --branch day-1 --out day-1.zip",
            ]),
        ],
        "faqs": [
            ["1", "Does the grader use my live Groq API?", "No. Batch grading runs deterministic offline mode so API rate limits never penalize students."],
            ["2", "Why did AST say ReAct Loop = 0/20?", "agent.py lacks a real while/for loop executing registered tools."],
            ["3", "How do I test corrupt_malformed.json?", "Pass it to read_telemetry/read_kpis; return {'ok': False, 'error': 'JSONDecodeError'} cleanly."],
            ["4", "Why check git ls-files on Day 5?", "Leaked .env, gsk_ strings, or committed chroma_db/ triggers hygiene deductions."],
            ["5", "What happens on cold-restart test?", "Evaluator launches separate Python subprocesses; RAM-only globals fail."],
            ["6", "My Windows PowerShell didn't expand *.py?", "pytest expands 'capstone_*/test_tools.py' internally; run via pytest, not raw dir."],
            ["7", "Can students resubmit if < 60?", "Offer same-day remediation window after Batch 2 before issuing certificates."],
            ["8", "What qualifies for Distinction?", "90-100 points overall + passing live oral trace walkthrough."],
        ],
        "mistakes": [
            ["1", "Crash on corrupt_malformed.json", "json.loads() outside try/except", "Wrap json.loads() in try/except returning error dict"],
            ["2", "Crash on bus_v: 'NaN'", "Cast float('NaN') passes float()", "Check isinstance(v,(int,float)) and not math.isnan(float(v))"],
            ["3", "0/20 AST loop deduction", "Linear step1(); step2() script", "Refactor into bounded for/while control loop"],
            ["4", "-6 Security Fail deduction", "Committed .env or gsk_ string", "git rm --cached .env ; rotate Groq key cleanly"],
            ["5", "10/20 Memory half-credit", "Recalled AAR without step drop", "Verify Run 2 skips initial blind guess on Step 1"],
        ],
        "skip_list": [
            ["Cut 1st", "S30 (What Next Landscape)", "Summarize in closing 2 minutes."],
            ["Cut 2nd", "S25 (Persistence Theory)", "Redundant if S24 Cold Restarts explained clearly."],
            ["Cut 3rd", "S28 (Career Impact)", "Mention briefly during Git portfolio S27."],
            ["NEVER CUT", "S13-22 (Rubric, Viva Format, Live Runs)", "Core Day 5 grading & defense protocol."],
        ],
        "answer_key_title": "Day 5 Answer Key — Certificate & Grade Thresholds",
        "answer_key_headers": ["Grade", "Score Range", "Certificate Tier"],
        "answer_key_rows": [
            ["A+", "90 - 100", "Distinction in Agentic AI Engineering"],
            ["A", "80 - 89", "Excellence in Agentic AI Engineering"],
            ["B", "70 - 79", "Completion of Agentic AI Engineering"],
            ["C", "60 - 69", "Participation in Agentic AI Engineering"],
            ["FAIL", "< 60", "No certificate — offer controlled resubmission window"],
        ],
        "answer_key_widths": [55, 85, CONTENT_W - 140],
        "extras": [
            {
                "heading": "Day 5 Confidential Reference: Batch B Faults, Rubric &amp; Viva Bank",
                "callout": (
                    "INSTRUCTOR EYES ONLY — DO NOT PROJECT BEFORE DEFENSE",
                    "Keep exact Batch B fault rows hidden until teams begin live testing. These datasets intentionally "
                    "mix valid rows, NaN strings, extreme threshold violations, and broken JSON syntax.",
                    "#B91C1C", "#FEF2F2",
                ),
                "blocks": [
                    {"type": "h2", "text": "Unseen Batch B Ground Truth (iot_batch_b.json, gnb_batch_b.json, corrupt_malformed.json)"},
                    {"type": "table", "headers": ["File / Record", "Injected Fault", "Required Agent Behavior"],
                     "widths": [135, 165, CONTENT_W - 300], "rows": [
                         ["iot_batch_b: BATCHB-01", "None (clean baseline)", "Analyze normally, zero flags"],
                         ["iot_batch_b: BATCHB-02", "bus_v: 'NaN' (string)", "Quarantine as NaN_or_non_numeric"],
                         ["iot_batch_b: BATCHB-03", "vds=118.2 V, temp=112.4 C", "Flag both MOSFET Vds > 100 V and Temp > 85 C"],
                         ["iot_batch_b: Row 4", "{'bad_key': 'malformed_row'}", "Quarantine as malformed_row (no node_id)"],
                         ["gnb_batch_b: GNB-B01", "None (clean baseline)", "Analyze normally"],
                         ["gnb_batch_b: GNB-B02", "PRB=96.2, SINR=-1.2, BLER=18.4", "Flag all 3 degraded KPI metrics"],
                         ["gnb_batch_b: GNB-B03", "prb_pct: 'NaN' (string)", "Quarantine safely"],
                         ["corrupt_malformed.json", "{[corrupt_json_payload...", "Return ok=False, error='JSONDecodeError' (0 crashes)"],
                     ]},
                    {"type": "h2", "text": "100-Point Automated Grader Rubric Breakdown"},
                    {"type": "table", "headers": ["Category", "Max", "Automated Grader Checks", "Most Common Deduction"],
                     "widths": [90, 34, 215, CONTENT_W - 339], "rows": [
                         ["RAG Pipeline", "25", "Idempotent upsert (12) + semantic target retrieval (13)", "Using .add() -> duplicates"],
                         ["ReAct Loop", "20", "AST detects real while/for loop in agent.py (20) / partial trace (10)", "Hardcoded linear script (0/20)"],
                         ["Fault Recovery", "25", "Self-heals missing path (13) + quarantines NaN/corrupt JSON (12)", "Uncaught JSON/float crash"],
                         ["Episodic Memory", "20", "Cold-restart Run 2 step reduction (20) / recall no speedup (10)", "Non-persistent RAM Client()"],
                         ["Hygiene & Docs", "10", "Zero .env or gsk_ leaks (6) + README.md & pyproject.toml (4)", "Committed .env (-6)"],
                     ]},
                    {"type": "h2", "text": "5-Minute Viva Defense Question Bank"},
                    {"type": "bullets", "items": [
                        "<b>[Mandatory 1]</b> Name your 4 tools and explain the JSON dict returned by each.",
                        "<b>[Mandatory 2]</b> Run Batch B right now on the projector and walk me through trace.jsonl.",
                        "<b>[Mandatory 3]</b> Show the exact lines where FileNotFoundError or JSONDecodeError is caught.",
                        "<b>[Follow-up 4]</b> Why max_distance=1.65? What fails at 0.5 or 2.5?",
                        "<b>[Follow-up 5]</b> What breaks if max_steps is removed?",
                        "<b>[Follow-up 6]</b> Print your stored AAR lesson from ChromaDB. Why is it 1 sentence?",
                        "<b>[Follow-up 7]</b> Prove how _resolve_safe() blocks a '../../.env' attack.",
                        "<b>[Follow-up 8]</b> Explain Semantic vs Episodic Chroma collections in your own words.",
                    ]},
                    {"type": "code", "title": "PERFECT 100/100 EVALUATOR SUMMARY REFERENCE", "lines": [
                        "RAG Pipeline: 25/25  |  ReAct Loop: 20/20  |  Fault Recovery: 25/25",
                        "Episodic Memory: 20/20  |  Hygiene & Docs: 10/10",
                        "TOTAL: 100 / 100  |  GRADE: A+  |  DEDUCTIONS: (none)",
                    ]},
                ],
            }
        ],
        "bridge_title": "PROGRAM CLOSING NOTE",
        "bridge_text": (
            "Congratulate the cohort: every team moved from single-turn prompts to verifiable, fault-tolerant "
            "Python systems ready for VTU final-year hardware/telecom projects and technical interviews."
        ),
    },
]


def main() -> None:
    built = [render_day_pdf(spec) for spec in DAY_SPECS]
    print(f"Built {len(built)} Instructor Preparation PDFs in {OUT_DIR}:")
    for p in built:
        print(f" - {p.name} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
