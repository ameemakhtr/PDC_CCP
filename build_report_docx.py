import csv
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_bullet_item(doc, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r_b = p.add_run("•  ")
    r_b.font.name = 'Times New Roman'
    r_b.font.size = Pt(10.5)
    r_b.bold = True
    if title:
        r_t = p.add_run(title + " ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10.5)
        r_t.bold = True
    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(10.5)

def add_num_item(doc, num_str, title, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.15)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r_n = p.add_run(num_str + "  ")
    r_n.font.name = 'Times New Roman'
    r_n.font.size = Pt(10.5)
    r_n.bold = True
    if title:
        r_t = p.add_run(title + " ")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10.5)
        r_t.bold = True
    r_txt = p.add_run(text)
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(10.5)

def create_docx_report():
    doc = docx.Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
    # Styles setup
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # PAGE 1: TITLE / COVER PAGE
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(28)
    p_title.paragraph_format.space_after = Pt(8)
    run_title = p_title.add_run("Complex Computing Problem Report")
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(24)
    run_title.bold = True
    run_title.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(4)
    run_course = p_course.add_run("CS-428: Parallel and Distributed Computing")
    run_course.font.name = 'Times New Roman'
    run_course.font.size = Pt(16)
    run_course.bold = True

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(4)
    run_dept = p_dept.add_run("Final Year - Cyber Security")
    run_dept.font.name = 'Times New Roman'
    run_dept.font.size = Pt(13)

    p_batch = doc.add_paragraph()
    p_batch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_batch.paragraph_format.space_after = Pt(20)
    run_batch = p_batch.add_run("Batch: 2023")
    run_batch.font.name = 'Times New Roman'
    run_batch.font.size = Pt(12)

    # Logo
    logo_path = 'ned_logo.png' if os.path.exists('ned_logo.png') else 'ned_logo_1.png'
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(24)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(2.0))

    # Group Members
    p_gm = doc.add_paragraph()
    p_gm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_gm.paragraph_format.space_after = Pt(12)
    run_gm = p_gm.add_run("Group Members:")
    run_gm.font.name = 'Times New Roman'
    run_gm.font.size = Pt(14)
    run_gm.bold = True

    # Members Table
    table_members = doc.add_table(rows=4, cols=2)
    table_members.alignment = WD_TABLE_ALIGNMENT.CENTER
    members_data = [
        ("Mr. Ameem Akhtar", "CR-23013"),
        ("Mr. Minhal Rizvi", "CR-23017"),
        ("Mr. Muhammad Usman", "CR-23038"),
        ("Mr. Maaz Wasim", "CR-23041")
    ]
    for i, (name, roll) in enumerate(members_data):
        row = table_members.rows[i]
        cell_name = row.cells[0]
        cell_roll = row.cells[1]
        
        cell_name.width = Inches(3.2)
        cell_roll.width = Inches(1.8)
        
        p0 = cell_name.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(f"{name} " + ".".ljust(25, '.'))
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)

        p1 = cell_roll.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(f"({roll})")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.bold = True

    # Spacing
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(28)
    p_space.paragraph_format.space_after = Pt(4)

    # Submitted to
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("Submitted to: Dr. Saad Qasim Khan (Assistant Professor, CIS)")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.bold = True

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_date.paragraph_format.space_after = Pt(0)
    r_date = p_date.add_run("Submission Date: November 02, 2026")
    r_date.font.name = 'Times New Roman'
    r_date.font.size = Pt(11)

    # -------------------------------------------------------------
    # PAGE 2: TABLE OF CONTENTS
    # -------------------------------------------------------------
    doc.add_page_break()

    p_toc_head = doc.add_paragraph()
    p_toc_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_toc_head.paragraph_format.space_before = Pt(14)
    p_toc_head.paragraph_format.space_after = Pt(14)
    r_th = p_toc_head.add_run("Table of Contents")
    r_th.font.name = 'Times New Roman'
    r_th.font.size = Pt(16)
    r_th.bold = True

    toc_table = doc.add_table(rows=8, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_data = [
        ("S. No.", "Description", "Pg. No."),
        ("1", "Abstract", "3"),
        ("2", "Problem Introduction", "4"),
        ("3", "Sequential Implementation", "5"),
        ("4", "Parallel Implementation", "6"),
        ("5", "Simulation Results", "7"),
        ("6", "Conclusion", "8"),
        ("7", "Any added information (optional)", "9")
    ]
    for row_idx, data in enumerate(toc_data):
        row = toc_table.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.space_before = Pt(5)
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            
            if row_idx == 0:
                run.bold = True
                set_cell_background(cell, "2C3E50")
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            elif row_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

            if col_idx == 0:
                cell.width = Inches(0.8)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif col_idx == 1:
                cell.width = Inches(4.7)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                cell.width = Inches(0.9)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    # -------------------------------------------------------------
    # PAGE 3: ABSTRACT
    # -------------------------------------------------------------
    doc.add_page_break()

    p_abs_h = doc.add_paragraph()
    p_abs_h.paragraph_format.space_before = Pt(10)
    p_abs_h.paragraph_format.space_after = Pt(10)
    r_ah = p_abs_h.add_run("Abstract:")
    r_ah.font.name = 'Times New Roman'
    r_ah.font.size = Pt(14)
    r_ah.bold = True

    p_cpe_desc = doc.add_paragraph()
    p_cpe_desc.paragraph_format.line_spacing = 1.15
    p_cpe_desc.paragraph_format.space_after = Pt(8)
    p_cpe_desc.add_run(
        "A Complex Computing Problem (CPE/CCP) in high-performance computer engineering is defined as an open-ended, mathematically demanding challenge that cannot be solved using standard linear or trivial algorithms. CCPs are characterized by non-linear computational scaling, deep iterative dependencies, strict resource limitations, and memory subsystem bottlenecks. Solving a complex computing problem requires in-depth architectural awareness, encompassing multi-core processor topology, shared-memory synchronization primitives, cache hierarchy locality, and theoretical modeling via Amdahl's and Gustafson's Laws."
    )

    p_proj_desc = doc.add_paragraph()
    p_proj_desc.paragraph_format.line_spacing = 1.15
    p_proj_desc.paragraph_format.space_after = Pt(8)
    p_proj_desc.add_run(
        "This project investigates the performance engineering and shared-memory parallelization of the classical Floyd–Warshall All-Pairs Shortest Path (APSP) algorithm using OpenMP in C. The Floyd–Warshall algorithm exhibits a severe cubic asymptotic time complexity of O(V^3) and a quadratic memory requirement of O(V^2), where V denotes the total number of vertices in a network graph. In large-scale cybersecurity network graphs, computing shortest paths is foundational for real-time attack path enumeration, vulnerability reachability, lateral movement tracking, and zero-trust blast radius containment. However, the cubic time complexity poses a formidable barrier, requiring billions of operations for enterprise-scale topologies."
    )

    p_achieve_desc = doc.add_paragraph()
    p_achieve_desc.paragraph_format.line_spacing = 1.15
    p_achieve_desc.paragraph_format.space_after = Pt(8)
    p_achieve_desc.add_run(
        "To address this computational bottleneck, three distinct implementations were engineered and evaluated: (1) a baseline Sequential Implementation in C, (2) a Standard OpenMP Parallel Implementation distributing row updates across multiple hardware threads, and (3) an advanced Cache-Blocked (Tiled) OpenMP Parallel Implementation designed to maximize L1/L2 cache hits and mitigate memory bus saturation, with block sizes B in {16, 32, 64, 128, 256} studied. Scalability and performance benchmarks were executed across graph sizes of V in {500, 1000, 1500, 2000} vertices utilizing 1, 2, 4, 6, 8 and 12 threads on an Intel Core i7-9750H (6 cores / 12 hardware threads)."
    )

    p_results_desc = doc.add_paragraph()
    p_results_desc.paragraph_format.line_spacing = 1.15
    p_results_desc.paragraph_format.space_after = Pt(8)
    p_results_desc.add_run(
        "Every timing is the median of 5 round-robin runs. At V = 2000 (8 billion inner-loop operations), Standard OpenMP reduced runtime from 9.677s to 2.401s on 8 threads (4.03x speedup) and Cache-Blocked OpenMP to 2.160s (4.48x), reaching 4.91x (1.969s) on 12 threads. Blocking gave its largest gain on small graphs (3.68x vs 1.66x at V = 500) because it needs far fewer barrier synchronizations. Parallel overhead was quantified with T_o = p*T_p - T_seq and the Karp-Flatt metric, and a block-size study found B = 64 fastest. Correctness was verified on 1,800 test runs against an independent Bellman-Ford oracle, and every benchmark result was checked against the sequential output. An attack-graph demo shows the solver finding the minimum-effort attack path and blast radius in an enterprise network."
    )

    # -------------------------------------------------------------
    # PAGE 4: PROBLEM INTRODUCTION
    # -------------------------------------------------------------
    doc.add_page_break()

    p_pi_h = doc.add_paragraph()
    p_pi_h.paragraph_format.space_before = Pt(10)
    p_pi_h.paragraph_format.space_after = Pt(10)
    r_pi = p_pi_h.add_run("Problem Introduction:")
    r_pi.font.name = 'Times New Roman'
    r_pi.font.size = Pt(14)
    r_pi.bold = True

    p_pi1 = doc.add_paragraph()
    p_pi1.paragraph_format.line_spacing = 1.15
    p_pi1.paragraph_format.space_after = Pt(8)
    p_pi1.add_run(
        "The All-Pairs Shortest Path (APSP) problem is a foundational problem in graph theory and combinatorial optimization. Given a weighted, directed graph G = (V, E) defined by a vertex set V = {v1, v2, ..., vn} and an edge weight function w: E -> R, the objective is to determine the minimum cumulative path weight D(i, j) connecting every possible source vertex vi to every destination vertex vj."
    )

    p_pi2 = doc.add_paragraph()
    p_pi2.paragraph_format.line_spacing = 1.15
    p_pi2.paragraph_format.space_after = Pt(6)
    p_pi2.add_run(
        "The Floyd–Warshall algorithm solves the APSP problem using dynamic programming. The state transition is defined mathematically as:"
    )

    p_eq = doc.add_paragraph()
    p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eq.paragraph_format.space_before = Pt(4)
    p_eq.paragraph_format.space_after = Pt(8)
    r_eq = p_eq.add_run("D(k)[i][j] = min( D(k-1)[i][j],  D(k-1)[i][k] + D(k-1)[k][j] )")
    r_eq.bold = True
    r_eq.font.name = 'Consolas'
    r_eq.font.size = Pt(10.5)

    p_pi3 = doc.add_paragraph()
    p_pi3.paragraph_format.line_spacing = 1.15
    p_pi3.paragraph_format.space_after = Pt(8)
    p_pi3.add_run(
        "Here, D(k)[i][j] represents the shortest path from vertex i to vertex j considering only intermediate vertices from the subset {0, 1, ..., k}. The algorithm evaluates all intermediate vertices through three deeply nested loops, resulting in a strict computational complexity of Theta(V^3). For a moderately sized enterprise topology of V = 2000 nodes, the total number of operations equals 2000^3 = 8,000,000,000 inner-loop executions. On conventional single-core processors, sequential execution takes excessive time, creating an unacceptable latency for security applications."
    )

    p_cyber_h = doc.add_paragraph()
    p_cyber_h.paragraph_format.space_before = Pt(6)
    p_cyber_h.paragraph_format.space_after = Pt(4)
    r_ch = p_cyber_h.add_run("Cybersecurity Domain Application:")
    r_ch.bold = True
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(12)

    p_cyber_intro = doc.add_paragraph()
    p_cyber_intro.paragraph_format.line_spacing = 1.15
    p_cyber_intro.paragraph_format.space_after = Pt(4)
    p_cyber_intro.add_run("In modern cybersecurity infrastructure, rapid shortest path computations enable critical defensive workflows:")

    # BULLET POINTS ON NEW LINES
    add_bullet_item(doc, "Attack Path Enumeration:", "Network assets (workstations, DMZ gateways, AD domain controllers) are mapped as vertices. Edges represent exploitable communication channels with weights inverse to vulnerability risk (e.g., w = 10 - CVSS). APSP calculates the exact minimal-effort exploit path an adversary would traverse to reach crown-jewel assets.")
    add_bullet_item(doc, "Blast Radius Analysis:", "When an endpoint is compromised by ransomware, APSP immediately reveals all subnets and resources within reachable lateral propagation thresholds, allowing instant automated quarantine.")
    add_bullet_item(doc, "Zero-Trust Segmentation:", "Centrality and shortest-path frequency identify critical bridge nodes where firewalls, Intrusion Prevention Systems (IPS), and EDR telemetry must be prioritized.")

    # -------------------------------------------------------------
    # PAGE 5: SEQUENTIAL IMPLEMENTATION
    # -------------------------------------------------------------
    doc.add_page_break()

    p_seq_h = doc.add_paragraph()
    p_seq_h.paragraph_format.space_before = Pt(10)
    p_seq_h.paragraph_format.space_after = Pt(10)
    r_seq = p_seq_h.add_run("Sequential Implementation:")
    r_seq.font.name = 'Times New Roman'
    r_seq.font.size = Pt(14)
    r_seq.bold = True

    p_seq1 = doc.add_paragraph()
    p_seq1.paragraph_format.line_spacing = 1.15
    p_seq1.paragraph_format.space_after = Pt(6)
    p_seq1.add_run(
        "The sequential baseline was developed in C to serve as the ground truth for computational accuracy and performance benchmarks. The program utilizes a contiguous single-dimensional dynamic array of size N x N to represent the adjacency matrix, accessed using the index calculation: dist[i * N + j]."
    )

    p_seq_keys_h = doc.add_paragraph()
    p_seq_keys_h.paragraph_format.space_before = Pt(4)
    p_seq_keys_h.paragraph_format.space_after = Pt(4)
    r_skh = p_seq_keys_h.add_run("Architectural Considerations:")
    r_skh.bold = True
    r_skh.font.size = Pt(11)

    # NUMBERED ITEMS ON NEW LINES
    add_num_item(doc, "1.", "Contiguous Row-Major Storage:", "A single 1D array allocated via malloc() eliminates double-pointer (int**) indirection, enabling CPU hardware prefetchers to stream cache lines smoothly along the innermost loop.")
    add_num_item(doc, "2.", "Safe Infinity Representation:", "Absent edges are initialized to INF = 10^9. This prevents 32-bit signed integer overflow during arithmetic additions (dik + dkj).")
    add_num_item(doc, "3.", "Early Loop Pruning:", "The condition (if (dik == INF) continue;) prunes unreachable intermediate rows before entering loop j, skipping millions of redundant computations.")

    p_code_seq = doc.add_paragraph()
    p_code_seq.paragraph_format.space_before = Pt(6)
    p_code_seq.paragraph_format.space_after = Pt(4)
    r_cs_h = p_code_seq.add_run("Listing 1: Sequential Floyd-Warshall Algorithm in C")
    r_cs_h.bold = True
    r_cs_h.font.size = Pt(10)

    # Code Box Table
    tbl_code1 = doc.add_table(rows=1, cols=1)
    tbl_code1.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell1 = tbl_code1.rows[0].cells[0]
    c_cell1.width = Inches(6.5)
    set_cell_background(c_cell1, "F8F9FA")
    set_cell_margins(c_cell1, top=100, bottom=100, left=140, right=140)
    
    code_text1 = (
        "void floyd_warshall_sequential(int *dist, int n) {\n"
        "    for (int k = 0; k < n; k++) {\n"
        "        for (int i = 0; i < n; i++) {\n"
        "            int dik = dist[i * n + k];\n"
        "            if (dik == INF) continue; // Prune unreachable paths\n"
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
    p_c1 = c_cell1.paragraphs[0]
    p_c1.paragraph_format.space_before = Pt(2)
    p_c1.paragraph_format.space_after = Pt(2)
    p_c1.paragraph_format.line_spacing = 1.05
    rc1 = p_c1.add_run(code_text1)
    rc1.font.name = 'Consolas'
    rc1.font.size = Pt(9)
    rc1.font.color.rgb = RGBColor(0x1a, 0x25, 0x2f)

    p_seq_bottle = doc.add_paragraph()
    p_seq_bottle.paragraph_format.space_before = Pt(6)
    p_seq_bottle.paragraph_format.line_spacing = 1.15
    p_seq_bottle.paragraph_format.space_after = Pt(6)
    p_seq_bottle.add_run(
        "Sequential Bottlenecks: While contiguous row traversal over j is cache-friendly, reading dist[i * n + k] traverses column k across iterations of i, causing non-contiguous memory access. As matrix size exceeds the L3 cache size (e.g. 16 MB at V=2000), severe cache thrashing occurs, severely capping sequential throughput."
    )

    # -------------------------------------------------------------
    # PAGE 6: PARALLEL IMPLEMENTATION
    # -------------------------------------------------------------
    doc.add_page_break()

    p_par_h = doc.add_paragraph()
    p_par_h.paragraph_format.space_before = Pt(10)
    p_par_h.paragraph_format.space_after = Pt(10)
    r_par = p_par_h.add_run("Parallel implementation:")
    r_par.font.name = 'Times New Roman'
    r_par.font.size = Pt(14)
    r_par.bold = True

    p_dep_h = doc.add_paragraph()
    p_dep_h.paragraph_format.space_before = Pt(2)
    p_dep_h.paragraph_format.space_after = Pt(4)
    r_dh = p_dep_h.add_run("Dependency Analysis:")
    r_dh.bold = True
    r_dh.font.size = Pt(11)

    # BULLETS ON NEW LINES
    add_bullet_item(doc, "Outer Loop k (Loop-Carried Dependency):", "Iteration k strictly requires the completed state of iteration k - 1. This Read-After-Write (RAW) hazard prevents parallelization across iterations of k.")
    add_bullet_item(doc, "Inner Loops i and j (Data Independence):", "During step k, row k (dist[k][j]) and column k (dist[i][k]) remain invariant because dist[k][k] = 0. Each thread updating row i writes exclusively to disjoint memory slices (dist[i * n + j]). Thus, the i-loop is embarrassingly parallel without write-write race hazards!")

    p_code_par = doc.add_paragraph()
    p_code_par.paragraph_format.space_before = Pt(4)
    p_code_par.paragraph_format.space_after = Pt(4)
    r_cp_h = p_code_par.add_run("Listing 2: Standard OpenMP Row-Parallel Implementation")
    r_cp_h.bold = True
    r_cp_h.font.size = Pt(10)

    tbl_code2 = doc.add_table(rows=1, cols=1)
    tbl_code2.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell2 = tbl_code2.rows[0].cells[0]
    c_cell2.width = Inches(6.5)
    set_cell_background(c_cell2, "F8F9FA")
    set_cell_margins(c_cell2, top=100, bottom=100, left=140, right=140)
    
    code_text2 = (
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
    p_c2 = c_cell2.paragraphs[0]
    p_c2.paragraph_format.space_before = Pt(2)
    p_c2.paragraph_format.space_after = Pt(2)
    p_c2.paragraph_format.line_spacing = 1.05
    rc2 = p_c2.add_run(code_text2)
    rc2.font.name = 'Consolas'
    rc2.font.size = Pt(9)
    rc2.font.color.rgb = RGBColor(0x1a, 0x25, 0x2f)

    p_blk_h = doc.add_paragraph()
    p_blk_h.paragraph_format.space_before = Pt(6)
    p_blk_h.paragraph_format.space_after = Pt(4)
    r_bh = p_blk_h.add_run("Cache-Blocked (Tiled) Parallel Implementation:")
    r_bh.bold = True
    r_bh.font.size = Pt(11)

    p_blk_intro = doc.add_paragraph()
    p_blk_intro.paragraph_format.line_spacing = 1.15
    p_blk_intro.paragraph_format.space_after = Pt(4)
    p_blk_intro.add_run("To mitigate memory bus saturation, we engineered a 3-Phase Blocked Floyd-Warshall algorithm dividing the N x N matrix into B x B sub-blocks (default B = 64):")

    # BULLETS ON NEW LINES
    add_bullet_item(doc, "Phase 1 (Diagonal Block):", "Diagonal block (kb, kb) is computed sequentially.")
    add_bullet_item(doc, "Phase 2 (Cross Blocks):", "Cross row blocks (kb, jb) and column blocks (ib, kb) are updated concurrently in parallel using #pragma omp parallel for.")
    add_bullet_item(doc, "Phase 3 (Independent Blocks):", "All remaining independent tiles (ib, jb) are processed simultaneously using #pragma omp parallel for collapse(2) schedule(static). Each kernel call reads and writes three B x B tiles (3 x 4 x B^2 bytes: 12 KB at B = 32, 48 KB at B = 64), which stay inside each core's private L1/L2 cache (32 KB / 256 KB) instead of streaming from DRAM.")

    # -------------------------------------------------------------
    # PAGE 7: SIMULATION RESULTS
    # -------------------------------------------------------------
    doc.add_page_break()

    p_sim_h = doc.add_paragraph()
    p_sim_h.paragraph_format.space_before = Pt(10)
    p_sim_h.paragraph_format.space_after = Pt(10)
    r_sim = p_sim_h.add_run("Simulation Results:")
    r_sim.font.name = 'Times New Roman'
    r_sim.font.size = Pt(14)
    r_sim.bold = True

    p_sim_exp = doc.add_paragraph()
    p_sim_exp.paragraph_format.line_spacing = 1.15
    p_sim_exp.paragraph_format.space_after = Pt(6)
    p_sim_exp.add_run(
        "Empirical benchmarks were conducted on an Intel Core i7-9750H (6 cores / 12 hardware threads, 32 KB L1D + 256 KB L2 per core, 12 MB shared L3) using GCC 16.2.0 (-O3 -fopenmp). Each time is the median of 5 runs, taken round-robin (every configuration once per round) so CPU clock drift affects all of them equally, and every parallel result was verified against the sequential output. In strict alignment with CS-428 Lab 4 (Performance Analysis of Real OpenMP Applications), the parallel solutions were evaluated across three foundational performance metrics:\n"
        "• Speedup ψ(n, p) = T_seq / T_p: Relative performance compared to the sequential baseline.\n"
        "• Efficiency ε(n, p) = ψ(n, p) / p * 100%: Percentage of time each hardware thread is usefully utilized.\n"
        "• Parallel Cost c(n, p) = p * T_p: Resource expenditure in processor-seconds, demonstrating cost-optimality when c(n, p) approaches sequential time."
    )

    table_headers = ["Vertices (V)", "Algorithm Variant", "Threads (p)", "Time (sec)", "Speedup ψ", "Efficiency ε", "Cost c(n,p)"]
    
    # Table rows come straight from benchmark_results.csv so the report always matches the data
    table_data = []
    with open('benchmark_results.csv') as f:
        for r in csv.DictReader(f):
            if r['Implementation'] == 'Sequential' or r['Threads'] == '8':
                t, p = float(r['ExecutionTime_Sec']), int(r['Threads'])
                table_data.append((r['Size'], r['Implementation'], r['Threads'], f"{t:.4f} s",
                                   f"{float(r['Speedup']):.2f}x", f"{float(r['Efficiency_Pct']):.1f}%", f"{p * t:.3f} p-s"))

    # Simulation Results Table
    sim_table = doc.add_table(rows=len(table_data) + 1, cols=7)
    sim_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    hdr_cells = sim_table.rows[0].cells
    for i, title in enumerate(table_headers):
        hdr_cells[i].text = title
        hdr_cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_cells[i].paragraphs[0].runs[0].font.name = 'Times New Roman'
        hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(9)
        hdr_cells[i].paragraphs[0].runs[0].bold = True
        set_cell_background(hdr_cells[i], "2C3E50")
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_margins(hdr_cells[i], top=60, bottom=60, left=60, right=60)

    for r_idx, row_values in enumerate(table_data):
        row_cells = sim_table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_values):
            row_cells[c_idx].text = val
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.runs[0]
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if r_idx % 2 == 1:
                set_cell_background(row_cells[c_idx], "F8F9FA")
            set_cell_margins(row_cells[c_idx], top=50, bottom=50, left=60, right=60)

    # Figures
    p_fig_h = doc.add_paragraph()
    p_fig_h.paragraph_format.space_before = Pt(8)
    p_fig_h.paragraph_format.space_after = Pt(4)
    r_fh = p_fig_h.add_run("Performance & Scalability Graphs:")
    r_fh.bold = True
    r_fh.font.size = Pt(11)

    tbl_imgs = doc.add_table(rows=1, cols=2)
    tbl_imgs.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_img1 = tbl_imgs.rows[0].cells[0]
    cell_img2 = tbl_imgs.rows[0].cells[1]
    cell_img1.width = Inches(3.2)
    cell_img2.width = Inches(3.2)

    if os.path.exists('runtime_comparison.png'):
        p_i1 = cell_img1.paragraphs[0]
        p_i1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_i1.add_run().add_picture('runtime_comparison.png', width=Inches(3.1))
        p_cap1 = cell_img1.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc1 = p_cap1.add_run("Figure 1: Runtime vs Matrix Size")
        rc1.font.size = Pt(8.5)
        rc1.font.italic = True

    if os.path.exists('cache_blocking_comparison.png'):
        p_i2 = cell_img2.paragraphs[0]
        p_i2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_i2.add_run().add_picture('cache_blocking_comparison.png', width=Inches(3.1))
        p_cap2 = cell_img2.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc2 = p_cap2.add_run("Figure 2: Standard vs Blocked (8 Threads)")
        rc2.font.size = Pt(8.5)
        rc2.font.italic = True

    # -------------------------------------------------------------
    # PAGE 8: CONCLUSION
    # -------------------------------------------------------------
    doc.add_page_break()

    p_con_h = doc.add_paragraph()
    p_con_h.paragraph_format.space_before = Pt(10)
    p_con_h.paragraph_format.space_after = Pt(10)
    r_con = p_con_h.add_run("Conclusion")
    r_con.font.name = 'Times New Roman'
    r_con.font.size = Pt(14)
    r_con.bold = True

    p_c1_h = doc.add_paragraph()
    p_c1_h.paragraph_format.space_before = Pt(2)
    p_c1_h.paragraph_format.space_after = Pt(4)
    r_c1h = p_c1_h.add_run("Summary of Outcomes & Achieved Speedups:")
    r_c1h.bold = True
    r_c1h.font.size = Pt(11)

    p_con_intro = doc.add_paragraph()
    p_con_intro.paragraph_format.line_spacing = 1.15
    p_con_intro.paragraph_format.space_after = Pt(4)
    p_con_intro.add_run("This project successfully designed, implemented, and empirically evaluated parallel optimizations for the Floyd-Warshall All-Pairs Shortest Path algorithm. On moderate to large graph sizes, shared-memory multi-threading delivered marked performance gains over single-threaded sequential execution:")

    # BULLETS ON NEW LINES
    add_bullet_item(doc, "Standard OpenMP:", "Reached 4.03x speedup on 8 threads at V = 2000 (2.401s vs 9.677s sequential) and 2.79x at V = 1000 (0.415s vs 1.157s). Going from 8 to 12 threads changed its speedup by only -0.11x to +0.33x.")
    add_bullet_item(doc, "Cache-Blocked OpenMP:", "Reached 4.48x speedup on 8 threads and 4.91x on 12 threads at V = 2000 (1.969s), and 4.16x at V = 1000 (0.278s, 8 threads). With 8 threads, blocking beat standard parallelization at every size: by 122% at V = 500, 49% at V = 1000, 17% at V = 1500 and 11% at V = 2000. B = 64 was the fastest block size, or within 1% of it, at every size.")
    add_bullet_item(doc, "Parallel Overhead:", "With 1 thread, both OpenMP versions run within +/-10% of the sequential code (0.91-1.07x), so thread start-up overhead is small. The blocked version's large gain at V = 500 (2.2x) comes mostly from needing 2V/B barriers instead of V.")

    p_c2_h = doc.add_paragraph()
    p_c2_h.paragraph_format.space_before = Pt(6)
    p_c2_h.paragraph_format.space_after = Pt(4)
    r_c2h = p_c2_h.add_run("Amdahl's Law and Scalability Limitations:")
    r_c2h.bold = True
    r_c2h.font.size = Pt(11)

    p_amd_intro = doc.add_paragraph()
    p_amd_intro.paragraph_format.line_spacing = 1.15
    p_amd_intro.paragraph_format.space_after = Pt(4)
    p_amd_intro.add_run("While thread counts were scaled up to 8 threads, linear speedup (S = p) was not attained due to fundamental architectural constraints governed by Amdahl's Law:")

    # NUMBERED ITEMS ON NEW LINES
    add_num_item(doc, "1.", "Thread Synchronization Barriers:", "Because iteration k strictly requires the completed state of iteration k-1, an implicit barrier synchronization occurs at the end of every k phase (2000 total barriers for V=2000). Thread fork-join overhead and scheduling jitter accumulate across iterations.")
    add_num_item(doc, "2.", "Memory Bandwidth Saturation:", "The standard algorithm possesses low arithmetic intensity (~0.17 ops/byte). When multiple threads concurrently stream non-contiguous column elements from main RAM, the shared multi-core memory bus saturates, creating memory stall cycles.")
    add_num_item(doc, "3.", "Physical Core Limit:", "The i7-9750H has 6 physical cores. Threads 7-12 run on the same cores through Hyper-Threading and share their execution units and L1/L2 caches. From 8 to 12 threads, Standard OpenMP changed by -0.11x to +0.33x speedup, while the cache-friendly Blocked version still gained 0.21x to 0.98x.")

    p_oh_h = doc.add_paragraph()
    p_oh_h.paragraph_format.space_before = Pt(6)
    p_oh_h.paragraph_format.space_after = Pt(4)
    r_oh = p_oh_h.add_run("Parallel Overhead and Karp-Flatt Analysis:")
    r_oh.bold = True
    r_oh.font.size = Pt(11)
    p_oh = doc.add_paragraph()
    p_oh.paragraph_format.line_spacing = 1.15
    p_oh.paragraph_format.space_after = Pt(4)
    p_oh.add_run("Parallel overhead is the total thread-time not spent on useful work, T_o = p*T_p - T_seq, and the Karp-Flatt metric e = (1/speedup - 1/p) / (1 - 1/p) estimates the effective serial fraction from the measured speedup. With 1 thread, T_o is within +/-10% of T_seq (measurement noise), so thread start-up is cheap. T_o then grows with p: at V = 2000 Standard OpenMP wastes 4.1 s of thread-time at p = 2 and 20.0 s at p = 12, the Blocked version 3.9 s and 14.0 s. The Blocked version has the lower e in 19 of the 20 cases below. In 6 of 8 cases e rises from 8 to 12 threads: overhead (barriers and Hyper-Threading contention) grows faster than useful work, rather than a fixed serial part limiting speedup. e is highest at V = 500, where each barrier guards only 250,000 cell updates.")

    # Karp-Flatt serial fraction e per thread count, read from benchmark_results.csv
    with open('benchmark_results.csv') as f:
        bench = list(csv.DictReader(f))
    kf_threads = ['2', '4', '6', '8', '12']
    kf_rows = [["Vertices (V)", "Variant"] + [f"e (p={p})" for p in kf_threads] + ["T_o (p=12)"]]
    for size in sorted({r['Size'] for r in bench}, key=int):
        for impl in ("OpenMP-Standard", "OpenMP-Blocked"):
            sub = {r['Threads']: r for r in bench if r['Size'] == size and r['Implementation'] == impl}
            kf_rows.append([size, impl.split('-')[1]] + [f"{float(sub[p]['KarpFlatt']):.3f}" for p in kf_threads]
                           + [f"{float(sub['12']['Overhead_Sec']):.2f} s"])
    kf_table = doc.add_table(rows=len(kf_rows), cols=len(kf_rows[0]))
    kf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row_values in enumerate(kf_rows):
        for c_idx, val in enumerate(row_values):
            cell = kf_table.rows[r_idx].cells[c_idx]
            cell.text = val
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = cell.paragraphs[0].runs[0]
            run.font.name = 'Times New Roman'
            run.font.size = Pt(8.5)
            if r_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                set_cell_background(cell, "2C3E50")
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)

    p_c3_h = doc.add_paragraph()
    p_c3_h.paragraph_format.space_before = Pt(6)
    p_c3_h.paragraph_format.space_after = Pt(4)
    r_c3h = p_c3_h.add_run("Engineering Significance for Cyber Defense:")
    r_c3h.bold = True
    r_c3h.font.size = Pt(11)

    p_con3 = doc.add_paragraph()
    p_con3.paragraph_format.line_spacing = 1.15
    p_con3.paragraph_format.space_after = Pt(8)
    p_con3.add_run(
        "Accelerating all-pairs shortest path analysis transforms static graph analysis into real-time operational defense. By cutting computational latency from tens of seconds to sub-second thresholds for thousand-node enterprise topologies, defensive teams can dynamically calculate lateral attack propagation paths, compute real-time blast radius matrices during active ransomware outbreaks, and instantly optimize firewall placement in Zero-Trust environments."
    )

    # -------------------------------------------------------------
    # PAGE 9: ANY ADDED INFORMATION (OPTIONAL)
    # -------------------------------------------------------------
    doc.add_page_break()

    p_add_h = doc.add_paragraph()
    p_add_h.paragraph_format.space_before = Pt(10)
    p_add_h.paragraph_format.space_after = Pt(10)
    r_add = p_add_h.add_run("Any added information")
    r_add.font.name = 'Times New Roman'
    r_add.font.size = Pt(14)
    r_add.bold = True

    p_add_sub1 = doc.add_paragraph()
    p_add_sub1.paragraph_format.space_before = Pt(2)
    p_add_sub1.paragraph_format.space_after = Pt(4)
    r_as1 = p_add_sub1.add_run("1. Cybersecurity Case Study: Attack Path Reachability & Blast Radius Modeling")
    r_as1.bold = True
    r_as1.font.size = Pt(11)

    p_case_intro = doc.add_paragraph()
    p_case_intro.paragraph_format.line_spacing = 1.15
    p_case_intro.paragraph_format.space_after = Pt(4)
    p_case_intro.add_run("To demonstrate the cybersecurity application, main_benchmark.c runs the OpenMP Floyd-Warshall solver on an 8-node enterprise attack graph (step [2/3] of the program):")

    # BULLETS ON NEW LINES
    add_bullet_item(doc, "Network Assets:", "Phished-PC, Web-DMZ, VPN-Gateway, HR-Workstation, File-Server, SQL-Database, Jump-Host and Domain-Controller. Nine directed edges model exploitable channels (reused password, SQL injection, open SMB share, stored RDP credentials, admin session).")
    add_bullet_item(doc, "Edge Weights:", "Each weight is the attacker effort to pivot (lower = easier), e.g. W(u, v) = 10 - CVSS_Exploitability.")
    add_bullet_item(doc, "Result:", "Minimum-effort path Phished-PC -> HR-Workstation -> File-Server -> Jump-Host -> Domain-Controller (effort 11), cheaper than the direct HR-Workstation -> Domain-Controller route (14) and the Web-DMZ -> SQL-Database route (18). Blast radius within effort 7: HR-Workstation (2), File-Server (5), Web-DMZ (6), Jump-Host (7). The program checks this against the hand-computed answer and fails if it differs.")

    p_add_sub2 = doc.add_paragraph()
    p_add_sub2.paragraph_format.space_before = Pt(6)
    p_add_sub2.paragraph_format.space_after = Pt(4)
    r_as2 = p_add_sub2.add_run("2. Roofline Model Analysis & Cache Locality Profiling")
    r_as2.bold = True
    r_as2.font.size = Pt(11)

    p_add2 = doc.add_paragraph()
    p_add2.paragraph_format.line_spacing = 1.15
    p_add2.paragraph_format.space_after = Pt(6)
    p_add2.add_run(
        "In the inner loop, two memory loads and one write accompany one addition and one comparison, yielding an intensity of ~0.17 ops/byte, so naive Floyd-Warshall is memory-bound. A blocked tile kernel touches 3 x 4 x B^2 bytes: 12 KB at B = 32 (fits L1), 48 KB at B = 64 and 192 KB at B = 128 (fit the 256 KB L2), and 768 KB at B = 256 (spills to L3). The block-size study (Figure 5) found B = 64 the fastest, or within 1% of the fastest, at every graph size, which supports it as the default. Small tiles (B = 16) are slower at every size because they need 2V/B barriers (250 at V = 2000) and run very short inner loops. Large tiles (B = 256) leave too few tiles to keep 8 threads busy: at V = 500 only one Phase-3 tile remains, so B = 256 runs at 1.05x, barely faster than sequential."
    )

    # Figures in added info
    tbl_imgs2 = doc.add_table(rows=1, cols=2)
    tbl_imgs2.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_i1 = tbl_imgs2.rows[0].cells[0]
    c_i2 = tbl_imgs2.rows[0].cells[1]
    c_i1.width = Inches(3.2)
    c_i2.width = Inches(3.2)

    if os.path.exists('speedup_analysis.png'):
        p1 = c_i1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.add_run().add_picture('speedup_analysis.png', width=Inches(3.1))
        p_c1 = c_i1.add_paragraph()
        p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc1 = p_c1.add_run("Figure 3: Speedup vs Thread Count")
        rc1.font.size = Pt(8.5)
        rc1.font.italic = True

    if os.path.exists('efficiency_plot.png'):
        p2 = c_i2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.add_run().add_picture('efficiency_plot.png', width=Inches(3.1))
        p_c2 = c_i2.add_paragraph()
        p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc2 = p_c2.add_run("Figure 4: Parallel Efficiency vs Threads")
        rc2.font.size = Pt(8.5)
        rc2.font.italic = True

    if os.path.exists('block_size_analysis.png'):
        p5 = doc.add_paragraph()
        p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p5.add_run().add_picture('block_size_analysis.png', width=Inches(3.6))
        rc5 = p5.add_run("\nFigure 5: Block Size vs Speedup (Blocked OpenMP, 8 Threads)")
        rc5.font.size = Pt(8.5)
        rc5.font.italic = True

    if os.path.exists('overhead_analysis.png'):
        p6 = doc.add_paragraph()
        p6.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p6.add_run().add_picture('overhead_analysis.png', width=Inches(3.6))
        rc6 = p6.add_run("\nFigure 6: Karp-Flatt Serial Fraction vs Threads")
        rc6.font.size = Pt(8.5)
        rc6.font.italic = True

    output_path = "Complex_Computing_Problem_Report.docx"
    doc.save(output_path)
    print(f"Successfully generated Word document: {output_path}")

if __name__ == '__main__':
    create_docx_report()
