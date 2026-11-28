"""
build_comprehensive_a4_vap_pdfs.py
Generates two comprehensive, textbook-grade A4 PDF engineering handbooks for the
5-Day Value Added Program (VAP) at Acharya Institute of Technology:
1. VAP_Student_Workshop_Guide.pdf (~20-24 A4 pages)
2. VAP_Instructor_Preparation_Guide.pdf (~18-22 A4 pages)

Design & Formatting Standards:
- Page Size: A4 (595.27 x 841.89 pt), 54 pt left/right margins (printable width 487 pt)
- Minimalist theme: white background (#FFFFFF), deep blue (#1E3A8A), tech orange (#EA580C)
- Comfortable, readable typography: Body 10.5pt/15pt, H1 16.5pt, H2 13pt, Code 8.2pt/11pt
- Splittable multi-row code blocks so pages flow smoothly with zero large blank gaps
- Natural multi-page chapters (PageBreak only at major chapter starts)
- Exact aspect-ratio preservation on all 300-DPI non-overlapping block diagrams
- Clean, minimal cover page: Title, Cover Graphic, Department of ECE, Acharya Institute of Technology
- ASD-STE100 Simplified Technical English, active voice, zero emojis
- Consistent running header/footer pairs on pages 2+ with accurate "Page X of Y" numbering
"""

import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

IMAGES_DIR = r"C:\Users\lapto\Desktop\demo\BEN\VAP\images"
PAGE_WIDTH, PAGE_HEIGHT = A4
CONTENT_W = 486.0  # 595.27 - 2*54 = 487.27 pt


# ----------------------------------------------------------------------
# Two-Pass A4 Numbered Canvas for Running Headers and Footers
# ----------------------------------------------------------------------
class A4NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.doc_title = getattr(self, "doc_title", "VALUE ADDED PROGRAM GUIDE")
        self.doc_subtitle = getattr(self, "doc_subtitle", "ECE 5TH SEMESTER | ACHARYA INSTITUTE OF TECHNOLOGY")

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        pw, ph = A4

        # Top running header
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(54, ph - 34, self.doc_title.upper())

        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(pw - 54, ph - 34, self.doc_subtitle.upper())

        # Header divider line with orange left accent bar
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, ph - 41, pw - 54, ph - 41)

        self.setStrokeColor(colors.HexColor("#EA580C"))
        self.setLineWidth(1.8)
        self.line(54, ph - 41, 120, ph - 41)

        # Bottom running footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 44, pw - 54, 44)

        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 30, "DEPARTMENT OF ECE  |  ACHARYA INSTITUTE OF TECHNOLOGY")

        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawRightString(pw - 54, 30, f"Page {self._pageNumber} of {total_pages}")

        self.restoreState()


def get_a4_canvas_class(doc_title, doc_subtitle):
    class CustomA4Canvas(A4NumberedCanvas):
        def __init__(self, *args, **kwargs):
            self.doc_title = doc_title
            self.doc_subtitle = doc_subtitle
            super().__init__(*args, **kwargs)
    return CustomA4Canvas


# ----------------------------------------------------------------------
# Typography & Styles (Comfortable Textbook Scale)
# ----------------------------------------------------------------------
def setup_styles():
    base = getSampleStyleSheet()
    return {
        "CoverProgram": ParagraphStyle(
            "CoverProgram", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=12, leading=16,
            textColor=colors.HexColor("#EA580C"), alignment=TA_CENTER, spaceAfter=10,
        ),
        "CoverTitle": ParagraphStyle(
            "CoverTitle", parent=base["Title"],
            fontName="Helvetica-Bold", fontSize=24, leading=30,
            textColor=colors.HexColor("#1E3A8A"), alignment=TA_CENTER, spaceAfter=10,
        ),
        "CoverSubtitle": ParagraphStyle(
            "CoverSubtitle", parent=base["Normal"],
            fontName="Helvetica", fontSize=13, leading=18,
            textColor=colors.HexColor("#475569"), alignment=TA_CENTER, spaceAfter=18,
        ),
        "CoverDept": ParagraphStyle(
            "CoverDept", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=13, leading=18,
            textColor=colors.HexColor("#334155"), alignment=TA_CENTER, spaceAfter=6,
        ),
        "CoverCollege": ParagraphStyle(
            "CoverCollege", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=16, leading=21,
            textColor=colors.HexColor("#1E3A8A"), alignment=TA_CENTER, spaceAfter=8,
        ),
        "CoverYear": ParagraphStyle(
            "CoverYear", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=10.5, leading=14,
            textColor=colors.HexColor("#EA580C"), alignment=TA_CENTER,
        ),
        "ChapterTag": ParagraphStyle(
            "ChapterTag", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=9.5, leading=12,
            textColor=colors.HexColor("#EA580C"), spaceBefore=0, spaceAfter=2,
            keepWithNext=True,
        ),
        "H1": ParagraphStyle(
            "H1", parent=base["Heading1"],
            fontName="Helvetica-Bold", fontSize=16.5, leading=21,
            textColor=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=6,
            keepWithNext=True,
        ),
        "H2": ParagraphStyle(
            "H2", parent=base["Heading2"],
            fontName="Helvetica-Bold", fontSize=13, leading=17,
            textColor=colors.HexColor("#EA580C"), spaceBefore=12, spaceAfter=5,
            keepWithNext=True,
        ),
        "H3": ParagraphStyle(
            "H3", parent=base["Heading3"],
            fontName="Helvetica-Bold", fontSize=11, leading=14.5,
            textColor=colors.HexColor("#0F172A"), spaceBefore=9, spaceAfter=3,
            keepWithNext=True,
        ),
        "Body": ParagraphStyle(
            "Body", parent=base["BodyText"],
            fontName="Helvetica", fontSize=10.5, leading=15.0,
            textColor=colors.HexColor("#1E293B"), spaceAfter=7, alignment=TA_LEFT,
        ),
        "Bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"],
            fontName="Helvetica", fontSize=10.2, leading=14.5,
            textColor=colors.HexColor("#1E293B"), leftIndent=16, firstLineIndent=-10, spaceAfter=4,
        ),
        "Caption": ParagraphStyle(
            "Caption", parent=base["Normal"],
            fontName="Helvetica-Oblique", fontSize=9.0, leading=12.5,
            textColor=colors.HexColor("#475569"), alignment=TA_CENTER, spaceBefore=3, spaceAfter=10,
        ),
        "CodeTitle": ParagraphStyle(
            "CodeTitle", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=9.0, leading=12,
            textColor=colors.HexColor("#1E3A8A"),
        ),
        "CodeLine": ParagraphStyle(
            "CodeLine", parent=base["Normal"],
            fontName="Courier", fontSize=8.0, leading=10.5,
            textColor=colors.HexColor("#0F172A"),
        ),
        "CalloutTitle": ParagraphStyle(
            "CalloutTitle", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=10.2, leading=14,
            textColor=colors.HexColor("#1E3A8A"), spaceAfter=4,
        ),
        "CalloutText": ParagraphStyle(
            "CalloutText", parent=base["Normal"],
            fontName="Helvetica", fontSize=9.8, leading=13.8,
            textColor=colors.HexColor("#1E293B"),
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=9.0, leading=12.0,
            textColor=colors.HexColor("#FFFFFF"), alignment=TA_LEFT,
        ),
        "TableCell": ParagraphStyle(
            "TableCell", parent=base["Normal"],
            fontName="Helvetica", fontSize=8.8, leading=12.0,
            textColor=colors.HexColor("#1E293B"), alignment=TA_LEFT,
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBold", parent=base["Normal"],
            fontName="Helvetica-Bold", fontSize=8.8, leading=12.0,
            textColor=colors.HexColor("#0F172A"), alignment=TA_LEFT,
        ),
    }


# ----------------------------------------------------------------------
# Reusable Layout Components
# ----------------------------------------------------------------------
def add_chapter_header(story, chapter_num: str, title: str, styles):
    story.append(Paragraph(chapter_num.upper(), styles["ChapterTag"]))
    story.append(Paragraph(title, styles["H1"]))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=10))


