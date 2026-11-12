import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 2: # Skip cover and TOC
            self.saveState()
            self.setFont("Times-Roman", 9.5)
            self.setFillColor(colors.HexColor("#555555"))
            # Header
            self.drawString(54, 746, "Complex Computing Problem Report | CS-428: Parallel and Distributed Computing")
            self.setStrokeColor(colors.HexColor("#D0D5DD"))
            self.setLineWidth(0.6)
            self.line(54, 738, 558, 738)
            
            # Footer
            self.line(54, 48, 558, 48)
            self.drawRightString(558, 36, f"Page {self._pageNumber} of {page_count}")
            self.drawString(54, 36, "Department of Computer & Information Systems Engineering, NED University")
            self.restoreState()

def generate_pdf():
    pdf_filename = "Complex_Computing_Problem_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=24,
        leading=28,
        alignment=1, # Center
        textColor=colors.HexColor("#1A252F")
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        alignment=1,
        textColor=colors.HexColor("#2C3E50")
    )

    dept_style = ParagraphStyle(
        'CoverDept',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12.5,
        leading=16.5,
        alignment=1,
        textColor=colors.HexColor("#333333")
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading1'],
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        spaceBefore=0,
        spaceAfter=10,
        textColor=colors.HexColor("#1A252F")
    )

    sub_heading = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading2'],
        fontName='Times-Bold',
        fontSize=11,
        leading=15,
        spaceBefore=6,
        spaceAfter=3,
        textColor=colors.HexColor("#2C3E50")
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14.5,
        spaceAfter=6,
        alignment=4, # Justify
        textColor=colors.HexColor("#222222")
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        leftIndent=16,
        firstLineIndent=-10,
        spaceAfter=4,
        alignment=4,
        textColor=colors.HexColor("#222222")
    )

    numbered_style = ParagraphStyle(
        'NumberedStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        leftIndent=16,
        firstLineIndent=-12,
        spaceAfter=4,
        alignment=4,
        textColor=colors.HexColor("#222222")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A252F")
    )

    story = []

    # =========================================================
    # PAGE 1: COVER PAGE
    # =========================================================
    story.append(Spacer(1, 26))
    story.append(Paragraph("Complex Computing Problem Report", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("CS-428: Parallel and Distributed Computing", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Final Year - Cyber Security", dept_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Batch: 2023", dept_style))
    story.append(Spacer(1, 22))

    # NED Logo
    logo_path = 'ned_logo.png' if os.path.exists('ned_logo.png') else 'ned_logo_1.png'
    if os.path.exists(logo_path):
        story.append(RLImage(logo_path, width=2.0*inch, height=2.0*inch))
    story.append(Spacer(1, 22))

    story.append(Paragraph("Group Members:", subtitle_style))
    story.append(Spacer(1, 10))

    members_data = [
        [Paragraph("<b>Mr. Ameem Akhtar</b> .........................................................", body_style), Paragraph("<b>(CR-23013)</b>", body_style)],
        [Paragraph("<b>Mr. Minhal Rizvi</b> .........................................................", body_style), Paragraph("<b>(CR-23017)</b>", body_style)],
        [Paragraph("<b>Mr. Muhammad Usman</b> .....................................................", body_style), Paragraph("<b>(CR-23038)</b>", body_style)],
        [Paragraph("<b>Mr. Maaz Wasim</b> .........................................................", body_style), Paragraph("<b>(CR-23041)</b>", body_style)],
    ]
    t_members = Table(members_data, colWidths=[3.8*inch, 1.8*inch])
    t_members.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_members)

    story.append(Spacer(1, 32))
    story.append(Paragraph("<b>Submitted to:</b> Dr. Saad Qasim Khan (Assistant Professor, CIS)", body_style))
    story.append(Paragraph("<b>Submission Date:</b> November 02, 2026", body_style))
    story.append(PageBreak())

    # =========================================================
    # PAGE 2: TABLE OF CONTENTS
    # =========================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("Table of Contents", section_heading))
    story.append(Spacer(1, 10))

    toc_rows = [
        ["S. No.", "Description", "Pg. No."],
        ["1", "Abstract", "3"],
        ["2", "Problem Introduction", "4"],
        ["3", "Sequential Implementation", "5"],
        ["4", "Parallel Implementation", "6"],
        ["5", "Simulation Results", "7"],
        ["6", "Conclusion", "8"],
        ["7", "Any added information (optional)", "9"]
    ]
    t_toc = Table(toc_rows, colWidths=[0.8*inch, 5.0*inch, 0.9*inch])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================
    # PAGE 3: ABSTRACT
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Abstract:", section_heading))
    
    story.append(Paragraph(
        "<b>Complex Computing Problem (CCP) Formulation:</b> In parallel computing, a Complex Computing Problem (CCP) is characterized by non-linear algorithmic time scaling, deep sequential data dependencies, and severe memory hierarchy contention that render naive single-threaded computing inefficient. Solving such problems requires holistic cross-layer engineering—ranging from loop dependency analysis and cache tile tuning to shared-memory thread orchestration under Amdahl's Law.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Project Focus:</b> This project investigates the performance optimization of the classical <b>Floyd–Warshall All-Pairs Shortest Path (APSP)</b> algorithm using <b>OpenMP in C</b>. The algorithm exhibits an asymptotic time complexity of &Theta;(<i>V</i><sup>3</sup>) and space complexity of &Theta;(<i>V</i><sup>2</sup>). In cybersecurity network analytics, APSP is essential for computing vulnerability reachability, mapping lateral movement pathways in enterprise Active Directory domains, identifying single-point-of-failure bottlenecks, and quantifying zero-trust blast radii. For large-scale network topologies (e.g., <i>V</i> = 2000), single-threaded execution requires billions of operations, creating an unacceptable latency barrier.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Methodology & Implementations:</b> To achieve scalable throughput, three distinct implementations were developed: (1) a baseline <b>Sequential Implementation</b> in C, (2) an <b>OpenMP Row-Parallel Implementation</b> distributing independent row calculations across multi-core threads, and (3) a <b>Cache-Blocked (Tiled) OpenMP Implementation</b> (default block size <i>B</i> = 64, with <i>B</i> &isin; {16, 32, 64, 128, 256} studied) engineered to maximize L1/L2 cache locality and prevent memory bus saturation.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Key Achievements:</b> Benchmarks were run on an Intel Core i7-9750H (6 cores / 12 hardware threads) across graph sizes <i>V</i> &isin; {500, 1000, 1500, 2000} using 1, 2, 4, and 8 threads, with every timing taken as the median of 3 runs. At <i>V</i> = 2000 (8 billion inner-loop operations), Standard OpenMP reduced runtime from 9.635s to 2.026s (<b>4.76x speedup</b>) and Cache-Blocked OpenMP to <b>1.969s</b> (<b>4.89x speedup</b>, 61% efficiency on 8 threads). Blocking gave its largest gain on small graphs (3.27x vs 1.70x at <i>V</i> = 500) because it needs far fewer barrier synchronizations; on large graphs the gain shrank to about 3%. A block-size study found <i>B</i> = 32-64 fastest. Correctness was verified on 1,224 test runs against an independent Bellman-Ford oracle, and every benchmark result was checked against the sequential output.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================
    # PAGE 4: PROBLEM INTRODUCTION
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Problem Introduction:", section_heading))
    story.append(Paragraph(
        "The All-Pairs Shortest Path (APSP) problem is a foundational problem in graph theory. Given a directed, weighted graph <i>G = (V, E)</i> where <i>V</i> represents vertices and <i>E</i> represents directed edges with weights <i>w(u, v)</i>, the goal is to determine the minimum path distance <i>D(i, j)</i> between every ordered pair of vertices (<i>i, j</i>).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Mathematical Formulation:</b> The Floyd–Warshall algorithm solves APSP using dynamic programming. Letting <i>D</i><sup>(<i>k</i>)</sup>[<i>i</i>][<i>j</i>] be the shortest path from vertex <i>i</i> to vertex <i>j</i> with intermediate vertices restricted to {0, 1, ..., <i>k</i>}, the recurrence relation is:",
        body_style
    ))

    eq_box = [
        [Paragraph("<font face='Courier' size=9.5><b>D<sup>(k)</sup>[i][j] = min( D<sup>(k-1)</sup>[i][j],  D<sup>(k-1)</sup>[i][k] + D<sup>(k-1)</sup>[k][j] )</b></font>", body_style)]
    ]
    t_eq = Table(eq_box, colWidths=[6.5*inch])
    t_eq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F2F6")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CED6E0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_eq)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Computational Complexity & Scaling:</b> The algorithm executes three nested loops of dimension <i>n</i>, resulting in a strict time complexity of &Theta;(<i>V</i><sup>3</sup>) and a memory space requirement of &Theta;(<i>V</i><sup>2</sup>). For an enterprise network graph of <i>V</i> = 2000 hosts, the inner loop executes exactly 2000<sup>3</sup> = <b>8,000,000,000 iterations</b>. On a single thread, this imposes heavy latency, making real-time path updates infeasible during active security events.",
        body_style
    ))
    story.append(Paragraph("<b>Cybersecurity Domain Application:</b>", sub_heading))
    story.append(Paragraph(
        "In modern cybersecurity infrastructure, rapid shortest path computations enable critical defensive workflows:",
        body_style
    ))
    # SEPARATE BULLETS ON NEW LINES WITH PROPER INDENTATION
    story.append(Paragraph(
        "&bull; <b>Attack Path Enumeration:</b> Network assets (workstations, DMZ gateways, AD domain controllers) are mapped as vertices. Edges represent exploitable communication channels with weights inverse to vulnerability risk (e.g., <i>w</i> = 10 - CVSS). APSP calculates the exact minimal-effort exploit path an adversary would traverse to reach crown-jewel assets.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Blast Radius Analysis:</b> When an endpoint is compromised by ransomware, APSP immediately reveals all subnets and resources within reachable lateral propagation thresholds, allowing instant automated quarantine.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Zero-Trust Segmentation:</b> Centrality and shortest-path frequency identify critical bridge nodes where firewalls, Intrusion Prevention Systems (IPS), and EDR telemetry must be prioritized.",
        bullet_style
    ))
    story.append(PageBreak())

    # =========================================================
    # PAGE 5: SEQUENTIAL IMPLEMENTATION
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Sequential Implementation:", section_heading))
    story.append(Paragraph(
        "The sequential implementation in C provides an optimized baseline for correctness and scalability comparison. A flat 1D contiguous array of size <i>N &times; N</i> is allocated via <font face='Courier'>malloc()</font> to represent the distance matrix, indexed via <font face='Courier'>dist[i * n + j]</font>.",
        body_style
    ))
    story.append(Paragraph("<b>Architectural Considerations:</b>", sub_heading))
    # SEPARATE NUMBERED ITEMS ON NEW LINES WITH PROPER INDENTATION
    story.append(Paragraph(
        "<b>1. Contiguous Row-Major Storage:</b> Avoids pointer-indirection overhead (e.g., <font face='Courier'>int**</font>), enabling hardware prefetchers to stream cache lines smoothly along the innermost loop.",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>2. Safe Infinity Representation:</b> Absent edges are initialized to <font face='Courier'>INF = 10<sup>9</sup></font>. This guarantees that <font face='Courier'>dist[i][k] + dist[k][j]</font> will never overflow a standard 32-bit signed integer.",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>3. Early Pruning:</b> The condition <font face='Courier'>if (dik == INF) continue;</font> prunes unreachable row paths before entering loop <i>j</i>, bypassing millions of unnecessary calculations on sparse and semi-dense topologies.",
        numbered_style
    ))
    story.append(Spacer(1, 4))

    code_seq_txt = (
        "void floyd_warshall_sequential(int *dist, int n) {\n"
        "    for (int k = 0; k < n; k++) {\n"
        "        for (int i = 0; i < n; i++) {\n"
        "            int dik = dist[i * n + k];\n"
        "            if (dik == INF) continue; // Early pruning\n"
        "            for (int j = 0; j < n; j++) {\n"
        "                int dkj = dist[k * n + j];\n"
        "                if (dkj != INF && dik + dkj < dist[i * n + j]) {\n"
        "                    dist[i * n + j] = dik + dkj;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}"
    )
    t_c1 = Table([[Preformatted(code_seq_txt, code_style)]], colWidths=[6.5*inch])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D1D8E0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_c1)
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Sequential Memory Bottleneck:</b> While traversing row <i>j</i> exhibits spatial locality, reading <font face='Courier'>dist[i * n + k]</font> accesses column <i>k</i> across iterations of <i>i</i>, causing frequent cache capacity evictions once matrix footprint exceeds the hardware L3 cache (e.g., 16 MB at <i>V</i> = 2000).",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================
    # PAGE 6: PARALLEL IMPLEMENTATION
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Parallel implementation:", section_heading))
    story.append(Paragraph("<b>Dependency Analysis:</b>", sub_heading))
    # SEPARATE BULLETS ON NEW LINES WITH PROPER INDENTATION
    story.append(Paragraph(
        "&bull; <b>Outer Loop k (Loop-Carried Dependency):</b> Iteration <i>k</i> strictly requires the completed state of iteration <i>k</i> - 1. Thus, outer loop <i>k</i> possesses a true data dependency and cannot be parallelized.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Inner Loops i and j (Data Independence):</b> During step <i>k</i>, row <i>k</i> (<font face='Courier'>dist[k][j]</font>) and column <i>k</i> (<font face='Courier'>dist[i][k]</font>) remain invariant because <font face='Courier'>dist[k][k] = 0</font>. Each thread updating row <i>i</i> writes exclusively to disjoint memory slices (<font face='Courier'>dist[i * n + j]</font>). Thus, the <i>i</i>-loop is embarrassingly parallel without write-write race hazards!",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    code_par_txt = (
        "void floyd_warshall_parallel(int *dist, int n, int num_threads) {\n"
        "    omp_set_num_threads(num_threads);\n"
        "    for (int k = 0; k < n; k++) {\n"
        "        #pragma omp parallel for schedule(static)\n"
        "        for (int i = 0; i < n; i++) {\n"
        "            int dik = dist[i * n + k];\n"
        "            if (dik == INF) continue;\n"
        "            for (int j = 0; j < n; j++) {\n"
        "                int dkj = dist[k * n + j];\n"
        "                if (dkj != INF && dik + dkj < dist[i * n + j]) {\n"
        "                    dist[i * n + j] = dik + dkj;\n"
        "                }\n"
        "            }\n"
        "        }\n"
        "    }\n"
        "}"
    )
    t_c2 = Table([[Preformatted(code_par_txt, code_style)]], colWidths=[6.5*inch])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D1D8E0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_c2)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Cache-Blocked (Tiled) Implementation:</b>", sub_heading))
    story.append(Paragraph(
        "To overcome the memory-bound nature of the standard parallel approach, the matrix is partitioned into <i>B &times; B</i> tiles (<i>B</i> = 64). Each step <i>k<sub>b</sub></i> proceeds through three synchronized phases:",
        body_style
    ))
    # SEPARATE BULLETS ON NEW LINES WITH PROPER INDENTATION
    story.append(Paragraph(
        "&bull; <b>Phase 1 (Diagonal Block):</b> Diagonal block (<i>k<sub>b</sub>, k<sub>b</sub></i>) is computed sequentially.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Phase 2 (Cross Blocks):</b> Cross row blocks (<i>k<sub>b</sub>, j<sub>b</sub></i>) and column blocks (<i>i<sub>b</sub>, k<sub>b</sub></i>) are updated concurrently in parallel using <font face='Courier'>#pragma omp parallel for</font>.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Phase 3 (Independent Blocks):</b> All remaining independent tiles (<i>i<sub>b</sub>, j<sub>b</sub></i>) are processed simultaneously using <font face='Courier'>#pragma omp parallel for collapse(2) schedule(static)</font>. Each kernel call reads and writes three <i>B &times; B</i> tiles (3 &times; 4 &times; <i>B</i><sup>2</sup> bytes: 12 KB at <i>B</i> = 32, 48 KB at <i>B</i> = 64), which stay inside each core's private L1/L2 cache (32 KB / 256 KB) instead of streaming from DRAM.",
        bullet_style
    ))
    story.append(PageBreak())

    # =========================================================
    # PAGE 7: SIMULATION RESULTS
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Simulation Results:", section_heading))
    story.append(Paragraph(
        "Empirical benchmarks were conducted on an Intel Core i7-9750H (6 cores / 12 hardware threads, 32 KB L1D + 256 KB L2 per core, 12 MB shared L3) using GCC 16.2.0 (<font face='Courier'>-O3 -fopenmp</font>). Each time is the median of 3 runs, and every parallel result was verified against the sequential output. In strict conformance with <b>CS-428 Lab 4 (Performance Analysis of Real OpenMP Applications)</b>, performance is analyzed across Speedup &psi;(<i>n, p</i>), Efficiency &epsilon;(<i>n, p</i>), and Parallel Cost <i>c(n, p) = p &times; T<sub>p</sub></i> (processor-seconds):",
        body_style
    ))

    # Table rows come straight from benchmark_results.csv so the report always matches the data
    res_table_data = [["Vertices (V)", "Algorithm Variant", "Threads", "Time (sec)", "Speedup ψ", "Efficiency ε", "Cost c(n,p)"]]
    with open('benchmark_results.csv') as f:
        for r in csv.DictReader(f):
            if r['Implementation'] == 'Sequential' or r['Threads'] == '8':
                t, p = float(r['ExecutionTime_Sec']), int(r['Threads'])
                res_table_data.append([r['Size'], r['Implementation'], r['Threads'], f"{t:.4f} s",
                                       f"{float(r['Speedup']):.2f}x", f"{float(r['Efficiency_Pct']):.1f}%", f"{p * t:.3f} p-s"])
    t_res = Table(res_table_data, colWidths=[0.9*inch, 1.45*inch, 0.65*inch, 0.85*inch, 0.85*inch, 0.9*inch, 0.9*inch])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (1,-1), 'LEFT'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9FA")])
    ]))
    story.append(t_res)
    story.append(Spacer(1, 8))

    # Figures Table
    if os.path.exists("runtime_comparison.png") and os.path.exists("cache_blocking_comparison.png"):
        img_row = [
            [
                RLImage("runtime_comparison.png", width=3.1*inch, height=1.85*inch),
                RLImage("cache_blocking_comparison.png", width=3.1*inch, height=1.85*inch)
            ],
            [
                Paragraph("<font size=8><i>Figure 1: Runtime vs Matrix Size (V)</i></font>", body_style),
                Paragraph("<font size=8><i>Figure 2: Standard vs Blocked OpenMP</i></font>", body_style)
            ]
        ]
        t_img = Table(img_row, colWidths=[3.25*inch, 3.25*inch])
        t_img.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('TOPPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(t_img)

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Performance Analysis:</b> Both parallel versions scale with graph size: at 8 threads the Standard OpenMP speedup rises from 1.70x (<i>V</i> = 500) to 4.76x (<i>V</i> = 2000), because larger graphs give each thread more work per synchronization barrier. The Cache-Blocked version is faster at every size, but its advantage falls from 1.9x at <i>V</i> = 500 to about 3% at <i>V</i> = 2000: on small graphs it wins mainly by replacing <i>V</i> barriers with 2<i>V</i>/<i>B</i> barriers, while on large graphs both versions are limited by memory bandwidth and by the 6 physical cores. With 1 thread, both OpenMP versions run at 0.72-1.02x of the sequential code, which measures the parallel overhead (thread start-up and the extra loop structure of blocking).",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================
    # PAGE 8: CONCLUSION
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Conclusion", section_heading))
    story.append(Paragraph("<b>Summary of Outcomes & Achieved Speedups:</b>", sub_heading))
    story.append(Paragraph(
        "This project successfully designed, implemented, and benchmarked parallel optimizations for the Floyd–Warshall All-Pairs Shortest Path algorithm on multi-core architectures. The key performance conclusions include:",
        body_style
    ))
    # SEPARATE BULLETS ON NEW LINES WITH PROPER INDENTATION
    story.append(Paragraph(
        "&bull; <b>Standard OpenMP:</b> Reached <b>4.76x speedup</b> on 8 threads at <i>V</i> = 2000 (2.026s vs 9.635s sequential) and <b>3.52x</b> at <i>V</i> = 1000 (0.327s vs 1.150s).",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Cache-Blocked OpenMP:</b> Reached <b>4.89x speedup</b> at <i>V</i> = 2000 (1.969s) and <b>4.29x</b> at <i>V</i> = 1000 (0.268s). Blocking beat standard parallelization at every size: by 92% at <i>V</i> = 500, 22% at <i>V</i> = 1000 and about 3% at <i>V</i> = 2000. Block sizes <i>B</i> = 32 and 64 were fastest; <i>B</i> = 256 was slowest because its three active tiles (768 KB) no longer fit in the 256 KB L2 cache.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Amdahl's Law and Scaling Bottlenecks:</b>", sub_heading))
    story.append(Paragraph(
        "Linear speedup (<i>S = p</i>) was bounded by hardware and algorithmic factors:",
        body_style
    ))
    # SEPARATE NUMBERED ITEMS ON NEW LINES WITH PROPER INDENTATION
    story.append(Paragraph(
        "<b>1. Synchronization Barriers:</b> The outer <i>k</i> loop necessitates <i>N</i> barrier synchronizations (2,000 barriers at <i>V</i> = 2000), incurring thread scheduling jitter.",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>2. Memory Bandwidth Saturation:</b> The naive algorithm possesses an arithmetic intensity of ~0.17 FLOPs/byte. Multiple cores streaming non-contiguous column elements from main RAM saturate memory channels, causing CPU stall cycles.",
        numbered_style
    ))
    story.append(Paragraph(
        "<b>3. Physical Core Limit:</b> The i7-9750H has 6 physical cores, so the 8-thread runs place two threads on some cores through Hyper-Threading, where they share execution units and L1/L2 caches. This caps 8-thread efficiency near 60%.",
        numbered_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Significance for Cybersecurity Engineering:</b>", sub_heading))
    story.append(Paragraph(
        "Accelerating all-pairs shortest path analysis transforms static security audits into dynamic real-time defense. By slashing computational latency to sub-second durations for thousand-node topologies, defensive teams can continuously monitor lateral attack propagation, quantify real-time blast radius boundaries during active malware outbreaks, and dynamically enforce Zero-Trust micro-segmentation.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================
    # PAGE 9: ANY ADDED INFORMATION
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Any added information", section_heading))
    story.append(Paragraph("<b>1. Cybersecurity Case Study: Attack Path Reachability & Blast Radius Modeling</b>", sub_heading))
    story.append(Paragraph(
        "To demonstrate the cybersecurity application, <font face='Courier'>main_benchmark.c</font> runs the OpenMP Floyd-Warshall solver on an 8-node enterprise attack graph (step [2/3] of the program):",
        body_style
    ))
    # SEPARATE BULLETS ON NEW LINES WITH PROPER INDENTATION
    story.append(Paragraph(
        "&bull; <b>Network Assets:</b> Phished-PC, Web-DMZ, VPN-Gateway, HR-Workstation, File-Server, SQL-Database, Jump-Host and Domain-Controller. Nine directed edges model exploitable channels (reused password, SQL injection, open SMB share, stored RDP credentials, admin session).",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Edge Weights:</b> Each weight is the attacker effort to pivot (lower = easier), e.g. <i>W(u, v) = 10 - CVSS_Exploitability</i>.",
        bullet_style
    ))
    story.append(Paragraph(
        "&bull; <b>Result:</b> Minimum-effort path Phished-PC -&gt; HR-Workstation -&gt; File-Server -&gt; Jump-Host -&gt; Domain-Controller (effort 11), cheaper than the direct HR-Workstation -&gt; Domain-Controller route (14) and the Web-DMZ -&gt; SQL-Database route (18). Blast radius within effort 7: HR-Workstation (2), File-Server (5), Web-DMZ (6), Jump-Host (7). The program checks this against the hand-computed answer and fails if it differs.",
        bullet_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2. Roofline Model & Speedup Visualizations</b>", sub_heading))
    story.append(Paragraph(
        "Because Floyd-Warshall executes 2 memory reads and 1 write for every addition and comparison, it is memory-bandwidth bound. A tile kernel touches 3 &times; 4 &times; <i>B</i><sup>2</sup> bytes, and the block-size study (Figure 5) shows the effect directly: <i>B</i> = 32 (12 KB, fits L1) and <i>B</i> = 64 (48 KB, fits L2) are fastest and within about 6% of each other; <i>B</i> = 128 (192 KB) is close on large graphs but clearly slower at <i>V</i> = 500; <i>B</i> = 256 (768 KB) exceeds the 256 KB L2 cache and is the slowest at every size; <i>B</i> = 16 is also slower because loop overhead dominates such small tiles.",
        body_style
    ))

    if os.path.exists("speedup_analysis.png") and os.path.exists("efficiency_plot.png"):
        img_row2 = [
            [
                RLImage("speedup_analysis.png", width=3.1*inch, height=1.85*inch),
                RLImage("efficiency_plot.png", width=3.1*inch, height=1.85*inch)
            ],
            [
                Paragraph("<font size=8><i>Figure 3: Speedup vs Thread Count</i></font>", body_style),
                Paragraph("<font size=8><i>Figure 4: Parallel Efficiency (%) vs Threads</i></font>", body_style)
            ]
        ]
        t_img2 = Table(img_row2, colWidths=[3.25*inch, 3.25*inch])
        t_img2.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ('TOPPADDING', (0,0), (-1,-1), 1),
        ]))
        story.append(t_img2)

    if os.path.exists("block_size_analysis.png"):
        story.append(Spacer(1, 4))
        story.append(RLImage("block_size_analysis.png", width=3.6*inch, height=2.15*inch))
        story.append(Paragraph("<font size=8><i>Figure 5: Block Size vs Speedup (Blocked OpenMP, 8 threads)</i></font>", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {pdf_filename}")

if __name__ == '__main__':
    generate_pdf()