def make_callout(title: str, text: str, styles, border_color="#1E3A8A", bg_color="#F8FAFC", width=CONTENT_W):
    rows = []
    if title:
        c_title = ParagraphStyle("CT_" + border_color, parent=styles["CalloutTitle"], textColor=colors.HexColor(border_color))
        rows.append([Paragraph(title, c_title)])
    rows.append([Paragraph(text, styles["CalloutText"])])

    t = Table(rows, colWidths=[width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg_color)),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
        ("LINELEFT", (0, 0), (-1, -1), 3.5, colors.HexColor(border_color)),
        ("TOPPADDING", (0, 0), (-1, 0), 7),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
        ("TOPPADDING", (0, 1), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -2), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def make_code_box(title: str, code_lines: list[str], styles, width=CONTENT_W):
    """Multi-row splittable code box: breaks gracefully across A4 pages without leaving blank gaps."""
    rows = []
    if title:
        rows.append([Paragraph(f"<b>{title}</b>", styles["CodeTitle"])])

    for line in code_lines:
        esc = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace(" ", "&nbsp;")
        )
        if esc == "":
            esc = "&nbsp;"
        rows.append([Paragraph(esc, styles["CodeLine"])])

    repeat = 1 if title else 0
    t = Table(rows, colWidths=[width], repeatRows=repeat)
    ts = [
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("LINEBEFORE", (0, 0), (0, -1), 3.0, colors.HexColor("#EA580C")),
        ("LINEAFTER", (-1, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, colors.HexColor("#E2E8F0")),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]
    if title:
        ts.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EFF6FF")))
        ts.append(("TOPPADDING", (0, 0), (-1, 0), 5))
        ts.append(("BOTTOMPADDING", (0, 0), (-1, 0), 5))
        ts.append(("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.HexColor("#CBD5E1")))
        if len(rows) > 1:
            ts.append(("TOPPADDING", (0, 1), (-1, 1), 5))
    else:
        ts.append(("TOPPADDING", (0, 0), (-1, 0), 5))
    ts.append(("BOTTOMPADDING", (0, -1), (-1, -1), 5))

    t.setStyle(TableStyle(ts))
    return t


def make_table(headers: list[str], rows: list[list[str]], col_widths: list[float], styles, header_bg="#1E3A8A"):
    data = [[Paragraph(h, styles["TableHeader"]) for h in headers]]
    for row in rows:
        data.append([
            Paragraph(cell, styles["TableCellBold"] if c_idx == 0 else styles["TableCell"])
            for c_idx, cell in enumerate(row)
        ])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    ts = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg)),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            ts.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F8FAFC")))
    t.setStyle(TableStyle(ts))
    return t


def make_diagram(image_name: str, caption: str, styles, max_width=480.0):
    """Embed image preserving exact native aspect ratio so zero distortion occurs."""
    img_path = os.path.join(IMAGES_DIR, image_name)
    if not os.path.exists(img_path):
        return []
    with PILImage.open(img_path) as im:
        w_px, h_px = im.size
    height = max_width * (h_px / w_px)
    img = Image(img_path, width=max_width, height=height)
    img.hAlign = "CENTER"
    items = [Spacer(1, 6), img]
    if caption:
        items.append(Paragraph(caption, styles["Caption"]))
    return items


def build_cover_page(story, title_html: str, subtitle_text: str, year_text: str, styles):
    """Minimal, prestigious cover page: Title, Cover Graphic, Department of ECE, Acharya Institute of Technology."""
    top_bar = Table([["", ""]], colWidths=[110, CONTENT_W - 110])
    top_bar.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (0, 0), 4.5, colors.HexColor("#EA580C")),
        ("LINEBELOW", (1, 0), (1, 0), 4.5, colors.HexColor("#1E3A8A")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(Spacer(1, 18))
    story.append(top_bar)
    story.append(Spacer(1, 32))

    story.append(Paragraph("5-DAY VALUE ADDED PROGRAM (VAP)", styles["CoverProgram"]))
    story.append(Paragraph(title_html, styles["CoverTitle"]))
    story.append(Paragraph(subtitle_text, styles["CoverSubtitle"]))
    story.append(Spacer(1, 18))

    # Preserve exact aspect ratio of cover_graphic.png
    img_path = os.path.join(IMAGES_DIR, "cover_graphic.png")
    with PILImage.open(img_path) as im:
        w_px, h_px = im.size
    w_pt = 472.0
    h_pt = w_pt * (h_px / w_px)
    cover_img = Image(img_path, width=w_pt, height=h_pt)
    cover_img.hAlign = "CENTER"
    story.append(cover_img)

    story.append(Spacer(1, 48))
    story.append(HRFlowable(width="55%", thickness=1.2, color=colors.HexColor("#CBD5E1"), hAlign="CENTER", spaceAfter=18))
    story.append(Paragraph("Department of Electronics and Communication Engineering", styles["CoverDept"]))
    story.append(Paragraph("Acharya Institute of Technology", styles["CoverCollege"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(year_text, styles["CoverYear"]))
    story.append(PageBreak())


# ======================================================================
# DOCUMENT 1: STUDENT WORKSHOP HANDBOOK (A4, MULTI-PAGE CHAPTERS)
# ======================================================================
def build_student_guide(output_path: str):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=54, rightMargin=54, topMargin=56, bottomMargin=54,
    )
    styles = setup_styles()
    story = []

    # -------------------- COVER PAGE --------------------
    build_cover_page(
        story,
        "Engineering Autonomous Agentic AI<br/>Systems with Vector RAG Memory",
        "Comprehensive Student Engineering Handbook &amp; Laboratory Manual",
        "ECE 5th Semester  |  Academic Year 2026 - 2027",
        styles,
    )

    # -------------------- CHAPTER 1: SYLLABUS & ROADMAP --------------------
    add_chapter_header(story, "Chapter 1", "Course Overview, Syllabus & 5-Day Roadmap", styles)

    story.append(Paragraph(
        "This 5-day Value Added Program (VAP) trains 5th-semester Electronics and Communication Engineering (ECE) "
        "students to build autonomous Agentic AI systems from first principles in Python. Most short workshops teach "
        "surface-level prompt templates or drag-and-drop wrappers that break in production. This course takes a "
        "systems engineering approach: students build every component directly against standard REST APIs and local "
        "vector indexes, gaining architectural clarity that transfers directly to final-year VTU projects, "
        "embedded automation, telecom diagnostics, and technical job interviews.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "Students complete two distinct software engineering projects across the five days. In Project 1 (Days 1 and 2), "
        "the instructor first demonstrates a complete working Vector Retrieval-Augmented Generation (RAG) system, "
        "and students then build their own end-to-end RAG pipeline using ChromaDB and Groq Cloud API. "
        "Day 3 bridges passive retrieval to true autonomy. In Project 2 (Days 4 and 5), students work independently "
        "without instructor code help to design, build, stress-test, and defend an autonomous Agentic AI system "
        "that uses Vector RAG as persistent episodic memory.",
        styles["Body"],
    ))

    story.append(make_callout(
        "FIVE MEASURABLE ENGINEERING COMPETENCIES",
        "<b>1. Architectural Clarity:</b> Separate passive single-turn tool use from autonomous goal-seeking agents.<br/>"
        "<b>2. Vector Geometry &amp; Indexing:</b> Apply dense embeddings, cosine similarity, sentence chunking, and HNSW indexing.<br/>"
        "<b>3. Deterministic Tool Calling:</b> Design JSON Schema function contracts and dynamic Python tool registries.<br/>"
        "<b>4. Autonomous Control Loops:</b> Implement pure-Python ReAct while-loops with step budgets and exception self-healing.<br/>"
        "<b>5. Dual-Memory Engineering:</b> Fuse short-term rolling scratchpads with persistent ChromaDB episodic memory and After Action Review (AAR).",
        styles, border_color="#1E3A8A", bg_color="#EFF6FF",
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1.1 Detailed 5-Day Program Timetable", styles["H2"]))
    story.append(Paragraph(
        "Each workshop day runs from 09:30 to 17:00 across three structured sessions: two theory-focused morning "
        "sessions (09:30 - 11:00 and 11:30 - 13:00) followed by a dedicated three-hour hands-on working session "
        "(14:00 - 17:00) with GitHub milestone checkpoints.",
        styles["Body"],
    ))

    sched_headers = ["Day & Session", "Technical Module", "Focus & Deliverables / Checkpoints"]
    sched_rows = [
        ["Day 1 · Session 1\n(09:30 - 11:00)", "Theory: Orientation & Mental Model Reset",
         "Baseline skill survey, 5-day roadmap, dismantling the 'email summarizer' fallacy, and Levels 0-4 autonomy spectrum."],
        ["Day 1 · Session 2\n(11:30 - 13:00)", "Theory: Vector Math, Chunking & RAG Demo",
         "Embedding spaces, cosine similarity derivation, chunk overlap science, HNSW indexing, and instructor live RAG demo."],
        ["Day 1 · Session 3\n(14:00 - 17:00)", "Working: Environment Setup, API & Chroma Lab",
         "Install Python 3.13 & uv, configure .env secrets & .gitignore, run verify.py, and build first chroma_demo.py sandbox."],
        ["Day 2 · Session 1\n(09:30 - 11:00)", "Theory: Project 1 Ingestion & Chunking",
         "Document loaders, sentence-aware chunking with overlap, metadata tagging, and idempotent ChromaDB upsert design."],
        ["Day 2 · Session 2\n(11:30 - 13:00)", "Theory: Semantic Retrieval & Prompt Grounding",
         "Top-k cosine similarity, distance thresholds, anti-hallucination system prompts, citation rules, and Groq API schema."],
        ["Day 2 · Session 3\n(14:00 - 17:00)", "Working: Build Project 1 & GitHub Push",
         "Implement ingest.py + query.py end-to-end, verify in-domain/out-of-domain/synonym test cases, and push Project 1."],
        ["Day 3 · Session 1\n(09:30 - 11:00)", "Theory: ReAct Loop & JSON Tool Calling",
         "Think-Act-Observe-Reflect control flow, OpenAI/Groq JSON tool schemas, @register_tool, budgets & try/except self-healing."],
        ["Day 3 · Session 2\n(11:30 - 13:00)", "Theory: Dual Memory, AAR & Capstone Briefing",
         "Short-term scratchpad vs. ChromaDB episodic memory, After Action Review reflection, and Capstone Track disclosure."],
        ["Day 3 · Session 3\n(14:00 - 17:00)", "Working: Build Agent, Memory & AAR Core",
         "Implement tools.py, agent.py while-loop, memory.py (store/recall), and aar_engine.py; validate cross-session recall."],
        ["Day 4 · Session 1\n(09:30 - 11:00)", "Theory/Standup: Capstone Declaration",
         "Unassisted sprint kickoff. Declare Problem Statement (IoT, 5G Telecom, or Literature Survey) and block diagram."],
        ["Day 4 · Session 2\n(11:30 - 13:00)", "Theory/Design: Memory & Tool Contracts",
         "Define ChromaDB domain chunk schema, 4 typed JSON tool contracts, path safety rules, and failure-recovery edge cases."],
        ["Day 4 · Session 3\n(14:00 - 17:00)", "Working: Capstone Build Sprint & Git Push",
         "Ingest mock datasets, code all 4 tools and ReAct loop unassisted, pass >=3 tool-call smoke test, and push to GitHub."],
        ["Day 5 · Session 1\n(09:30 - 11:00)", "Theory/Audit: Verification & Viva Prep",
         "Fault-injection test plan, 100-point rubric audit, zero-point pitfalls check, and oral defense walkthrough prep."],
        ["Day 5 · Session 2\n(11:30 - 13:00)", "Pre-Defense Working: Hardening & Docs",
         "Test corrupt inputs and cross-session memory, finalize trace.jsonl, .env.example & README.md; 1:00 PM final Git push."],
        ["Day 5 · Session 3\n(14:00 - 17:00)", "Working/Defense: Live Evaluation & Viva",
         "Execute agent live against unseen evaluator benchmark, code walkthrough, oral viva defense, and program certification."],
    ]
    story.append(make_table(sched_headers, sched_rows, [96, 150, 240], styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.2 Daily Operating Schedule & Grading Split", styles["H2"]))
    story.append(Paragraph(
        "The workshop operates on a fixed three-session daily rhythm: <b>09:30 - 11:00</b> Morning Theory Session 1, "
        "<b>11:00 - 11:30</b> Morning Break, <b>11:30 - 13:00</b> Morning Theory Session 2, <b>13:00 - 14:00</b> Lunch Break, "
        "and <b>14:00 - 17:00</b> Afternoon Hands-On Working Session (Implementation, Verification &amp; Git Push). "
        "Assessment totals <b>100 points</b>: <b>30 points</b> for Project 1 (Basic Vector RAG) and <b>70 points</b> for "
        "Project 2 (Autonomous Agentic AI with Vector Memory). On Days 4 and 5, the instructor acts strictly as an evaluator "
        "and provides zero code debugging assistance.",
        styles["Body"],
    ))
    story.append(PageBreak())

    # -------------------- CHAPTER 2: CONCEPTUAL RESET --------------------
    add_chapter_header(story, "Chapter 2", "The Core Conceptual Reset: Passive Pipelines vs. Autonomous Agency", styles)

    story.append(Paragraph(
        "Before writing a single line of agent code, engineers must discard marketing terminology and establish "
        "a precise systems definition of agency. Across universities and software companies, many teams mislabel "
        "ordinary API wrappers as 'AI Agents'. Understanding why that classification is wrong is the foundation "
        "of every architectural decision in this course.",
        styles["Body"],
    ))

    story.append(make_callout(
        "THE COMMON MISCONCEPTION DISSECTED",
        "<b>Claim:</b> 'An AI that connects to my email inbox and summarizes unread messages whenever I ask is an Agentic AI.'<br/><br/>"
        "<b>Systems Reality:</b> That architecture is <b>Passive Tool Augmentation (Single-Turn Function Calling)</b>. "
        "It is NOT agentic. The human initiates the request, the developer hardcodes the exact tool pipeline, "
        "the model produces one summary completion, and the process terminates immediately. The model exercises zero "
        "planning authority, zero error recovery, and zero goal verification.",
        styles, border_color="#EA580C", bg_color="#FFF7ED",
    ))
    story.append(Spacer(1, 6))

    story.extend(make_diagram(
        "diag_autonomy_spectrum.png",
        "Figure 2.1: Structural difference between Level 1 passive single-turn tool augmentation and Level 3 autonomous agency.",
        styles,
    ))

    story.append(Paragraph("2.1 The Five-Level Spectrum of AI System Autonomy", styles["H2"]))
    story.append(Paragraph(
        "Software engineers classify LLM systems along five discrete autonomy levels. Knowing which level a problem "
        "actually requires prevents over-engineering simple tasks and under-engineering complex workflows:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Level 0 — Static Prompting:</b> Direct text-in, text-out interaction. No external data, no tools, no state.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Level 1 — Passive Tool Augmentation (Function Calling):</b> The model invokes a single tool (such as fetching emails or weather) on demand and returns a formatted response. Control stays entirely with the human.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Level 2 — Deterministic RAG Pipeline:</b> A fixed script retrieves relevant document chunks from a vector database and passes them to the LLM. Still a single linear pass — Project 1 operates at Level 2.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Level 3 — Autonomous Agent (ReAct + Memory):</b> Given a high-level objective, the LLM runs inside a loop. It plans sub-tasks, selects tools dynamically, inspects outputs, recovers from runtime errors, recalls episodic memory, and stops only when the goal is verified — Project 2 operates at Level 3.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Level 4 — Multi-Agent Swarms:</b> Multiple specialized Level 3 agents collaborate asynchronously through shared message boards and task contracts.", styles["Bullet"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 Six-Dimension Architectural Comparison", styles["H2"]))
    comp_headers = ["Dimension", "Passive Tool Use / RAG (Levels 1-2)", "Autonomous Agentic AI (Level 3)"]
    comp_rows = [
        ["Control Flow", "Linear request-response pipeline executed once per prompt.", "Iterative while-loop: Thought -> Action -> Observation -> Reflection."],
        ["Initiative & Planning", "Human decomposes the task and triggers each step manually.", "Human declares the end-state goal; agent decomposes sub-steps dynamically."],
        ["Error Handling", "Tool exception crashes the script or prints a raw error to the user.", "Self-healing: try/except feeds the error trace back so the LLM repairs arguments."],
        ["Multi-Step Chaining", "Impossible unless a programmer hardcodes the exact call sequence.", "Agent chooses the next tool dynamically based on what the prior tool returned."],
        ["Memory Architecture", "Stateless per call, or raw chat history that overflows context limits.", "Dual memory: rolling short-term scratchpad plus ChromaDB long-term episodic store."],
        ["Termination Rule", "Stops immediately after one LLM token generation completes.", "Stops only when the agent verifies goal satisfaction and emits FINAL ANSWER:."],
    ]
    story.append(make_table(comp_headers, comp_rows, [104, 188, 194], styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.3 Worked ECE Engineering Case Study", styles["H2"]))
    story.append(Paragraph(
        "Consider a campus IoT sensor network of 50 environmental monitoring nodes. Compare how a passive script "
        "versus an autonomous agent responds when an anomaly alert fires:",
        styles["Body"],
    ))
    story.append(Paragraph(
        "<b>Passive Pipeline Approach:</b> An engineer types <i>'Read sensor_logs.csv and summarize Node 17.'</i> "
        "The backend loads the CSV, sends rows to the LLM, and prints <i>'Node 17 voltage is 1.8V.'</i> "
        "The engineer must then manually open old incident tickets, manually check the Zigbee network topology, "
        "manually diagnose battery depletion, and manually draft the maintenance ticket.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "<b>Autonomous Agent Approach:</b> The monitoring daemon passes a goal: <i>'Investigate Node 17 anomaly, "
        "identify root cause using historical incidents and network topology, and file an audit report.'</i> "
        "Without human intervention, the agent calls <code>analyze_sensor_telemetry('SENSOR_017')</code>, detects a 1.8V drop, "
        "queries ChromaDB episodic memory for past under-voltage failures, finds that 1.8V matches lithium cell depletion, "
        "verifies packet loss via <code>check_network_topology()</code>, writes a formatted Markdown post-mortem to disk, "
        "and logs a new lesson into vector memory. That closed-loop execution is true engineering agency.",
        styles["Body"],
    ))
    story.append(PageBreak())

    # -------------------- CHAPTER 3: WINDOWS STACK & SETUP --------------------
    add_chapter_header(story, "Chapter 3", "Windows Engineering Stack & Cloud API Verification", styles)

    story.append(Paragraph(
        "Running local 70-billion-parameter LLMs requires 40+ GB of GPU VRAM, which excludes standard undergraduate "
        "laptops. This program enforces a strict <b>API-only, zero-local-GPU architecture</b>. Heavy LLM inference runs "
        "on Groq's cloud LPU hardware over standard HTTPS, while ChromaDB runs locally on CPU with minimal RAM overhead. "
        "Every student with a basic 4 GB RAM Windows laptop achieves sub-second response latency.",
        styles["Body"],
    ))

    story.append(Paragraph("3.1 Mandatory Hardware & Software Stack", styles["H2"]))
    sys_headers = ["Component", "Standardized Tool", "Why This Exact Choice"]
    sys_rows = [
        ["Operating System", "Windows 10 / 11 (64-bit)", "Standardized paths, PowerShell syntax, and lab parity."],
        ["Python Runtime", "Python 3.13 (Add to PATH)", "Latest stable standard library, clean type syntax, fast runtime."],
        ["Package Manager", "uv (pip install uv)", "Rust-based resolver; 10-50x faster than pip with deterministic lockfiles."],
        ["Development IDE", "Antigravity IDE", "AI-native engineering editor with integrated PowerShell terminal."],
        ["Version Control", "Git for Windows + GitHub", "Industry-standard milestone commits, branching, and portfolio hosting."],
        ["LLM Inference", "Groq Cloud API (Free Tier)", "Free Llama 3.3 70B & Llama 3.1 8B endpoints; zero credit card required."],
        ["Vector Database", "ChromaDB (Local SQLite)", "Purpose-built vector store; single package install, zero external server."],
        ["Hardware Floor", "4 GB RAM, 5 GB free disk", "Runs smoothly on entry-level laptops; zero dedicated GPU required."],
    ]
    story.append(make_table(sys_headers, sys_rows, [104, 152, 230], styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Step-by-Step PowerShell Workspace Initialization", styles["H2"]))
    story.append(Paragraph(
        "Open PowerShell and execute the commands below in order. Each step isolates your workshop dependencies "
        "inside a project-local virtual environment (<code>.venv</code>) so packages never conflict with system Python.",
        styles["Body"],
    ))

    setup_cmds = [
        "# Step 1: Confirm Python 3.13 is accessible on Windows PATH",
        "python --version",
        "",
        "# Step 2: Install the uv package manager globally",
        "pip install uv",
        "uv --version",
        "",
        "# Step 3: Create and enter the workshop workspace directory",
        "mkdir vap-agentic-ai",
        "cd vap-agentic-ai",
        "",
        "# Step 4: Initialize pyproject.toml and isolated .venv automatically",
        "uv init",
        "",
        "# Step 5: Install only lightweight, essential dependencies (zero framework bloat)",
        "uv add chromadb requests python-dotenv pydantic duckduckgo-search",
        "",
        "# Step 6: Configure Git identity for milestone submissions",
        'git config --global user.name "Your Full Name"',
        'git config --global user.email "your.email@acharya.ac.in"',
    ]
    story.append(make_code_box("PowerShell Setup Sequence (Day 1 Working Session: 14:00 - 17:00)", setup_cmds, styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.3 Secret Management & API Verification (verify.py)", styles["H2"]))
    story.append(Paragraph(
        "Hardcoding API keys in Python source files is a critical security failure: pushing a secret to a public "
        "GitHub repository causes automated bots to harvest and revoke your key within minutes. Always store keys "
        "inside a local <code>.env</code> file (<code>GROQ_API_KEY=gsk_your_key</code>) and immediately add "
        "<code>.env</code>, <code>.venv/</code>, and <code>__pycache__/</code> to <code>.gitignore</code>.",
        styles["Body"],
    ))
    story.append(Paragraph(
        "We intentionally call the Groq REST endpoint using Python's built-in <code>urllib.request</code> library "
        "instead of hiding HTTP mechanics behind opaque wrapper SDKs. Understanding raw headers, JSON request payloads, "
        "and response structures makes you independent of any specific vendor library.",
        styles["Body"],
    ))

    verify_code = [
        "# verify.py -- Confirm Groq Cloud API connectivity and measure latency",
        "import json",
        "import os",
        "import time",
        "import urllib.request",
        "from dotenv import load_dotenv",
        "",
        "# Load key-value pairs from .env into os.environ",
        "load_dotenv()",
        "api_key = os.environ.get('GROQ_API_KEY')",
        "if not api_key:",
        "    raise RuntimeError('Missing GROQ_API_KEY. Create a .env file in project root.')",
        "",
        "# Groq exposes an OpenAI-compatible Chat Completions REST endpoint",
        "API_URL = 'https://api.groq.com/openai/v1/chat/completions'",
        "headers = {",
        "    'Authorization': f'Bearer {api_key}',  # Standard Bearer token auth",
        "    'Content-Type': 'application/json',    # Declare UTF-8 JSON body",
        "}",
        "",
        "# Construct deterministic test request (temperature=0.0 removes randomness)",
        "payload = {",
        "    'model': 'llama-3.1-8b-instant',",
        "    'messages': [",
        "        {'role': 'user', 'content': 'Connectivity check. Reply with ONE word: ONLINE'}",
        "    ],",
        "    'max_tokens': 10,",
        "    'temperature': 0.0,",
        "}",
        "",
        "# Encode Python dict -> JSON string -> raw UTF-8 bytes for HTTP POST",
        "body_bytes = json.dumps(payload).encode('utf-8')",
        "req = urllib.request.Request(API_URL, data=body_bytes, headers=headers, method='POST')",
        "",
        "start_time = time.perf_counter()",
        "with urllib.request.urlopen(req, timeout=15) as response:",
        "    elapsed_ms = (time.perf_counter() - start_time) * 1000",
        "    data = json.loads(response.read().decode('utf-8'))",
        "    reply = data['choices'][0]['message']['content'].strip()",
        "    tokens = data['usage']['total_tokens']",
        "    print(f'Status: {reply} | Latency: {elapsed_ms:.0f} ms | Tokens: {tokens}')",
    ]
    story.append(make_code_box("File: verify.py (Run via: uv run python verify.py)", verify_code, styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Code Explanation:</b> Line 9 calls <code>load_dotenv()</code> to inject your secret key into process memory "
        "without touching source code. Lines 15–18 attach standard HTTP Bearer authentication headers. "
        "Setting <code>temperature=0.0</code> forces greedy decoding so the model produces repeatable output for testing. "
        "Finally, <code>time.perf_counter()</code> measures end-to-end round-trip latency and prints token usage from "
        "<code>data['usage']</code> — a habit every production AI engineer uses to monitor API cost and speed.",
        styles["Body"],
    ))
    story.append(Paragraph("3.4 Guided Lab Exercise 1.1: Benchmarking Speed vs. Reasoning Capacity", styles["H2"]))
    story.append(Paragraph(
        "Before moving to Chapter 4, complete these three verification tasks in your local workspace:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Task A (Model Latency Comparison):</b> Run <code>verify.py</code> twice — first with <code>llama-3.1-8b-instant</code> and then with <code>llama-3.3-70b-versatile</code>. Record the millisecond latency difference. Notice why engineers route simple classification steps to 8B models and complex planning steps to 70B models.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Task B (Temperature Experiment):</b> Ask the model to explain an Op-Amp in one sentence at <code>temperature=0.0</code> (run 3 times) vs. <code>temperature=1.2</code> (run 3 times). Observe how higher temperatures introduce phrasing variance and factual drift.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Task C (Secret Leak Prevention Audit):</b> Run <code>git status</code> in PowerShell and confirm <code>.env</code> does NOT appear in untracked files. Push your initial <code>verify.py</code> and <code>.gitignore</code> to GitHub.", styles["Bullet"]))
    story.append(PageBreak())

    # -------------------- CHAPTER 4: VECTOR MATH & EMBEDDINGS --------------------
    add_chapter_header(story, "Chapter 4", "Mathematical Foundations of Embeddings, Chunking & Vector Indexing", styles)

    story.append(Paragraph(
        "Traditional database search (SQL <code>LIKE</code> or keyword inverted indexes) fails on engineering queries "
        "because human technicians use synonyms. A junior engineer searching <i>'How does a transistor amplify current?'</i> "
        "will miss a manual titled <i>'MOSFET Gate Voltage Control Characteristics'</i> because zero words match exactly. "
        "Vector embeddings solve this by mapping text into a continuous geometric coordinate system where meaning "
        "corresponds to direction.",
        styles["Body"],
    ))

    story.append(Paragraph("4.1 Dense Embeddings & Cosine Similarity Geometry", styles["H2"]))
    story.append(Paragraph(
        "An embedding model (such as ChromaDB's default <code>all-MiniLM-L6-v2</code> running locally via lightweight ONNX) "
        "transforms any sentence into a fixed-length vector of 384 floating-point numbers in <b>R</b><sup>384</sup>. "
        "Sentences with related meanings point in nearly the same direction in this 384-dimensional space.",
        styles["Body"],
    ))

    story.append(make_callout(
        "CORE VECTOR SIMILARITY EQUATIONS",
        "Given two embedding vectors <b>u</b> = (u<sub>1</sub>, ..., u<sub>D</sub>) and <b>v</b> = (v<sub>1</sub>, ..., v<sub>D</sub>) in <b>R</b><sup>D</sup>:<br/><br/>"
        "&bull; <b>Dot Product:</b> &nbsp; <b>u</b> &middot; <b>v</b> = &Sigma;<sub>i=1..D</sub> (u<sub>i</sub> &times; v<sub>i</sub>)<br/>"
        "&bull; <b>L2 Norm (Magnitude):</b> &nbsp; ||<b>u</b>|| = &radic;( &Sigma;<sub>i=1..D</sub> u<sub>i</sub><sup>2</sup> )<br/>"
        "&bull; <b>Cosine Similarity:</b> &nbsp; cos(&theta;) = (<b>u</b> &middot; <b>v</b>) / ( ||<b>u</b>|| &times; ||<b>v</b>|| )<br/>"
        "&bull; <b>Cosine Distance:</b> &nbsp; d<sub>cos</sub>(<b>u</b>, <b>v</b>) = 1 &minus; cos(&theta;)<br/><br/>"
        "A cosine similarity of <b>+1.0</b> means identical semantic direction (0&deg; angle). "
        "A value of <b>0.0</b> means orthogonal / unrelated meaning (90&deg; angle). "
        "Because cosine similarity divides by vector magnitude, it compares topic direction accurately even when "
        "a short 6-word query is matched against a long 80-word technical paragraph.",
        styles, border_color="#1E3A8A", bg_color="#EFF6FF",
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.2 Worked 3D Numerical Example (Compute by Hand)", styles["H2"]))
    story.append(Paragraph(
        "Imagine a simplified 3-dimensional semantic space where the three axes represent "
        "<i>(Semiconductor Physics, Energy Storage, Software Programming)</i>:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Query q</b> (<i>'How does a transistor work?'</i>) = [0.95, 0.10, 0.05]", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Doc A</b> (<i>'MOSFET gate voltage controls drain current.'</i>) = [0.92, 0.12, 0.00]", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Doc B</b> (<i>'A capacitor stores charge in an electric field.'</i>) = [0.15, 0.96, 0.00]", styles["Bullet"]))
    story.append(Paragraph(
        "Computing cosine similarity: <b>q &middot; A</b> = (0.95)(0.92) + (0.10)(0.12) + 0 = <b>0.886</b>; "
        "||<b>q</b>|| = 0.957, ||<b>A</b>|| = 0.928, so <b>cos(q, A) = 0.886 / 0.888 = 0.998</b> (near-perfect match!). "
        "Meanwhile, <b>q &middot; B</b> = (0.95)(0.15) + (0.10)(0.96) = 0.2385, giving <b>cos(q, B) = 0.256</b>. "
        "Even with zero shared keywords, vector geometry ranks Doc A at the top cleanly.",
        styles["Body"],
    ))

    story.append(Paragraph("4.3 Document Chunking Science & HNSW Indexing", styles["H2"]))
    story.append(Paragraph(
        "Embedding an entire 40-page datasheet as a single vector averages together hundreds of unrelated specifications "
        "(power rails, pinouts, RF limits, thermal curves) into a blurry vector that matches nothing well. "
        "Engineers therefore split source documents into focused chunks before indexing:",
        styles["Body"],
    ))

    chunk_headers = ["Chunking Strategy", "Mechanism", "Engineering Trade-Offs"]
    chunk_rows = [
        ["Fixed Character Split", "Cuts strictly every N characters (e.g., 500 chars).", "Trivial to code, but breaks sentences and equations mid-thought."],
        ["Sentence-Aware Split", "Accumulates complete sentences until budget (400 chars) is reached.", "Preserves grammatical meaning; ideal default for technical manuals."],
        ["Sliding Window Overlap", "Repeats the final 1-2 sentences of chunk i at the start of chunk i+1.", "Prevents losing facts that straddle a chunk boundary; ~15% storage cost."],
    ]
    story.append(make_table(chunk_headers, chunk_rows, [116, 175, 195], styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Why ChromaDB Scales (HNSW Graphs):</b> Comparing a query vector against every stored vector one by one "
        "requires <b>O(N)</b> operations. At 100,000 chunks, brute-force scanning causes unacceptable lag. "
        "ChromaDB automatically builds a <b>Hierarchical Navigable Small World (HNSW)</b> graph — a multi-layer "
        "proximity highway that navigates coarse clusters first and refines locally, achieving <b>O(log N)</b> query "
        "time in milliseconds on a standard laptop CPU.",
        styles["Body"],
    ))

    story.append(Paragraph("4.4 Hands-On Sandbox Lab: First ChromaDB Query (chroma_demo.py)", styles["H2"]))
    demo_code = [
        "# chroma_demo.py -- Verify semantic similarity matching without shared keywords",
        "import chromadb",
        "",
        "# Create a lightweight in-memory client for fast experimentation",
        "client = chromadb.Client()",
        "collection = client.create_collection(name='ece_concepts')",
        "",
        "# ChromaDB automatically downloads/runs the all-MiniLM-L6-v2 ONNX embedder on CPU",
        "collection.add(",
        "    documents=[",
        "        'The MOSFET gate-to-source voltage controls channel drain current.',",
        "        'A capacitor stores electrical energy inside a dielectric electric field.',",
        "        'Nyquist theorem requires sampling at twice the highest signal frequency.',",
        "    ],",
        "    metadatas=[{'topic': 'devices'}, {'topic': 'passives'}, {'topic': 'dsp'}],",
        "    ids=['doc_1', 'doc_2', 'doc_3'],",
        ")",
        "",
        "# Run a query containing ZERO exact words from doc_1",
        "results = collection.query(",
        "    query_texts=['How does a field effect transistor amplify signals?'],",
        "    n_results=2,",
        ")",
        "for doc, dist in zip(results['documents'][0], results['distances'][0]):",
        "    print(f'Distance: {dist:.4f} | Match: {doc}')",
    ]
    story.append(make_code_box("File: chroma_demo.py (Day 1 Working Session: 14:00 - 17:00)", demo_code, styles))
    story.append(PageBreak())

    # -------------------- CHAPTER 5: PROJECT 1 VECTOR RAG --------------------
    add_chapter_header(story, "Chapter 5", "Project 1: Building a Production Vector RAG Pipeline", styles)

    story.append(Paragraph(
        "Project 1 (worth 30 points) challenges students to build a complete, persistent Retrieval-Augmented "
        "Generation system across two modular Python scripts: <code>ingest.py</code> (offline indexing) and "
        "<code>query.py</code> (runtime retrieval and grounded generation). Separating offline ingestion from "
        "online querying mirrors real production architecture so documents are embedded once and queried thousands of times.",
        styles["Body"],
    ))

    story.extend(make_diagram(
        "diag_rag_architecture.png",
        "Figure 5.1: Complete two-phase Vector RAG pipeline separating offline ChromaDB indexing from runtime Groq LLM grounding.",
        styles,
    ))

    story.append(Paragraph("5.1 Phase 1: Document Ingestion Engine (ingest.py)", styles["H2"]))
    story.append(Paragraph(
        "A common beginner bug is calling <code>collection.add()</code> twice on the same files, which crashes with "
        "a duplicate-ID error. Production pipelines use <code>collection.upsert()</code> with deterministic IDs "
        "(<code>filename_chunk_index</code>), making re-ingestion safely idempotent. We also apply a 1-sentence "
        "sliding overlap so context never breaks abruptly across chunk boundaries.",
        styles["Body"],
    ))

    ingest_code = [
        "# ingest.py -- Idempotent Document Ingestion & Sentence Chunking Pipeline",
        "import os",
        "import chromadb",
        "",
        "def load_documents(directory: str) -> list[dict]:",
        "    '''Read all .md and .txt files from the knowledge base folder.'''",
        "    docs = []",
        "    for fname in sorted(os.listdir(directory)):",
        "        if fname.endswith(('.md', '.txt')):",
        "            full_path = os.path.join(directory, fname)",
        "            with open(full_path, 'r', encoding='utf-8') as f:",
        "                docs.append({'filename': fname, 'content': f.read()})",
        "    return docs",
        "",
        "def chunk_with_overlap(text: str, max_chars: int = 400) -> list[str]:",
        "    '''Group sentences up to max_chars while carrying the last sentence forward.'''",
        "    sentences = [s.strip() for s in text.replace('\\n', ' ').split('. ') if s.strip()]",
        "    chunks, current = [], []",
        "    for sentence in sentences:",
        "        candidate = '. '.join(current + [sentence]) + '.'",
        "        if len(candidate) > max_chars and current:",
        "            chunks.append('. '.join(current) + '.')",
        "            # Keep last sentence as overlap window for boundary continuity",
        "            current = [current[-1], sentence]",
        "        else:",
        "            current.append(sentence)",
        "    if current:",
        "        chunks.append('. '.join(current) + '.')",
        "    return chunks",
        "",
        "def run_ingestion(source_dir: str = 'knowledge_base', db_path: str = './chroma_db'):",
        "    '''Persist document embeddings and source metadata to local ChromaDB.'''",
        "    # PersistentClient saves HNSW index + SQLite metadata to disk",
        "    client = chromadb.PersistentClient(path=db_path)",
        "    collection = client.get_or_create_collection(name='rag_knowledge')",
        "",
        "    raw_docs = load_documents(source_dir)",
        "    total = 0",
        "    for doc in raw_docs:",
        "        chunks = chunk_with_overlap(doc['content'])",
        "        ids = [f\"{doc['filename']}_chunk_{i}\" for i in range(len(chunks))]",
        "        metas = [{'source': doc['filename'], 'chunk_index': i} for i in range(len(chunks))]",
        "        # upsert() inserts new chunks or updates existing IDs without crashing",
        "        collection.upsert(documents=chunks, metadatas=metas, ids=ids)",
        "        total += len(chunks)",
        "    print(f'Indexed {total} chunks across {len(raw_docs)} files into {db_path}.')",
        "",
        "if __name__ == '__main__':",
        "    run_ingestion()",
    ]
    story.append(make_code_box("File: ingest.py (Project 1 -- Day 2 Working Session: 14:00 - 17:00)", ingest_code, styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.2 Phase 2: Semantic Retrieval & Grounded Generation (query.py)", styles["H2"]))
    story.append(Paragraph(
        "Without strict grounding instructions, LLMs blend retrieved facts with memorized pre-training weights, "
        "producing confident hallucinations when asked about proprietary schematics or lab procedures. "
        "Notice how <code>query.py</code> solves this using three defensive techniques: (1) formatting every retrieved "
        "chunk with an explicit <code>[Source: filename (chunk N)]</code> header, (2) instructing the system prompt "
        "to refuse out-of-domain questions, and (3) setting <code>temperature=0.1</code> to minimize creative drift.",
        styles["Body"],
    ))

    query_code = [
        "# query.py -- Semantic Context Retrieval & Grounded Citation Generation",
        "import json",
        "import os",
        "import urllib.request",
        "import chromadb",
        "from dotenv import load_dotenv",
        "",
        "load_dotenv()",
        "",
        "def retrieve_context(question: str, top_k: int = 3, db_path: str = './chroma_db') -> str:",
        "    '''Query ChromaDB and format the top-k nearest chunks with source tags.'''",
        "    client = chromadb.PersistentClient(path=db_path)",
        "    collection = client.get_collection(name='rag_knowledge')",
        "    res = collection.query(query_texts=[question], n_results=top_k)",
        "    formatted = []",
        "    for doc, meta in zip(res['documents'][0], res['metadatas'][0]):",
        "        tag = f\"[Source: {meta['source']} (chunk {meta['chunk_index']})]\"",
        "        formatted.append(f'{tag}\\n{doc}')",
        "    return '\\n\\n'.join(formatted)",
        "",
        "def ask_groq(system_prompt: str, user_prompt: str) -> str:",
        "    '''Invoke Groq Llama 3.3 70B using standard library urllib.'''",
        "    url = 'https://api.groq.com/openai/v1/chat/completions'",
        "    headers = {",
        "        'Authorization': f\"Bearer {os.environ['GROQ_API_KEY']}\",",
        "        'Content-Type': 'application/json',",
        "    }",
        "    payload = {",
        "        'model': 'llama-3.3-70b-versatile',",
        "        'messages': [",
        "            {'role': 'system', 'content': system_prompt},",
        "            {'role': 'user', 'content': user_prompt},",
        "        ],",
        "        'temperature': 0.1,   # Low temperature enforces factual precision",
        "        'max_tokens': 512,",
        "    }",
        "    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)",
        "    with urllib.request.urlopen(req, timeout=20) as resp:",
        "        return json.loads(resp.read().decode('utf-8'))['choices'][0]['message']['content']",
        "",
        "def answer_question(question: str) -> str:",
        "    context = retrieve_context(question)",
        "    sys_prompt = (",
        "        'You are a technical engineering assistant. Answer ONLY using the provided Context. '",
        "        'If the Context lacks the answer, reply exactly: Insufficient evidence in knowledge base. '",
        "        'Cite every factual claim using [Source: filename (chunk N)].'",
        "    )",
        "    user_prompt = f'Context:\\n{context}\\n\\nQuestion: {question}'",
        "    return ask_groq(sys_prompt, user_prompt)",
        "",
        "if __name__ == '__main__':",
        "    q = input('Engineering Question: ')",
        "    print('\\n' + answer_question(q))",
    ]
    story.append(make_code_box("File: query.py (Project 1 -- Day 2 Working Session: 14:00 - 17:00)", query_code, styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.3 Project 1 Verification Matrix & Submission", styles["H2"]))
    story.append(make_callout(
        "MANDATORY PROJECT 1 TEST CASES BEFORE GITHUB PUSH",
        "<b>Test 1 (In-Domain Factual):</b> Ask a specific specification question covered in your documents. Confirm exact numbers and valid <code>[Source: ...]</code> tags.<br/>"
        "<b>Test 2 (Out-of-Domain Refusal):</b> Ask <i>'Who won the 2024 Olympics?'</i> Confirm the system refuses cleanly without hallucinating.<br/>"
        "<b>Test 3 (Synonym / Zero-Keyword Match):</b> Rephrase a technical concept using different words. Confirm ChromaDB retrieves the right chunk semantically.<br/><br/>"
        "<b>Transition Insight:</b> Commit Project 1 to GitHub (<code>git commit -m 'Project 1: Vector RAG'</code>). Notice its ceiling: it waits passively for one prompt, performs one lookup, and halts. Tomorrow, we give it agency.",
        styles, border_color="#EA580C", bg_color="#FFF7ED",
    ))
    story.append(PageBreak())

    # -------------------- CHAPTER 6: REACT & TOOL CALLING --------------------
    add_chapter_header(story, "Chapter 6", "Bridging to Agency: The ReAct Pattern & JSON Tool Calling", styles)

    story.append(Paragraph(
        "Large Language Models are pure text predictors — they cannot read local CSV files, run math safely, "
        "query live sensors, or write reports on their own. To turn an LLM into an autonomous engineer, "
        "we combine two mechanisms: <b>structured tool calling</b> (allowing the model to request Python function "
        "executions via JSON) and the <b>ReAct control loop</b> (allowing the model to inspect tool outputs and "
        "plan subsequent steps iteratively).",
        styles["Body"],
    ))

    story.append(Paragraph("6.1 The ReAct State Machine (Reason + Act)", styles["H2"]))
    story.append(Paragraph(
        "Introduced by Yao et al. (ICLR 2023), the ReAct paradigm interleaves internal reasoning traces with "
        "external environment actions inside a bounded execution loop:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Step 1 — Thought (State Assessment):</b> The model evaluates the user goal against observations gathered so far and identifies the next missing piece of evidence.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Step 2 — Action (Structured Invocation):</b> Instead of guessing an answer, the model emits a JSON tool call specifying an exact registered function name and typed parameter values.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Step 3 — Observation (Deterministic Execution):</b> Your Python runtime executes the requested function locally and appends the return string (or caught error message) back into the conversation history.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Step 4 — Reflection &amp; Next Iteration:</b> The LLM reads the observation. If the tool failed or revealed a new clue, the agent adjusts its strategy and loops again until the objective is verified.", styles["Bullet"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.2 JSON Schema Tool Contracts & Dynamic Dispatch Registry", styles["H2"]))
    story.append(Paragraph(
        "The Groq API accepts a <code>tools</code> array describing every function the agent is allowed to call. "
        "Write crystal-clear parameter descriptions — vague descriptions cause the LLM to pass wrong argument formats. "
        "On the Python side, we pair schemas with a lightweight <code>@register_tool</code> decorator that maps "
        "function names to callable objects inside <code>TOOL_REGISTRY</code>.",
        styles["Body"],
    ))

    tools_code = [
        "# tools.py -- Modular Tool Suite with Workspace Safety & JSON Schemas",
        "import ast",
        "import json",
        "import operator",
        "import os",
        "from duckduckgo_search import DDGS",
        "",
        "TOOL_REGISTRY = {}  # Maps string tool names -> executable Python functions",
        "WORKSPACE_DIR = os.path.abspath('./workspace')",
        "os.makedirs(WORKSPACE_DIR, exist_ok=True)",
        "",
        "def register_tool(func):",
        "    '''Decorator that registers a Python function for dynamic agent dispatch.'''",
        "    TOOL_REGISTRY[func.__name__] = func",
        "    return func",
        "",
        "@register_tool",
        "def search_web(query: str) -> str:",
        "    '''Search DuckDuckGo and return top 3 concise summaries.'''",
        "    with DDGS() as ddgs:",
        "        hits = list(ddgs.text(query, max_results=3))",
        "    return json.dumps(hits, indent=2) if hits else 'No web results found.'",
        "",
        "@register_tool",
        "def write_report(filename: str, content: str) -> str:",
        "    '''Safely write a Markdown report inside ./workspace only (blocks path traversal).'''",
        "    safe_name = os.path.basename(filename)  # Strip '../' directory escapes",
        "    target = os.path.join(WORKSPACE_DIR, safe_name)",
        "    with open(target, 'w', encoding='utf-8') as f:",
        "        f.write(content)",
        "    return f'Report saved to workspace/{safe_name} ({len(content)} chars).'",
        "",
        "@register_tool",
        "def calculate(expression: str) -> str:",
        "    '''Evaluate arithmetic safely using Python AST (never raw eval on untrusted text).'''",
        "    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}",
        "    def _eval(node):",
        "        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):",
        "            return node.value",
        "        if isinstance(node, ast.BinOp) and type(node.op) in ops:",
        "            return ops[type(node.op)](_eval(node.left), _eval(node.right))",
        "        raise ValueError(f'Unsupported expression element: {ast.dump(node)}')",
        "    return str(_eval(ast.parse(expression, mode='eval').body))",
        "",
        "# OpenAI/Groq JSON Schema declarations matching the functions above",
        "TOOL_SCHEMAS = [",
        "    {",
        "        'type': 'function',",
        "        'function': {",
        "            'name': 'search_web',",
        "            'description': 'Search the live web for technical papers, specs, or recent updates.',",
        "            'parameters': {",
        "                'type': 'object',",
        "                'properties': {'query': {'type': 'string', 'description': 'Specific search terms.'}},",
        "                'required': ['query'],",
        "            },",
        "        },",
        "    },",
        "    {",
        "        'type': 'function',",
        "        'function': {",
        "            'name': 'write_report',",
        "            'description': 'Save a structured Markdown report inside the workspace directory.',",
        "            'parameters': {",
        "                'type': 'object',",
        "                'properties': {",
        "                    'filename': {'type': 'string', 'description': 'File name such as audit.md.'},",
        "                    'content': {'type': 'string', 'description': 'Full Markdown text.'},",
        "                },",
        "                'required': ['filename', 'content'],",
        "            },",
        "        },",
        "    },",
        "]",
    ]
    story.append(make_code_box("File: tools.py (Safe Tool Engineering & JSON Schemas)", tools_code, styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Security Design Note:</b> Notice two production guardrails built right into <code>tools.py</code>. "
        "First, <code>os.path.basename(filename)</code> prevents path-traversal attacks where a confused LLM tries to "
        "write to <code>../../Windows/system32</code>. Second, <code>calculate()</code> parses arithmetic using "
        "Python's <code>ast</code> module instead of calling raw <code>eval()</code>, guaranteeing the model can "
        "never execute arbitrary operating system commands through the calculator tool.",
        styles["Body"],
    ))
    story.append(Paragraph("6.3 Guided Lab Exercise 3.1: Designing an ECE Hardware Tool &amp; Schema", styles["H2"]))
    story.append(Paragraph(
        "Practice writing deterministic tools by adding a fourth tool to <code>tools.py</code> before advancing to Chapter 7:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Step 1 — Write the Python Function:</b> Implement <code>@register_tool def ohms_law(voltage: float, resistance: float) -&gt; str:</code> that returns current in amperes and power dissipation in watts. Explicitly guard against <code>resistance &lt;= 0</code> by raising a descriptive <code>ValueError</code> so you can test agent self-healing later.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Step 2 — Declare the JSON Schema:</b> Add a matching entry to <code>TOOL_SCHEMAS</code> specifying <code>'type': 'number'</code> for both parameters and marking both in <code>'required'</code>.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Step 3 — Schema Contract Checklist:</b> Verify that (1) the schema <code>name</code> matches the exact Python function name, (2) every key in <code>properties</code> matches the exact parameter spelling, and (3) descriptions include engineering units (Volts, Ohms) so the LLM never passes millivolts by mistake.", styles["Bullet"]))
    story.append(PageBreak())

    # -------------------- CHAPTER 7: AGENT ENGINE & DUAL MEMORY --------------------
    add_chapter_header(story, "Chapter 7", "Autonomous Agent Engine & Dual-Memory Fusion", styles)

    story.append(Paragraph(
        "With tools registered and schemas declared, we now construct the heart of the entire 5-day program: "
        "the autonomous ReAct execution engine (<code>agent.py</code>) fused with ChromaDB episodic memory "
        "(<code>memory.py</code>) and post-task After Action Review (<code>aar_engine.py</code>).",
        styles["Body"],
    ))

    story.extend(make_diagram(
        "diag_react_loop.png",
        "Figure 7.1: Autonomous agent control engine fusing the ReAct while-loop with Tool Arsenal and ChromaDB Episodic Memory.",
        styles,
    ))

    story.append(Paragraph("7.1 The Pure-Python Agent While-Loop (agent.py)", styles["H2"]))
    story.append(Paragraph(
        "Every reliable autonomous agent implements four mandatory engineering safeguards: (1) a hard "
        "<code>max_steps</code> ceiling to stop infinite loops from draining API quotas, (2) a <code>try/except</code> "
        "wrapper around every tool call so runtime errors become readable observations instead of crashes, "
        "(3) output length capping (<code>[:2000]</code>) so a massive log dump never blows out the context window, "
        "and (4) a structured trace log (<code>trace.jsonl</code>) recording every Thought, Action, and Observation.",
        styles["Body"],
    ))

    agent_code = [
        "# agent.py -- Autonomous ReAct Agent Engine with Self-Healing & Trace Logging",
        "import json",
        "import os",
        "import urllib.request",
        "from dotenv import load_dotenv",
        "from tools import TOOL_REGISTRY, TOOL_SCHEMAS",
        "",
        "load_dotenv()",
        "",
        "def call_llm(messages: list[dict], tools: list[dict] | None = None) -> dict:",
        "    '''Send message history and tool declarations to Groq Llama 3.3 70B.'''",
        "    payload = {",
        "        'model': 'llama-3.3-70b-versatile',",
        "        'messages': messages,",
        "        'temperature': 0.1,",
        "        'max_tokens': 1024,",
        "    }",
        "    if tools:",
        "        payload['tools'] = tools",
        "        payload['tool_choice'] = 'auto'  # Let the LLM decide if/which tool to call",
        "    headers = {",
        "        'Authorization': f\"Bearer {os.environ['GROQ_API_KEY']}\",",
        "        'Content-Type': 'application/json',",
        "    }",
        "    req = urllib.request.Request(",
        "        'https://api.groq.com/openai/v1/chat/completions',",
        "        data=json.dumps(payload).encode('utf-8'),",
        "        headers=headers,",
        "    )",
        "    with urllib.request.urlopen(req, timeout=25) as resp:",
        "        return json.loads(resp.read().decode('utf-8'))",
        "",
        "def run_agent(goal: str, max_steps: int = 10) -> tuple[str, list[dict]]:",
        "    '''Execute autonomous ReAct control loop until goal is verified or budget expires.'''",
        "    sys_prompt = (",
        "        'You are an autonomous engineering agent with persistent vector memory. '",
        "        'Before diagnosing a problem, check recall_memory() for similar past cases. '",
        "        'If a tool returns an error, diagnose why and try a corrected call. '",
        "        'Only when every sub-goal is verified, emit FINAL ANSWER: followed by your report.'",
        "    )",
        "    history = [{'role': 'system', 'content': sys_prompt}, {'role': 'user', 'content': goal}]",
        "    trace_log = []",
        "",
        "    for step in range(1, max_steps + 1):",
        "        print(f'\\n=== Autonomous Step {step}/{max_steps} ===')",
        "        response = call_llm(history, tools=TOOL_SCHEMAS)",
        "        msg = response['choices'][0]['message']",
        "",
        "        # Branch A: The LLM decided to invoke one or more tools",
        "        if msg.get('tool_calls'):",
        "            history.append(msg)  # Preserve assistant tool request in rolling context",
        "            for call in msg['tool_calls']:",
        "                fn_name = call['function']['name']",
        "                try:",
        "                    fn_args = json.loads(call['function']['arguments'] or '{}')",
        "                    if fn_name not in TOOL_REGISTRY:",
        "                        result = f\"Tool Error: Unknown tool '{fn_name}'.\"",
        "                    else:",
        "                        result = str(TOOL_REGISTRY[fn_name](**fn_args))",
        "                except Exception as exc:",
        "                    # SELF-HEALING HOOK: return error string so LLM can recover!",
        "                    result = f'Tool Execution Error ({fn_name}): {exc}'",
        "",
        "                # Cap observation size to protect LLM context window",
        "                capped = result[:2000]",
        "                print(f'Action: {fn_name}({fn_args}) -> {capped[:120]}...')",
        "                trace_log.append({'step': step, 'tool': fn_name, 'obs': capped[:300]})",
        "                history.append({'role': 'tool', 'tool_call_id': call['id'], 'content': capped})",
        "",
        "        # Branch B: No tool call -- check for verified termination marker",
        "        else:",
        "            content = msg.get('content', '')",
        "            if 'FINAL ANSWER:' in content:",
        "                with open('trace.jsonl', 'a', encoding='utf-8') as f:",
        "                    f.write(json.dumps({'goal': goal, 'steps': trace_log}) + '\\n')",
        "                return content, trace_log",
        "            history.append(msg)",
        "",
        "    return 'HALTED: Step budget exhausted before goal verification.', trace_log",
    ]
    story.append(make_code_box("File: agent.py (Complete ReAct Execution Engine)", agent_code, styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("7.2 Dual-Memory Architecture & Episodic Vector Tools (memory.py)", styles["H2"]))
    story.append(Paragraph(
        "The <code>history</code> list inside <code>agent.py</code> acts as <b>Short-Term Working Memory</b> — "
        "it holds the immediate reasoning steps of the current task and resets when the process exits. "
        "By wrapping ChromaDB inside two registered agent tools (<code>store_memory</code> and <code>recall_memory</code>), "
        "Project 1's Vector RAG engine becomes <b>Long-Term Episodic Memory</b> that persists across sessions.",
        styles["Body"],
    ))

    mem_code = [
        "# memory.py -- Vector RAG Repurposed as Persistent Agent Episodic Memory",
        "import chromadb",
        "from tools import register_tool",
        "",
        "mem_client = chromadb.PersistentClient(path='./agent_memory')",
        "mem_col = mem_client.get_or_create_collection(name='episodic_memory')",
        "",
        "@register_tool",
        "def store_memory(category: str, observation: str) -> str:",
        "    '''Embed and store a verified fact or lesson learned for future sessions.'''",
        "    mem_id = f'mem_{mem_col.count() + 1}'",
        "    mem_col.upsert(",
        "        documents=[observation],",
        "        metadatas=[{'category': category}],",
        "        ids=[mem_id],",
        "    )",
        "    return f'Saved episodic memory {mem_id} under category [{category}].'",
        "",
        "@register_tool",
        "def recall_memory(query: str, top_k: int = 3) -> str:",
        "    '''Semantically retrieve similar past incidents and operational lessons.'''",
        "    count = mem_col.count()",
        "    if count == 0:",
        "        return 'Episodic memory store is currently empty.'",
        "    res = mem_col.query(query_texts=[query], n_results=min(top_k, count))",
        "    lines = [f\"[{m['category']}] {d}\" for d, m in zip(res['documents'][0], res['metadatas'][0])]",
        "    return '\\n'.join(lines)",
    ]
    story.append(make_code_box("File: memory.py (Persistent Episodic Memory Tools)", mem_code, styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("7.3 After Action Review (AAR): Self-Improving Agents", styles["H2"]))
    story.append(Paragraph(
        "Military and aerospace teams conduct an <b>After Action Review (AAR)</b> after every mission to extract "
        "reusable lessons. Our agent performs the exact same reflection automatically after <code>run_agent()</code> "
        "returns: it reviews its own <code>trace_log</code>, distills one concrete operational rule, and commits "
        "it into ChromaDB via <code>store_memory('aar_lesson', rule)</code>. On the next run, <code>recall_memory()</code> "
        "surfaces that lesson automatically so the agent never repeats the same diagnostic dead-end twice.",
        styles["Body"],
    ))

    aar_code = [
        "# aar_engine.py -- Automated Post-Task Reflection & Lesson Commitment",
        "import json",
        "from agent import call_llm",
        "from memory import store_memory",
        "",
        "def run_after_action_review(goal: str, trace_log: list[dict], outcome: str) -> str:",
        "    '''Distill one reusable engineering rule from the completed execution trace.'''",
        "    prompt = (",
        "        f'Goal: {goal}\\nTrace: {json.dumps(trace_log)}\\nOutcome: {outcome[:400]}\\n\\n'",
        "        'Write ONE concise operational rule (max 25 words) to solve similar future tasks faster.'",
        "    )",
        "    resp = call_llm([{'role': 'user', 'content': prompt}])",
        "    lesson = resp['choices'][0]['message']['content'].strip()",
        "    store_memory(category='aar_lesson', observation=lesson)",
        "    return lesson",
    ]
    story.append(make_code_box("File: aar_engine.py (Post-Execution Learning Engine)", aar_code, styles))
    story.append(Spacer(1, 6))
    story.append(Paragraph("7.4 Multi-Session Episodic Recall Walkthrough (Lab Exercise 3.2)", styles["H2"]))
    story.append(Paragraph(
        "Prove that your agent genuinely learns across completely separate terminal runs by executing this two-session test:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Session 1 (First Run):</b> Execute <code>uv run python agent.py</code> with a goal that triggers a deliberate error (e.g., querying an offline sensor ID). Watch the agent recover via topology lookup, produce its report, and run <code>run_after_action_review()</code> to store a lesson into <code>./agent_memory</code>.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Session 2 (Fresh Process):</b> Close PowerShell completely and open a new terminal. Run a related diagnostic goal. Observe in Step 1 that the agent calls <code>recall_memory()</code>, retrieves the exact lesson stored in Session 1, and solves the task in fewer steps without repeating the initial dead end.", styles["Bullet"]))
    story.append(make_callout(
        "WHY THIS ARCHITECTURE MATTERS IN PRODUCTION",
        "Notice that no model weights were fine-tuned and zero GPU training occurred — yet your system measurably "
        "improved its reliability between Session 1 and Session 2 purely through structured episodic memory in ChromaDB.",
        styles, border_color="#1E3A8A", bg_color="#EFF6FF",
    ))
    story.append(PageBreak())

    # -------------------- CHAPTER 8: CAPSTONE PROBLEM STATEMENTS --------------------
    add_chapter_header(story, "Chapter 8", "Project 2: Independent Capstone Problem Statements", styles)

    story.append(Paragraph(
        "During Days 4 and 5, students operate as independent engineering teams (individual or pairs). "
        "The instructor provides zero code debugging or architectural hints. Select <b>one</b> of the three "
        "problem statements below and deliver a complete, self-healing autonomous agent with at least 4 tools, "
        "ChromaDB episodic memory, trace logging, and an AAR reflection loop.",
        styles["Body"],
    ))

    story.extend(make_diagram(
        "diag_capstone_architecture.png",
        "Figure 8.1: Four-layer modular architecture required for all Project 2 capstone implementations.",
        styles,
    ))

    story.append(Paragraph("8.1 Option 1: Autonomous IoT Sensor Network Diagnostic Agent (ECE Embedded)", styles["H2"]))
    story.append(Paragraph(
        "<b>Engineering Scenario:</b> A smart-campus IoT deployment operates 50 wireless environmental sensor nodes "
        "(temperature, humidity, battery voltage). Intermittent anomalies have triggered automated monitoring alerts. "
        "Your agent receives an alert string, analyzes raw CSV telemetry logs statistically, inspects the wireless "
        "mesh topology graph, retrieves similar historical incidents from ChromaDB memory, identifies the exact root "
        "cause (battery depletion, thermistor disconnect, RF dropout, or sensor drift), and writes a formal post-mortem.",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Tool 1 — <code>query_incident_memory(query)</code>:</b> Semantic lookup over <code>past_incidents.json</code> indexed in ChromaDB.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 2 — <code>analyze_sensor_telemetry(sensor_id)</code>:</b> Parses <code>sensor_logs.csv</code>, computes mean/std-dev, and flags voltage or temperature spikes.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 3 — <code>check_network_topology(sensor_id)</code>:</b> Queries <code>network_topology.json</code> to verify parent gateway links, RSSI, and neighbor nodes.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 4 — <code>generate_diagnostic_report(filename, content)</code>:</b> Writes structured root-cause Markdown report into <code>workspace/</code>.", styles["Bullet"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.2 Option 2: Autonomous 5G/Wireless Protocol Compliance Agent (ECE Telecom)", styles["H2"]))
    story.append(Paragraph(
        "<b>Engineering Scenario:</b> A telecommunications lab tests a new 5G New Radio (NR) base station firmware build "
        "against 3GPP Release 17 RF specifications. Given a firmware build failure alert, your agent must parse raw "
        "test logs, compare measured RF metrics (Error Vector Magnitude, transmit power, frequency offset, timing advance) "
        "against specification limits, query ChromaDB compliance history for prior remediation fixes, and generate a "
        "pass/fail certification audit report.",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Tool 1 — <code>query_compliance_memory(query)</code>:</b> Semantic retrieval over historical compliance resolutions in ChromaDB.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 2 — <code>parse_test_log(build_id)</code>:</b> Extracts measured RF telemetry dictionaries from <code>firmware_test_output.json</code>.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 3 — <code>verify_against_spec(metrics_json)</code>:</b> Evaluates every parameter against <code>3gpp_thresholds.json</code> and returns violation deltas.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 4 — <code>generate_compliance_report(filename, content)</code>:</b> Emits formal pass/fail certification report with remediation steps.", styles["Bullet"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.3 Option 3: Autonomous Research Literature Survey & Gap Agent (Academic Core)", styles["H2"]))
    story.append(Paragraph(
        "<b>Engineering Scenario:</b> Designed to accelerate your upcoming VTU 7th/8th-semester major project. "
        "Given an emerging engineering research question (such as Spiking Neural Networks for edge audio or "
        "Federated Learning on microcontrollers), your agent queries an indexed corpus of paper abstracts in ChromaDB, "
        "runs live DuckDuckGo searches for recent preprints, clusters findings by methodology and year, identifies "
        "unsolved technical gaps, and writes an annotated literature review with citations.",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Tool 1 — <code>query_literature_memory(query)</code>:</b> Semantic search across <code>paper_abstracts.json</code> indexed in ChromaDB.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 2 — <code>search_web(query)</code>:</b> Live DuckDuckGo query for recent conference papers and arXiv preprints.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 3 — <code>extract_themes(papers_json)</code>:</b> Groups papers by architecture, hardware platform, and publication year to expose research gaps.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Tool 4 — <code>generate_literature_review(filename, content)</code>:</b> Writes structured literature survey with citations and proposed project direction.", styles["Bullet"]))
    story.append(PageBreak())

    # -------------------- CHAPTER 9: RUBRIC & CAREER ROADMAP --------------------
    add_chapter_header(story, "Chapter 9", "Evaluation Rubric, Live Defense & Career Engineering Roadmap", styles)

    story.append(Paragraph("9.1 Official 100-Point Assessment Rubric", styles["H2"]))
    rubric_headers = ["Evaluation Criterion", "Max", "Observable Engineering Standard"]
    rubric_rows = [
        ["P1: Ingestion & Chunking", "10", "Sentence-aware chunking with overlap, clean metadata, idempotent ChromaDB upsert."],
        ["P1: Semantic Retrieval", "10", "Top-k cosine search accurately retrieves domain chunks even on synonym queries."],
        ["P1: Grounded Generation", "10", "Accurate answers with [Source: file (chunk N)] tags; refuses out-of-domain prompts."],
        ["P2: Autonomous Control Flow", "20", "True ReAct while-loop where LLM selects tools. Hardcoded call order receives 0."],
        ["P2: Vector Memory Fusion", "15", "Agent contextually calls recall_memory() and persists findings via store_memory()."],
        ["P2: Tool Schemas & Safety", "10", "Minimum 4 tools with strict JSON schemas, typed parameters, and path safety."],
        ["P2: Self-Healing Recovery", "10", "Intercepts induced tool exception, reads error observation, and recovers cleanly."],
        ["P2: Unseen Live Benchmark", "10", "Executes end-to-end against unseen instructor evaluation prompt on Day 5."],
        ["P2: Code Quality & Docs", "5", "PEP 8 structure, uv pyproject.toml, .gitignore blocking .env, clear README.md."],
    ]
    story.append(make_table(rubric_headers, rubric_rows, [132, 34, 320], styles))
    story.append(Spacer(1, 10))

    story.append(make_callout(
        "PRE-DEFENSE SUBMISSION & SECURITY CHECKLIST (DAY 5, 1:00 PM)",
        "1. <b>Zero Leaked Secrets:</b> Run <code>git status</code> and verify <code>.env</code> is NOT tracked.<br/>"
        "2. <b>Reproducible Setup:</b> Confirm a fresh clone runs cleanly via <code>uv sync</code> and <code>uv run python agent.py</code>.<br/>"
        "3. <b>Execution Trace Evidence:</b> Confirm <code>trace.jsonl</code> logs every Thought, Action, and Observation.<br/>"
        "4. <b>Oral Defense Readiness:</b> Be prepared to explain dynamic dispatch, cosine similarity, and self-healing line by line.",
        styles, border_color="#1E3A8A", bg_color="#EFF6FF",
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("9.2 Beyond This Workshop: Your Engineering Career Roadmap", styles["H2"]))
    story.append(Paragraph(
        "The software patterns you built over these five days are not classroom toys — they form the exact architectural "
        "spine of modern production AI systems. Here is how to build on this momentum over the next three semesters:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>VTU Final-Year Major Project:</b> Pair a microcontroller (ESP32 / STM32) streaming real MQTT sensor telemetry with your autonomous diagnostic agent for an industry-grade hardware + AI capstone.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Model Context Protocol (MCP):</b> Explore the open MCP standard that generalizes the exact JSON tool schemas you wrote in <code>tools.py</code> into reusable cross-platform tool servers.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Hybrid Search &amp; Reranking:</b> Extend your ChromaDB vector retriever by combining BM25 keyword scores with cosine similarity (Reciprocal Rank Fusion) for precision datasheet search.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Technical Interviews:</b> You can now whiteboard the ReAct state machine, derive cosine similarity, explain HNSW complexity, and defend why pure tool calling is not agency.", styles["Bullet"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("9.3 Technical References", styles["H2"]))
    story.append(Paragraph("&bull; Yao, S. et al. (2023). <i>ReAct: Synergizing Reasoning and Acting in Language Models.</i> ICLR 2023.", styles["Bullet"]))
    story.append(Paragraph("&bull; Lewis, P. et al. (2020). <i>Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.</i> NeurIPS 2020.", styles["Bullet"]))
    story.append(Paragraph("&bull; Malkov, Y. &amp; Yashunin, D. (2020). <i>Efficient and Robust Approximate Nearest Neighbor Search Using HNSW Graphs.</i> IEEE TPAMI.", styles["Bullet"]))
    story.append(Paragraph("&bull; ChromaDB Documentation (docs.trychroma.com) &amp; Groq API Reference (console.groq.com/docs).", styles["Bullet"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("9.4 Showcasing Your Capstone on GitHub &amp; Resumes", styles["H2"]))
    story.append(Paragraph(
        "Do not let your capstone repository sit unused after Day 5. Recruiters for AI Engineering, Embedded Systems, "
        "and Telecom R&amp;D roles actively inspect public GitHub projects. Polish your repository with three additions:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Architecture Diagram in README.md:</b> Include a clean block diagram showing your ReAct loop, custom tools, and ChromaDB episodic memory collection.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Sample Execution Trace:</b> Paste a real multi-step terminal trace demonstrating autonomous tool chaining and error self-healing on an invalid input.", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Resume Impact Bullet:</b> <i>'Engineered an autonomous Python ReAct agent using Groq Llama 3.3 70B and ChromaDB HNSW vector memory to diagnose IoT/5G anomalies with automated exception self-healing and post-mortem reporting.'</i>", styles["Bullet"]))

    doc.build(story, canvasmaker=get_a4_canvas_class(
        "VAP STUDENT ENGINEERING HANDBOOK",
        "ECE 5TH SEMESTER | ACHARYA INSTITUTE OF TECHNOLOGY",
    ))
    print(f"Student Guide PDF built: {output_path}")


# ======================================================================
# DOCUMENT 2: INSTRUCTOR PREPARATION & TEACHING HANDBOOK (A4)
# ======================================================================
def build_instructor_guide(output_path: str):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=54, rightMargin=54, topMargin=56, bottomMargin=54,
    )
    styles = setup_styles()
    story = []

    # -------------------- COVER PAGE --------------------
    build_cover_page(
        story,
        "Teaching Autonomous Agentic AI<br/>Systems with Vector RAG Memory",
        "Instructor Preparation, Teaching Scripts, Reference Code &amp; Live Defense Suite",
        "Faculty Teaching Manual  |  Academic Year 2026 - 2027",
        styles,
    )

    # -------------------- CHAPTER 1: MASTER CHECKLIST --------------------
    add_chapter_header(story, "Chapter 1", "Pre-Workshop Master Checklist & Laboratory Readiness", styles)

    story.append(Paragraph(
        "This handbook equips the instructor with everything needed to run a smooth, high-impact 5-day workshop: "
        "advance laboratory verification scripts, verbatim classroom talk tracks, whiteboard pacing guides, "
        "live demo narratives, tested production reference code, capstone mock dataset generators, "
        "a live troubleshooting playbook, and unseen Day 5 defense benchmarks.",
        styles["Body"],
    ))

    story.extend(make_diagram(
        "diag_pedagogical_roadmap.png",
        "Figure 1.1: 5-Day instructional progression and the Day 4 authority transition from Mentor to Strict Evaluator.",
        styles,
    ))

    story.append(Paragraph("1.1 T-7 Days to Day 1 Operational Timeline", styles["H2"]))
    chk_headers = ["Timeline", "Preparation Milestone", "Exact Verification Action"]
    chk_rows = [
        ["T - 7 Days", "Campus Firewall Whitelist", "Confirm unrestricted HTTPS to api.groq.com, pypi.org, huggingface.co (ONNX model), and github.com."],
        ["T - 5 Days", "Lab PC Runtime Audit", "Verify Python 3.13 is installed with PATH enabled on sample lab PCs; test PowerShell execution policy."],
        ["T - 3 Days", "Student Onboarding Email", "Send pre-work note: install Git for Windows, create GitHub account, generate free Groq API key."],
        ["T - 2 Days", "Stage Mock Datasets", "Execute generate_mock_data.py (Chapter 6); verify all 3 capstone folders and push to template repo."],
        ["T - 1 Day", "Backup Keys & ONNX Cache", "Prepare 3 backup Groq keys; cache ChromaDB ONNX embedder on a USB drive in case campus Wi-Fi stalls."],
        ["Day 1 (08:30)", "Projector & IDE Setup", "Set Antigravity editor and PowerShell terminal fonts to 16pt high-contrast light theme for back-row legibility."],
    ]
    story.append(make_table(chk_headers, chk_rows, [76, 146, 264], styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.2 Network Verification & Groq Concurrency Planning", styles["H2"]))
    story.append(Paragraph(
        "The single biggest Day 1 time killer in college computer labs is an unannounced campus proxy blocking "
        "outbound HTTPS API calls or HuggingFace model downloads (ChromaDB downloads an ~80 MB ONNX embedding "
        "file on first run). Run this PowerShell diagnostic on a lab workstation 7 days before the workshop:",
        styles["Body"],
    ))

    net_cmd = [
        "# Test 1: Confirm api.groq.com SSL handshake (401 Unauthorized = REACHABLE!)",
        "try { Invoke-WebRequest -Uri 'https://api.groq.com/openai/v1/models' -TimeoutSec 10 }",
        "catch { Write-Host 'Groq Reachable. HTTP Status:' $_.Exception.Response.StatusCode.value__ }",
        "",
        "# Test 2: Confirm PyPI package index reachability",
        "(Invoke-WebRequest -Uri 'https://pypi.org/simple/' -Method Head -TimeoutSec 10).StatusCode",
    ]
    story.append(make_code_box("PowerShell Lab Network Diagnostic (Run T-7 Days)", net_cmd, styles))
    story.append(Spacer(1, 6))

    story.append(make_callout(
        "CLASSROOM RATE-LIMIT & CONCURRENCY STRATEGY",
        "Groq free tier allows <b>30 requests/minute</b> per individual API key. Because every student uses their own "
        "free Groq account, 60 students never share a single rate bucket. However, an unguarded while-loop can still "
        "burn a student's 30 RPM quota in seconds. Enforce two rules from Day 1: (1) always set <code>max_steps=10</code>, "
        "and (2) add <code>time.sleep(0.5)</code> between tool calls if students see HTTP 429 errors. Keep "
        "<code>llama-3.1-8b-instant</code> ready as an instant high-quota fallback.",
        styles, border_color="#1E3A8A", bg_color="#EFF6FF",
    ))
    story.append(PageBreak())

    # -------------------- CHAPTER 2: PEDAGOGY & WHITEBOARD --------------------
    add_chapter_header(story, "Chapter 2", "Pedagogical Strategy, Talk Tracks & Whiteboard Delivery", styles)

    story.append(Paragraph("2.1 Day 1 Session 1 Icebreaker & Baseline Survey (09:30 - 10:15)", styles["H2"]))
    story.append(Paragraph(
        "Third-year ECE students have strong hardware and signal-processing instincts, but their Python fluency "
        "varies widely. Use the first 45 minutes of Morning Theory Session 1 to build psychological safety, expose misconceptions playfully, "
        "and gauge coding comfort before touching the keyboard:",
        styles["Body"],
    ))
    story.append(Paragraph("&bull; <b>Opening Poll 1:</b> <i>'Raise your hand if you have used ChatGPT or Gemini for assignments.'</i> (Expect ~95% hands up.)", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Opening Poll 2:</b> <i>'Keep your hand up if you have written a Python script that called an AI API.'</i> (Expect ~15-20%.)", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Opening Poll 3:</b> <i>'Keep it up if you have built an AI that executed 4 independent steps, caught its own error, consulted memory, and finished a task without you typing a second prompt.'</i> (Expect zero hands.)", styles["Bullet"]))
    story.append(Paragraph("&bull; <b>Hook Statement:</b> <i>'That gap is why we are here. By Friday afternoon, every single person in this room will build and defend a live autonomous engineering agent from scratch.'</i>", styles["Bullet"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 The Whiteboard Mental Model Reset (10:15 - 11:00)", styles["H2"]))
    story.append(Paragraph(
        "Write the college misconception verbatim at the top of the whiteboard: <i>'AI reads my emails and summarizes "
        "them on demand = Agentic AI.'</i> Then ask the class: <i>'Who decided WHEN to read emails? Who decided WHICH "
        "tool to call? What happens if the inbox API returns an error?'</i> Students quickly realize the human and "
        "the hardcoded script made every decision. Then draw Figure 2.1 on the board step by step.",
        styles["Body"],
    ))

    story.extend(make_diagram(
        "diag_autonomy_spectrum.png",
        "Figure 2.1: Reference diagram for the Day 1 whiteboard lecture contrasting Level 1 passive calls vs. Level 3 agency.",
        styles,
    ))

    story.append(Paragraph("2.3 Classroom Pacing & The Day 4 Authority Transition", styles["H2"]))
    story.append(Paragraph(
        "<b>Handling Mixed Coding Speeds (Days 1–3):</b> Never let faster students sit idle or slower students fall "
        "irreversibly behind. Push every completed lab milestone to a public reference branch on GitHub at the end of "
        "each session so stuck students can inspect diffs cleanly. Give fast finishers stretch challenges (such as "
        "adding cosine distance filtering thresholds or printing token cost estimates).",
        styles["Body"],
    ))

    story.append(make_callout(
        "VERBATIM DAY 3 CLOSING SCRIPT (16:50)",
        "<i>'Over the last three days, we built a Vector RAG pipeline, turned it into episodic memory, and wired an "
        "autonomous ReAct loop together. Starting tomorrow at 09:30, my role changes completely. I am no longer your "
        "pair programmer — I am your engineering reviewer. Do not ask me to fix your syntax errors or tracebacks. "
        "Read your terminal logs, inspect your JSON schemas, test your tools in isolation, and engineer a system you "
        "can defend live on Friday afternoon.'</i>",
        styles, border_color="#EA580C", bg_color="#FFF7ED",
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("2.4 Classroom Q&amp;A Cheat Sheet (Anticipated Student Questions)", styles["H2"]))
    qa_headers = ["Common Student Question", "Crisp, Authoritative Instructor Answer"]
    qa_rows = [
        ["Why not use LangChain or CrewAI?", "Frameworks hide the while-loop and JSON schemas behind abstractions. Learning pure Python first lets you debug ANY framework later."],
        ["Why ChromaDB instead of MongoDB / MariaDB?", "ChromaDB is vector-native with built-in ONNX embeddings and HNSW search via one pip install — zero database server admin required."],
        ["Can we run Ollama locally instead of Groq?", "A 70B model requires 40+ GB VRAM. Cloud API inference ensures every student laptop runs fast and identically without hardware barriers."],
        ["How is an agent different from an if-else script?", "An if-else script only handles paths the developer predicted. An agent reasons over unexpected tool outputs and errors at runtime."],
    ]
    story.append(make_table(qa_headers, qa_rows, [165, 321], styles))
    story.append(PageBreak())

    # -------------------- CHAPTER 3: LIVE DEMOS --------------------
    add_chapter_header(story, "Chapter 3", "Live Classroom Demonstrations & Projector Scripts", styles)

    story.append(Paragraph(
        "Four carefully timed live demonstrations anchor the entire curriculum. Always test every demo on the "
        "projector laptop 15 minutes before the session begins so network or syntax surprises never derail momentum.",
        styles["Body"],
    ))

    story.append(Paragraph("3.1 Demo 1 (Day 1 Session 2): Zero-Keyword Semantic Matching", styles["H2"]))
    story.append(Paragraph(
        "<b>Pedagogical Goal:</b> Prove visually that embeddings capture meaning, not word overlap. "
        "Project your terminal, point out that the word <i>'transistor'</i> never appears anywhere in Document 1 "
        "(which only mentions <i>'MOSFET'</i>), and run the query live:",
        styles["Body"],
    ))

    d1 = [
        "# Live Projector Demo 1 -- Run interactively via: uv run python demo1_semantic.py",
        "import chromadb",
        "col = chromadb.Client().create_collection('live_demo')",
        "col.add(",
        "    documents=[",
        "        'The MOSFET gate-to-source voltage controls channel drain current.',",
        "        'A capacitor stores electrical energy in an electric field.',",
        "        'Python uses indentation to delimit code blocks.',",
        "    ],",
        "    ids=['d1', 'd2', 'd3'],",
        ")",
        "res = col.query(query_texts=['How does a transistor amplify signals?'], n_results=2)",
        "for doc, dist in zip(res['documents'][0], res['distances'][0]):",
        "    print(f'Distance {dist:.3f} -> {doc}')",
    ]
    story.append(make_code_box("Instructor Live Demo 1: Semantic Proximity", d1, styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 Demo 2 (Day 1 Session 2): Grounded RAG vs. Hallucination Refusal", styles["H2"]))
    story.append(Paragraph(
        "<b>Pedagogical Goal:</b> Show students what they will build on Day 2 before they write a single line. "
        "Run <code>query.py</code> twice live: first with an in-domain electronics question (highlight the "
        "<code>[Source: file (chunk N)]</code> citation), then immediately with an out-of-domain sports question "
        "(highlight the clean refusal: <i>'Insufficient evidence in knowledge base.'</i>). Ask the class: "
        "<i>'Why did the model refuse even though Llama 3.3 knows who won the World Cup?'</i> Reinforce how "
        "system prompt grounding suppresses parametric hallucination.",
        styles["Body"],
    ))

    story.append(Paragraph("3.3 Demo 3 & 4 (Day 3): Multi-Step Agency & Self-Healing Fault Injection", styles["H2"]))
    story.append(Paragraph(
        "This is the single most memorable moment of the workshop. Deliberately pass an invalid sensor ID "
        "(<code>SENSOR_9999</code>) into your live agent. Let students watch the tool raise an error — and then "
        "watch the agent NOT crash, diagnose the error, inspect topology, locate active neighbor <code>SENSOR_042</code>, "
        "and complete the diagnosis autonomously.",
        styles["Body"],
    ))

    story.extend(make_diagram(
        "diag_error_recovery_flow.png",
        "Figure 3.1: Fault-interception flow projected during Demo 4 to illustrate autonomous self-healing.",
        styles,
    ))

    d4 = [
        "# Narrated Projector Trace for Live Demo 4 (Self-Healing)",
        "goal = 'Diagnose SENSOR_9999. If offline or missing, find an active neighbor and inspect it.'",
        "answer, trace = run_agent(goal)",
        "",
        "# Expected Live Terminal Output (Pause at each step and narrate!):",
        "# === Step 1 === Action: analyze_sensor_telemetry(sensor_id='SENSOR_9999')",
        "#   -> Observation: Tool Execution Error: SENSOR_9999 not found in sensor_logs.csv",
        "#   [INSTRUCTOR CUE: Pause here! Ask class: 'What would a normal Python script do right now? Crash!']",
        "# === Step 2 === Action: check_network_topology(sensor_id='SENSOR_9999')",
        "#   -> Observation: SENSOR_9999 decommissioned. Adjacent active node: SENSOR_042 (Subnet B).",
        "# === Step 3 === Action: analyze_sensor_telemetry(sensor_id='SENSOR_042')",
        "#   -> Observation: SENSOR_042 voltage=3.3V, temp=24.5C (Nominal).",
        "# === Step 4 === FINAL ANSWER: SENSOR_9999 is missing from active registry; neighbor SENSOR_042 verified healthy.",
    ]
    story.append(make_code_box("Instructor Live Demo 4: Fault Injection Script & Narration Cues", d4, styles))
    story.append(PageBreak())

    # -------------------- CHAPTER 4: REFERENCE CODE PART 1 --------------------
    add_chapter_header(story, "Chapter 4", "Production Reference Implementations: Vector RAG Engine", styles)

    story.append(Paragraph(
        "Keep these verified reference scripts open on your instructor machine during Days 1 and 2. "
        "Each block includes teaching notes highlighting the exact bugs 5th-semester students most commonly introduce.",
        styles["Body"],
    ))

    story.append(Paragraph("4.1 Complete Reference: ingest.py (With Teaching Notes)", styles["H2"]))
    ref_ingest = [
        "# reference/ingest.py -- Verified Instructor Reference Implementation",
        "import os",
        "import chromadb",
        "",
        "def chunk_with_overlap(text: str, max_chars: int = 400) -> list[str]:",
        "    sentences = [s.strip() for s in text.replace('\\n', ' ').split('. ') if s.strip()]",
        "    chunks, current = [], []",
        "    for s in sentences:",
        "        if len('. '.join(current + [s]) + '.') > max_chars and current:",
        "            chunks.append('. '.join(current) + '.')",
        "            current = [current[-1], s]  # 1-sentence sliding overlap",
        "        else:",
        "            current.append(s)",
        "    if current:",
        "        chunks.append('. '.join(current) + '.')",
        "    return chunks",
        "",
        "def run_ingestion(source_dir: str = 'knowledge_base'):",
        "    client = chromadb.PersistentClient(path='./chroma_db')",
        "    col = client.get_or_create_collection('rag_knowledge')",
        "    for fname in sorted(os.listdir(source_dir)):",
        "        if not fname.endswith(('.md', '.txt')):",
        "            continue",
        "        with open(os.path.join(source_dir, fname), 'r', encoding='utf-8') as f:",
        "            chunks = chunk_with_overlap(f.read())",
        "        ids = [f'{fname}_chunk_{i}' for i in range(len(chunks))]",
        "        metas = [{'source': fname, 'chunk_index': i} for i in range(len(chunks))]",
        "        col.upsert(documents=chunks, metadatas=metas, ids=ids)",
        "    print(f'Total vectors indexed in ChromaDB: {col.count()}')",
        "",
        "if __name__ == '__main__':",
        "    run_ingestion()",
    ]
    story.append(make_code_box("Reference: ingest.py", ref_ingest, styles))
    story.append(Paragraph(
        "<b>Watch For Student Bugs:</b> (1) Students forget <code>encoding='utf-8'</code> on Windows, causing "
        "<code>UnicodeDecodeError: 'charmap' codec can't decode</code> when reading markdown files with dashes or symbols. "
        "(2) Students call <code>col.add()</code> twice instead of <code>col.upsert()</code>, triggering duplicate ID warnings.",
        styles["Body"],
    ))

    story.append(Paragraph("4.2 Complete Reference: query.py (With Teaching Notes)", styles["H2"]))
    ref_query = [
        "# reference/query.py -- Verified Instructor Reference Implementation",
        "import json, os, urllib.request, chromadb",
        "from dotenv import load_dotenv",
        "load_dotenv()",
        "",
        "def query_rag(question: str, top_k: int = 3) -> str:",
        "    col = chromadb.PersistentClient(path='./chroma_db').get_collection('rag_knowledge')",
        "    res = col.query(query_texts=[question], n_results=top_k)",
        "    ctx = '\\n\\n'.join(",
        "        f\"[Source: {m['source']} (chunk {m['chunk_index']})] {d}\"",
        "        for d, m in zip(res['documents'][0], res['metadatas'][0])",
        "    )",
        "    sys_p = ('Answer ONLY from Context. If missing, say: Insufficient evidence. '",
        "             'Cite sources as [Source: filename (chunk N)].')",
        "    payload = {",
        "        'model': 'llama-3.3-70b-versatile',",
        "        'messages': [{'role': 'system', 'content': sys_p},",
        "                     {'role': 'user', 'content': f'Context:\\n{ctx}\\n\\nQuestion: {question}'}],",
        "        'temperature': 0.1, 'max_tokens': 512,",
        "    }",
        "    req = urllib.request.Request(",
        "        'https://api.groq.com/openai/v1/chat/completions',",
        "        data=json.dumps(payload).encode('utf-8'),",
        "        headers={'Authorization': f\"Bearer {os.environ['GROQ_API_KEY']}\", 'Content-Type': 'application/json'},",
        "    )",
        "    with urllib.request.urlopen(req, timeout=20) as resp:",
        "        return json.loads(resp.read().decode('utf-8'))['choices'][0]['message']['content']",
    ]
    story.append(make_code_box("Reference: query.py", ref_query, styles))
    story.append(Paragraph(
        "<b>Watch For Student Bugs:</b> Students frequently index <code>res['documents']</code> instead of "
        "<code>res['documents'][0]</code>. Remind the class that ChromaDB supports batch queries, so results are "
        "always nested lists where index <code>[0]</code> corresponds to the first query string.",
        styles["Body"],
    ))
    story.append(PageBreak())

    # -------------------- CHAPTER 5: REFERENCE CODE PART 2 --------------------
    add_chapter_header(story, "Chapter 5", "Production Reference Implementations: Agent, Memory & AAR", styles)

    story.append(Paragraph(
        "Use this unified reference implementation during Day 3 live coding to demonstrate how the ReAct loop, "
        "dynamic tool dispatch, ChromaDB episodic memory, and After Action Review compose cleanly in under 90 lines "
        "of readable Python.",
        styles["Body"],
    ))

    ref_agent = [
        "# reference/agent_full.py -- Complete Autonomous Agent + Episodic Memory + AAR",
        "import json, os, time, urllib.request, chromadb",
        "from dotenv import load_dotenv",
        "load_dotenv()",
        "",
        "TOOL_REGISTRY = {}",
        "def register_tool(func):",
        "    TOOL_REGISTRY[func.__name__] = func",
        "    return func",
        "",
        "mem_col = chromadb.PersistentClient(path='./agent_memory').get_or_create_collection('episodic')",
        "",
        "@register_tool",
        "def store_memory(category: str, observation: str) -> str:",
        "    mem_id = f'mem_{mem_col.count() + 1}'",
        "    mem_col.upsert(documents=[observation], metadatas=[{'cat': category}], ids=[mem_id])",
        "    return f'Stored {mem_id} under [{category}].'",
        "",
        "@register_tool",
        "def recall_memory(query: str, top_k: int = 3) -> str:",
        "    if mem_col.count() == 0: return 'Memory store is empty.'",
        "    res = mem_col.query(query_texts=[query], n_results=min(top_k, mem_col.count()))",
        "    return '\\n'.join(f\"[{m['cat']}] {d}\" for d, m in zip(res['documents'][0], res['metadatas'][0]))",
        "",
        "def call_groq(messages: list, tools: list | None = None) -> dict:",
        "    payload = {'model': 'llama-3.3-70b-versatile', 'messages': messages, 'temperature': 0.1, 'max_tokens': 1024}",
        "    if tools: payload.update({'tools': tools, 'tool_choice': 'auto'})",
        "    req = urllib.request.Request(",
        "        'https://api.groq.com/openai/v1/chat/completions',",
        "        data=json.dumps(payload).encode('utf-8'),",
        "        headers={'Authorization': f\"Bearer {os.environ['GROQ_API_KEY']}\", 'Content-Type': 'application/json'},",
        "    )",
        "    with urllib.request.urlopen(req, timeout=25) as resp:",
        "        return json.loads(resp.read().decode('utf-8'))",
        "",
        "def run_agent(goal: str, schemas: list, max_steps: int = 10) -> str:",
        "    sys_p = ('Autonomous agent with vector memory. Check recall_memory first. '",
        "             'Recover from tool errors. Emit FINAL ANSWER: when objective is verified.')",
        "    history = [{'role': 'system', 'content': sys_p}, {'role': 'user', 'content': goal}]",
        "    trace = []",
        "    for step in range(1, max_steps + 1):",
        "        msg = call_groq(history, tools=schemas)['choices'][0]['message']",
        "        if msg.get('tool_calls'):",
        "            history.append(msg)",
        "            for tc in msg['tool_calls']:",
        "                fn = tc['function']['name']",
        "                try:",
        "                    args = json.loads(tc['function']['arguments'] or '{}')",
        "                    out = str(TOOL_REGISTRY[fn](**args)) if fn in TOOL_REGISTRY else f'Unknown tool: {fn}'",
        "                except Exception as exc:",
        "                    out = f'Tool Error ({fn}): {exc}'",
        "                trace.append({'step': step, 'tool': fn, 'out': out[:200]})",
        "                history.append({'role': 'tool', 'tool_call_id': tc['id'], 'content': out[:2000]})",
        "                time.sleep(0.3)  # Gentle rate-limit cushion",
        "        elif 'FINAL ANSWER:' in msg.get('content', ''):",
        "            # Automatic After Action Review reflection",
        "            aar_p = f'Goal: {goal}\\nTrace: {trace}\\nGive ONE 20-word operational lesson:'",
        "            lesson = call_groq([{'role': 'user', 'content': aar_p}])['choices'][0]['message']['content'].strip()",
        "            store_memory('aar_lesson', lesson)",
        "            return msg['content']",
        "        else:",
        "            history.append(msg)",
        "    return 'HALTED: max_steps exceeded.'",
    ]
    story.append(make_code_box("Reference: agent_full.py (Complete Day 3 Solution)", ref_agent, styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Key Teaching Emphasis:</b> Point out line 43 (<code>history.append(msg)</code> BEFORE appending the "
        "<code>role: 'tool'</code> messages). If students forget to append the assistant's tool-call request message "
        "first, the Groq API immediately rejects the next request with HTTP 400 because a tool response lacks its "
        "matching <code>tool_call_id</code>.",
        styles["Body"],
    ))
    story.append(PageBreak())

    # -------------------- CHAPTER 6: MOCK DATA GENERATORS --------------------
    add_chapter_header(story, "Chapter 6", "Capstone Mock Dataset Generators & Lab Distribution", styles)

    story.append(Paragraph(
        "Run <code>generate_mock_data.py</code> during Day 3 Session 3 (14:00 - 17:00) to create rich, realistic telemetry and corpus "
        "datasets for all three capstone problem statements. Each dataset intentionally includes subtle anomalies "
        "and cross-referenced historical records so only a genuine multi-step agent with vector memory can diagnose "
        "the root cause accurately.",
        styles["Body"],
    ))

    mock_code = [
        "# generate_mock_data.py -- Generate Complete Capstone Datasets (Problems 1, 2 & 3)",
        "import csv, json, os",
        "",
        "def generate_all(base_dir: str = 'capstone_data'):",
        "    # --- PROBLEM 1: IoT Sensor Network Telemetry + Topology + Past Incidents ---",
        "    p1 = os.path.join(base_dir, 'problem_1_iot')",
        "    os.makedirs(p1, exist_ok=True)",
        "    with open(os.path.join(p1, 'sensor_logs.csv'), 'w', newline='', encoding='utf-8') as f:",
        "        w = csv.writer(f)",
        "        w.writerow(['timestamp', 'sensor_id', 'temp_c', 'humidity_pct', 'voltage_v', 'rssi_dbm'])",
        "        for i in range(1, 51):",
        "            # Inject two realistic faults: Node 17 battery drain; Node 34 thermistor open circuit",
        "            v = 1.82 if i == 17 else 3.30",
        "            t = 0.00 if i == 34 else round(24.0 + (i % 5) * 0.4, 2)",
        "            rssi = -96 if i == 17 else -64",
        "            w.writerow([f'2026-11-17T10:{i:02d}:00Z', f'SENSOR_{i:03d}', t, 54.0, v, rssi])",
        "",
        "    with open(os.path.join(p1, 'network_topology.json'), 'w', encoding='utf-8') as f:",
        "        json.dump({",
        "            'SENSOR_017': {'gateway': 'GW_EAST_02', 'status': 'degraded', 'neighbor': 'SENSOR_018'},",
        "            'SENSOR_034': {'gateway': 'GW_WEST_01', 'status': 'online', 'neighbor': 'SENSOR_035'},",
        "            'SENSOR_042': {'gateway': 'GW_NORTH_01', 'status': 'online', 'neighbor': 'SENSOR_041'},",
        "        }, f, indent=2)",
        "",
        "    with open(os.path.join(p1, 'past_incidents.json'), 'w', encoding='utf-8') as f:",
        "        json.dump([",
        "            {'id': 'INC_101', 'symptom': 'Supply voltage below 2.0V with RSSI drop below -90 dBm',",
        "             'root_cause': 'Lithium cell depletion causing radio brownout.', 'fix': 'Replace 3.6V Li-SOCl2 cell.'},",
        "            {'id': 'INC_102', 'symptom': 'Temperature reads flat 0.0C while voltage remains nominal 3.3V',",
        "             'root_cause': 'Open-circuit NTC thermistor lead.', 'fix': 'Resolder probe connector J2.'},",
        "        ], f, indent=2)",
        "",
        "    # --- PROBLEM 2: 5G NR Base Station RF Compliance Logs + 3GPP Thresholds ---",
        "    p2 = os.path.join(base_dir, 'problem_2_5g')",
        "    os.makedirs(p2, exist_ok=True)",
        "    with open(os.path.join(p2, 'firmware_test_output.json'), 'w', encoding='utf-8') as f:",
        "        json.dump({",
        "            'FW_v2.4': {'tx_power_dbm': 23.1, 'evm_pct': 9.8, 'freq_offset_hz': 45, 'aclr_db': 47.2},",
        "            'FW_v2.5': {'tx_power_dbm': 23.4, 'evm_pct': 6.1, 'freq_offset_hz': 142, 'aclr_db': 46.8},",
        "        }, f, indent=2)",
        "    with open(os.path.join(p2, '3gpp_thresholds.json'), 'w', encoding='utf-8') as f:",
        "        json.dump({'max_evm_pct': 8.0, 'max_freq_offset_hz': 100, 'min_aclr_db': 45.0}, f, indent=2)",
        "    with open(os.path.join(p2, 'past_compliance_tests.json'), 'w', encoding='utf-8') as f:",
        "        json.dump([",
        "            {'id': 'COMP_01', 'violation': 'EVM exceeds 8.0% on 64-QAM',",
        "             'resolution': 'Power amplifier clipping; back off DPD crest factor by 1.5 dB.'},",
        "            {'id': 'COMP_02', 'violation': 'Carrier frequency offset exceeds 100 Hz',",
        "             'resolution': 'TCXO reference clock drift; recalibrate PLL loop bandwidth.'},",
        "        ], f, indent=2)",
        "",
        "    # --- PROBLEM 3: Research Literature Survey Corpus ---",
        "    p3 = os.path.join(base_dir, 'problem_3_research')",
        "    os.makedirs(p3, exist_ok=True)",
        "    with open(os.path.join(p3, 'paper_abstracts.json'), 'w', encoding='utf-8') as f:",
        "        json.dump([",
        "            {'title': 'Event-Driven SNNs for Ultra-Low-Power Audio Keyword Spotting', 'year': 2024,",
        "             'method': 'Spiking Neural Network on Loihi-2', 'gap': 'Lacks noisy multi-speaker robustness.'},",
        "            {'title': 'Quantized TinyML Transformers on Cortex-M55 MCUs', 'year': 2025,",
        "             'method': 'INT4 post-training quantization', 'gap': 'High SRAM peak during self-attention.'},",
        "            {'title': 'Federated Learning over Lossy LoRaWAN Sensor Networks', 'year': 2025,",
        "             'method': 'Gradient sparsification', 'gap': 'No energy-aware client selection protocol.'},",
        "        ], f, indent=2)",
        "    print(f'All 3 capstone datasets generated cleanly under ./{base_dir}/')",
        "",
        "if __name__ == '__main__':",
        "    generate_all()",
    ]
    story.append(make_code_box("File: generate_mock_data.py (Run Day 3 Session 3)", mock_code, styles))
    story.append(PageBreak())

    # -------------------- CHAPTER 7: TROUBLESHOOTING PLAYBOOK --------------------
    add_chapter_header(story, "Chapter 7", "Classroom Troubleshooting & Live Error Playbook", styles)

    story.append(Paragraph(
        "During Days 1 through 3, keep this rapid-diagnosis table handy so classroom environment issues are resolved "
        "in under 60 seconds without stalling the whole batch:",
        styles["Body"],
    ))

    tr_headers = ["Symptom / Error Message", "Root Cause", "Exact Immediate Fix"]
    tr_rows = [
        ["'python' is not recognized in PowerShell", "Python 3.13 installed without checking 'Add python.exe to PATH'.",
         "Re-run Python installer -> Modify -> check 'Add Python to environment variables', then restart PowerShell."],
        ["PowerShell Activate.ps1 execution disabled", "Windows default Restricted execution policy.",
         "Run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass (or always use 'uv run python ...'!)."],
        ["HTTP 401 Unauthorized from Groq API", "Missing .env file, typo in GROQ_API_KEY, or forgot load_dotenv().",
         "Check .env has no extra quotes/spaces; verify key begins with gsk_ and load_dotenv() executes first."],
        ["HTTP 400 Bad Request on tool turn", "Student appended role='tool' without first appending assistant's msg.",
         "Ensure history.append(msg) runs immediately inside 'if msg.get(\"tool_calls\"):' before the tool loop."],
        ["HTTP 429 Too Many Requests", "Agent hit Groq's 30 RPM limit (often due to runaway while-loop).",
         "Enforce max_steps=10, insert time.sleep(0.5), or switch temporarily to llama-3.1-8b-instant."],
        ["UnicodeDecodeError: charmap codec", "Windows defaults open() to cp1252 instead of UTF-8.",
         "Always pass encoding='utf-8' to every open() call when reading/writing Markdown, CSV, or JSON."],
        ["ChromaDB hangs on first run", "Downloading 80 MB ONNX embedder over congested campus Wi-Fi.",
         "Copy pre-cached ~/.cache/chroma/onnx_models folder from instructor USB drive to student machine."],
        ["LLM calls tool with wrong JSON arg name", "Parameter name in TOOL_SCHEMAS does not match Python function signature.",
         "Verify exact spelling match between properties keys in TOOL_SCHEMAS and def func(...) arguments."],
    ]
    story.append(make_table(tr_headers, tr_rows, [122, 152, 212], styles))
    story.append(Spacer(1, 10))

    story.append(make_callout(
        "PRO TIP: ELIMINATE ACTIVATION ISSUES WITH 'UV RUN'",
        "Instruct students to execute all scripts via <code>uv run python script.py</code> rather than manually "
        "running <code>.venv\\Scripts\\Activate.ps1</code>. <code>uv run</code> automatically uses the project virtual "
        "environment on Windows while completely bypassing PowerShell execution policy errors.",
        styles, border_color="#1E3A8A", bg_color="#EFF6FF",
    ))
    story.append(PageBreak())

    # -------------------- CHAPTER 8: DAY 5 BENCHMARKS & VIVA --------------------
    add_chapter_header(story, "Chapter 8", "Day 5 Live Defense Benchmarks, Oral Viva & Grading Guide", styles)

    story.append(Paragraph(
        "During Day 5 Session 3 (14:00 - 17:00), evaluate each student or pair in a structured 10-minute live defense: "
        "<b>4 minutes</b> executing the unseen benchmark prompt live, <b>3 minutes</b> inspecting <code>agent.py</code> "
        "and <code>trace.jsonl</code>, and <b>3 minutes</b> answering targeted oral viva questions.",
        styles["Body"],
    ))

    story.append(Paragraph("8.1 Unseen Evaluation Benchmark Prompts (Reveal Live on Day 5)", styles["H2"]))
    story.append(make_callout(
        "LIVE BENCHMARK PROMPTS (DO NOT SHARE PRIOR TO DAY 5 DEFENSE)",
        "<b>Problem 1 (IoT Diagnostics):</b> <i>'Urgent Alert: SENSOR_034 is reporting suspicious flatline telemetry. "
        "Investigate sensor_logs.csv, inspect network_topology.json, check ChromaDB incident history for matching "
        "failure signatures, diagnose the exact root cause, and write a post-mortem report to workspace/sensor_034_audit.md.'</i><br/><br/>"
        "<b>Problem 2 (5G Protocol Compliance):</b> <i>'Urgent Alert: Base station build FW_v2.5 failed lab certification. "
        "Parse firmware_test_output.json for FW_v2.5, verify all RF parameters against 3GPP thresholds, consult "
        "compliance memory for the historical hardware remediation fix, and save audit to workspace/fw_v25_compliance.md.'</i><br/><br/>"
        "<b>Problem 3 (Research Literature Survey):</b> <i>'Research Goal: Evaluate hardware deployment bottlenecks for "
        "Quantized TinyML Transformers on Cortex-M microcontrollers versus LoRaWAN Federated Learning. Query stored "
        "literature memory, run a live web search for 2025/2026 benchmarks, identify top 2 research gaps, and write "
        "an annotated review to workspace/edge_ai_survey.md.'</i>",
        styles, border_color="#EA580C", bg_color="#FFF7ED",
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("8.2 Oral Defense Viva Question Bank", styles["H2"]))
    viva_headers = ["Topic", "Oral Examination Question", "What Proves True Understanding"]
    viva_rows = [
        ["Agency Proof", "Show me the exact line where the LLM — not your Python code — chooses the next tool.",
         "Points to msg['tool_calls'] and TOOL_REGISTRY[fn_name](**args) inside the for/while loop."],
        ["Self-Healing", "What happens if I pass SENSOR_9999 which does not exist in your CSV file?",
         "Explains try/except returns a 'Tool Error:' observation string so the LLM reflects instead of crashing."],
        ["Vector Math", "Why does ChromaDB use cosine similarity instead of counting matching words?",
         "Explains dense 384-dim embeddings capture semantic direction (e.g., MOSFET <-> transistor) regardless of length."],
        ["Memory Duality", "Why do we need ChromaDB episodic memory when the LLM already has a messages list?",
         "Explains short-term context resets per run and hits token limits; ChromaDB persists lessons across sessions."],
        ["Loop Safety", "How do you guarantee your agent will not burn your entire Groq quota in an infinite loop?",
         "Points to max_steps guardrail and observation string truncation ([:2000])."],
        ["Security", "Why did you use os.path.basename() or AST inside your tools?",
         "Explains blocking directory traversal ('../') and preventing arbitrary code execution via raw eval()."],
    ]
    story.append(make_table(viva_headers, viva_rows, [82, 184, 220], styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("8.3 Anti-Cheating Red Flags Checklist", styles["H2"]))
    story.append(make_callout(
        "IMMEDIATE ZERO-POINT TRIGGERS ON 'AUTONOMOUS CONTROL FLOW' (20 PTS)",
        "&bull; <b>Red Flag 1 (Hardcoded Pipeline):</b> Code calls <code>analyze_telemetry()</code> then <code>query_memory()</code> then <code>write_report()</code> sequentially in Python instead of letting the LLM emit tool calls dynamically.<br/>"
        "&bull; <b>Red Flag 2 (Brittle Crash):</b> Injecting a typo or unknown sensor ID crashes the terminal with an uncaught Python traceback.<br/>"
        "&bull; <b>Red Flag 3 (Fake Memory):</b> Student reads a static JSON file directly instead of querying ChromaDB vectors semantically.<br/>"
        "&bull; <b>Red Flag 4 (Leaked Credentials):</b> Student committed a plaintext <code>GROQ_API_KEY</code> into GitHub (deduct Code Quality points and require immediate key rotation).",
        styles, border_color="#1E3A8A", bg_color="#EFF6FF",
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("8.4 Printable Day 5 Live Defense Scorecard", styles["H2"]))
    score_headers = ["Team / USN", "Prob", "P1 /30", "Loop /20", "Mem /15", "Tools /10", "Heal /10", "Viva /10", "Code /5", "Total"]
    score_rows = [
        ["1.", "", "", "", "", "", "", "", "", ""],
        ["2.", "", "", "", "", "", "", "", "", ""],
        ["3.", "", "", "", "", "", "", "", "", ""],
        ["4.", "", "", "", "", "", "", "", "", ""],
        ["5.", "", "", "", "", "", "", "", "", ""],
        ["6.", "", "", "", "", "", "", "", "", ""],
        ["7.", "", "", "", "", "", "", "", "", ""],
        ["8.", "", "", "", "", "", "", "", "", ""],
    ]
    story.append(make_table(score_headers, score_rows, [86, 36, 44, 48, 48, 48, 44, 44, 44, 44], styles))

    doc.build(story, canvasmaker=get_a4_canvas_class(
        "VAP INSTRUCTOR PREPARATION HANDBOOK",
        "FACULTY MANUAL | ACHARYA INSTITUTE OF TECHNOLOGY",
    ))
    print(f"Instructor Guide PDF built: {output_path}")


# ======================================================================
# DOCUMENT 3: PRE-WORKSHOP STUDENT SETUP & INSTALLATION GUIDE (A4)
# ======================================================================
def build_pre_workshop_guide(output_path: str):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=54, rightMargin=54, topMargin=56, bottomMargin=54,
    )
    styles = setup_styles()
    story = []

    # Compact executive Page-1 banner (pure white background)
    top_bar = Table([["", ""]], colWidths=[110, CONTENT_W - 110])
    top_bar.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (0, 0), 4.0, colors.HexColor("#EA580C")),
        ("LINEBELOW", (1, 0), (1, 0), 4.0, colors.HexColor("#1E3A8A")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(top_bar)
    story.append(Spacer(1, 12))
    story.append(Paragraph("5-DAY VALUE ADDED PROGRAM  |  PRE-WORKSHOP SETUP GUIDE", styles["ChapterTag"]))
    story.append(Paragraph(
        "Pre-Workshop Software Installation &amp; Environment Readiness",
        ParagraphStyle(
            "PreTitle", parent=styles["H1"], fontSize=20.0, leading=24.0, spaceAfter=4,
        ),
    ))
    story.append(Paragraph(
        "Department of ECE, Acharya Institute of Technology  |  Complete BEFORE Day 1 (09:30 AM)",
        ParagraphStyle(
            "PreSub", parent=styles["Body"], fontSize=9.8, leading=13.5,
            textColor=colors.HexColor("#475569"), spaceAfter=10,
        ),
    ))

    story.append(make_callout(
        "WHY FINISH THIS BEFORE DAY 1?",
        "Installing Python, Git, Antigravity IDE, and libraries takes 15 to 20 minutes and downloads ~150 MB. "
        "Do these steps at home to avoid slow Wi-Fi in class. Your laptop is then ready when "
        "Session 1 starts at <b>09:30 AM</b>.",
        styles, border_color="#1E3A8A", bg_color="#FFFFFF",
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Minimum Laptop and Environment Specifications", styles["H2"]))
    spec_headers = ["Item", "Minimum Specification", "Notes"]
    spec_rows = [
        ["Operating System", "Windows 10 or Windows 11 (64-bit)", "Run all setup and lab commands in PowerShell."],
        ["Memory (RAM)", "4 GB min (8 GB recommended)", "Enough for Antigravity IDE and Python packages."],
        ["Free Disk Space", "5 GB free SSD or HDD space", "Holds Python 3.13, uv packages, and local caches."],
        ["Processor / GPU", "Any dual-core CPU (No GPU needed)", "The lab uses cloud APIs. Zero local GPU setup needed."],
        ["Internet Access", "Wi-Fi or Mobile Hotspot (HTTPS)", "Needed to install packages and test API links."],
    ]
    story.append(make_table(spec_headers, spec_rows, [96, 154, 236], styles))
    story.append(PageBreak())

    # -------------------- PAGE 2: STEPS 1 TO 4 --------------------
    add_chapter_header(story, "Section 2", "Install Core Tools (Steps 1-4)", styles)

    story.append(Paragraph("Step 1: Install Python 3.13 (Set PATH Box)", styles["H3"]))
    story.append(Paragraph(
        "&bull; Download the <b>Python 3.13.x</b> Windows 64-bit installer from <code>https://www.python.org/downloads/</code>.<br/>"
        "&bull; On the first screen, select <b>Add python.exe to PATH</b> before you click Install Now.<br/>"
        "&bull; Open a new <b>PowerShell</b> window and run <code>python --version</code>. Check that it prints <code>Python 3.13.x</code>.",
        styles["Bullet"],
    ))
    story.append(make_callout(
        "IMPORTANT PATH WARNING",
        "If you do not select <b>Add python.exe to PATH</b>, PowerShell prints <i>'python is not recognized'</i>. "
        "Run the installer again, click <b>Modify -&gt; Next -&gt; Add Python to environment variables</b>, then restart PowerShell.",
        styles, border_color="#B91C1C", bg_color="#FFFFFF",
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Step 2: Install uv (Fast Python Manager)", styles["H3"]))
    story.append(Paragraph(
        "Use <code>uv</code> instead of manual virtualenvs so lab packages install in seconds.",
        styles["Body"],
    ))
    story.append(make_code_box("PowerShell: Install and Check uv", [
        "pip install uv",
        "uv --version",
        "# If PowerShell cannot find uv, run: python -m uv --version",
    ], styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Step 3: Install Git and Set User Details", styles["H3"]))
    story.append(Paragraph(
        "&bull; Download and install Git from <code>https://git-scm.com/download/win</code> with default options.<br/>"
        "&bull; Set your name and email once in PowerShell before you push code to GitHub:",
        styles["Bullet"],
    ))
    story.append(make_code_box("PowerShell: Set Git Name and Email", [
        'git config --global user.name "Your Full Name"',
        'git config --global user.email "your.email@example.com"',
        "git --version",
    ], styles))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Step 4: Create a GitHub Account and Repo", styles["H3"]))
    story.append(Paragraph(
        "&bull; Sign in or create a free account at <code>https://github.com</code>.<br/>"
        "&bull; Create an empty repository named <code>vap-agentic-ai</code>.",
        styles["Bullet"],
    ))
    story.append(PageBreak())

    # -------------------- PAGE 3: IDE, GROQ KEY & WORKSPACE SETUP (STEPS 5-7) --------------------
    add_chapter_header(story, "Section 3", "Antigravity IDE, Groq Key, and Folder Setup (Steps 5-7)", styles)

    story.append(Paragraph("Step 5: Install Antigravity IDE (Standalone x64 Version)", styles["H3"]))
    story.append(Paragraph(
        "&bull; Open <code>https://antigravity.dev</code> and download the <b>Standalone IDE (x64)</b> file for Windows. "
        "Do <b>not</b> download the standard Antigravity file.<br/>"
        "&bull; Run the Standalone x64 installer, click <b>Open Folder</b>, and open the terminal with <code>Ctrl + ~</code>.",
        styles["Bullet"],
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Step 6: Create a Free Groq API Key", styles["H3"]))
    story.append(Paragraph(
        "&bull; Open <code>https://console.groq.com</code> and create a free developer account.<br/>"
        "&bull; Open <b>API Keys -&gt; Create API Key</b>, enter <code>vap-workshop</code>, and copy the <code>gsk_...</code> key.",
        styles["Bullet"],
    ))
    story.append(Spacer(1, 4))
    story.append(make_callout(
        "SECRET SAFETY RULE",
        "NEVER paste your <code>gsk_...</code> API key into any <code>.py</code> file, screenshot, or chat text, "
        "and NEVER push <code>.env</code> to GitHub. GitHub scanners revoke leaked keys in seconds.",
        styles, border_color="#EA580C", bg_color="#FFFFFF",
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Step 7: Set Up vap-agentic-ai and Install Libraries", styles["H3"]))
    story.append(Paragraph(
        "Run these commands once in the Antigravity IDE terminal to install packages (~100 MB) and create "
        "<code>.gitignore</code> before you add code files:",
        styles["Body"],
    ))
    story.append(make_code_box("PowerShell: Folder and Package Setup", [
        "mkdir vap-agentic-ai; cd vap-agentic-ai",
        "uv init",
        "uv add chromadb requests python-dotenv pydantic duckduckgo-search",
        "",
        "# Create .gitignore BEFORE your first git add",
        '@(".env", "__pycache__/", "*.pyc", ".venv/", "chroma_db/") |',
        '  Set-Content -Encoding utf8 .gitignore',
        "",
        "# Put your real Groq key into .env (no spaces around =, no quotes)",
        'Set-Content -Encoding utf8 .env "GROQ_API_KEY=gsk_replace_with_your_real_key"',
    ], styles))
    story.append(PageBreak())

    # -------------------- PAGE 4: 60-SECOND VERIFICATION TEST (STEP 8) --------------------
    add_chapter_header(story, "Section 4", "60-Second Setup Check (Step 8)", styles)

    story.append(Paragraph(
        "Create a file named <code>verify.py</code> inside <code>vap-agentic-ai</code> and run "
        "<code>uv run python verify.py</code>. This tests Groq HTTPS access and local ChromaDB:",
        styles["Body"],
    ))
    story.append(make_code_box("File: verify.py (Run: uv run python verify.py)", [
        "import json, os, urllib.request, chromadb",
        "from dotenv import load_dotenv",
        "load_dotenv()",
        'hdrs = {"Authorization": f"Bearer {os.environ[\'GROQ_API_KEY\']}",',
        '        "Content-Type": "application/json"}',
        'body = json.dumps({"model": "llama-3.1-8b-instant", "max_tokens": 10,',
        '    "messages": [{"role": "user", "content": "Say hello in 1 word."}]}).encode()',
        'url = "https://api.groq.com/openai/v1/chat/completions"',
        "req = urllib.request.Request(url, data=body, headers=hdrs)",
        "with urllib.request.urlopen(req, timeout=20) as resp:",
        "    res = json.loads(resp.read())",
        'print("API Connected:", res["choices"][0]["message"]["content"])',
        'print("ChromaDB Version:", chromadb.__version__)',
    ], styles))
    story.append(Spacer(1, 8))
    story.append(make_code_box("Expected PowerShell Output", [
        "PS C:\\Users\\student\\vap-agentic-ai> python --version",
        "Python 3.13.x",
        "PS C:\\Users\\student\\vap-agentic-ai> uv --version",
        "uv 0.5.x",
        "PS C:\\Users\\student\\vap-agentic-ai> uv run python verify.py",
        "API Connected: Hello!",
        "ChromaDB Version: 0.6.x",
    ], styles))
    story.append(Spacer(1, 8))
    story.append(make_callout(
        "SETUP CHECK COMPLETE",
        "If all three commands print versions and <b>API Connected: Hello!</b> with zero HTTP errors, your laptop is ready.",
        styles, border_color="#15803D", bg_color="#FFFFFF",
    ))
    story.append(PageBreak())

    # -------------------- PAGE 5: TROUBLESHOOTING & ARRIVAL CHECKLIST --------------------
    add_chapter_header(story, "Section 5", "Quick Fixes and Day 1 Arrival Checklist", styles)

    story.append(Paragraph(
        "If a setup step fails on Windows, find the error below and run the fix before Day 1:",
        styles["Body"],
    ))
    tr_headers = ["Error Text", "Cause", "PowerShell Fix"]
    tr_rows = [
        ["'python' is not recognized", "PATH box missed during install",
         "Run Python 3.13 installer -> Modify -> select Add Python to PATH -> open new shell."],
        ["'uv' is not recognized", "Scripts folder missing from PATH",
         "Open a new PowerShell window, or run: python -m uv run python verify.py"],
        ["KeyError: 'GROQ_API_KEY'", "Notepad saved file as .env.txt",
         "Run 'ls -Force' in PowerShell. Rename with: Rename-Item .env.txt .env"],
        ["HTTP 401 Unauthorized", "Extra spaces or quotes in .env",
         "Keep only this line in .env: GROQ_API_KEY=gsk_... (no quotes, no spaces)."],
        ["HTTP 403 / SSL / Timeout", "Campus Wi-Fi firewall block",
         "Switch to mobile hotspot during uv add and verify.py commands."],
        ["ModuleNotFoundError: chromadb", "Ran 'python verify.py' directly",
         "Run scripts inside the uv environment: uv run python verify.py"],
    ]
    story.append(make_table(tr_headers, tr_rows, [122, 134, 230], styles))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Day 1 (09:30 AM) Readiness Checklist", styles["H2"]))
    arr_headers = ["Done?", "Item", "Check Rule"]
    arr_rows = [
        ["[  ]", "Laptop and Power Charger", "Windows 10 or 11 starts cleanly with >= 5 GB free disk space."],
        ["[  ]", "Python 3.13 + uv + Git", "'python --version', 'uv --version', and 'git --version' all pass."],
        ["[  ]", "Antigravity IDE + GitHub", "Antigravity Standalone x64 opens vap-agentic-ai; empty repo ready on GitHub."],
        ["[  ]", ".env + .gitignore Files", "GROQ_API_KEY saved in .env. .gitignore blocks .env and local caches."],
        ["[  ]", "verify.py Passes", "'uv run python verify.py' prints Groq reply and ChromaDB version."],
    ]
    story.append(make_table(arr_headers, arr_rows, [48, 138, 300], styles))
    story.append(Spacer(1, 10))

    story.append(make_callout(
        "READY FOR DAY 1 AT 09:30 AM",
        "When <code>verify.py</code> prints <b>API Connected</b> cleanly, your laptop setup is done. Bring your laptop and charger "
        "to the lab at <b>09:30 AM</b>.",
        styles, border_color="#15803D", bg_color="#FFFFFF",
    ))

    doc.build(story, canvasmaker=get_a4_canvas_class(
        "PRE-WORKSHOP STUDENT SETUP GUIDE",
        "5-DAY VAP | ACHARYA INSTITUTE OF TECHNOLOGY",
    ))
    print(f"Pre-Workshop Guide PDF built: {output_path}")


if __name__ == "__main__":
    vap_dir = r"C:\Users\lapto\Desktop\demo\BEN\VAP"
    os.makedirs(vap_dir, exist_ok=True)
    build_pre_workshop_guide(os.path.join(vap_dir, "VAP_Pre_Workshop_Setup_Guide.pdf"))
    build_student_guide(os.path.join(vap_dir, "VAP_Student_Workshop_Guide.pdf"))
    build_instructor_guide(os.path.join(vap_dir, "VAP_Instructor_Preparation_Guide.pdf"))
    print("All A4 VAP PDF guides built successfully.")
