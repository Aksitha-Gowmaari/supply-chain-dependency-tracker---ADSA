import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="Supply_Chain_Dependency_Tracker_Review.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Palette (Executive Slate & Tech Navy)
    DARK_BG = RGBColor(15, 23, 42)      # #0F172A
    CARD_BG = RGBColor(30, 41, 59)      # #1E293B
    CARD_BORDER = RGBColor(51, 65, 85)  # #334155
    TEXT_WHITE = RGBColor(248, 250, 252) # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184) # #94A3B8
    CYAN = RGBColor(6, 182, 212)        # #06B6D4
    PURPLE = RGBColor(139, 92, 246)     # #8B5CF6
    AMBER = RGBColor(245, 158, 11)      # #F59E0B
    ROSE = RGBColor(244, 63, 94)        # #F43F5E
    GREEN = RGBColor(16, 185, 129)      # #10B981

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = DARK_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, kicker_text="ADSA PROJECT REVIEW • TECHNICAL REPORT", slide_num=None):
        set_bg(slide)
        
        # Header Box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_kicker = tf.paragraphs[0]
        p_kicker.text = kicker_text.upper()
        p_kicker.font.size = Pt(10)
        p_kicker.font.bold = True
        p_kicker.font.color.rgb = CYAN
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        if slide_num:
            num_box = slide.shapes.add_textbox(Inches(12.0), Inches(0.5), Inches(0.8), Inches(0.4))
            ntf = num_box.text_frame
            np = ntf.paragraphs[0]
            np.text = f"{slide_num:02d}"
            np.alignment = PP_ALIGN.RIGHT
            np.font.size = Pt(12)
            np.font.bold = True
            np.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title=None, border_color=CARD_BORDER, bg_color=CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.18), width - Inches(0.4), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title.upper()
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = CYAN
        return card

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = "ADVANCED DATA STRUCTURES & ALGORITHMS • COURSE PROJECT"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = CYAN
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Supply Chain Dependency Tracker"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE
    p2.space_after = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Graph Architecture, Cycle Detection, Criticality Ranking & Failure Simulation"
    p3.font.size = Pt(18)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_after = Pt(28)

    p4 = tf.add_paragraph()
    p4.text = "Project Team: Aksitha & Khyathi  |  Code Implementation Review"
    p4.font.size = Pt(13)
    p4.font.bold = True
    p4.font.color.rgb = PURPLE

    # Stat chips on title slide
    chips = [
        ("63 Suppliers", "Tier 0 to Tier 4 Nodes"),
        ("76 Dependencies", "Lead-Time Weighted Edges"),
        ("2 Circular Deadlocks", "3-Color DFS Back-Edges"),
        ("16 SPOFs Identified", "Single Points of Failure")
    ]
    for i, (c_top, c_sub) in enumerate(chips):
        left_pos = Inches(0.8 + i * 2.95)
        card = add_card(s1, left_pos, Inches(5.6), Inches(2.8), Inches(1.2))
        tbox = s1.shapes.add_textbox(left_pos + Inches(0.2), Inches(5.75), Inches(2.4), Inches(0.9))
        ctf = tbox.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = 0
        
        cp1 = ctf.paragraphs[0]
        cp1.text = c_top
        cp1.font.size = Pt(15)
        cp1.font.bold = True
        cp1.font.color.rgb = TEXT_WHITE
        
        cp2 = ctf.add_paragraph()
        cp2.text = c_sub
        cp2.font.size = Pt(10)
        cp2.font.color.rgb = CYAN

    # =========================================================================
    # SLIDE 2: Problem Statement & Algorithmic Goals
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Algorithmic Objectives", "ADSA FOUNDATION", 2)

    # Left: Problem Context
    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "THE SUPPLY NETWORK PROBLEM")
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.4), Inches(5.2), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    points_prob = [
        ("Multi-Tier Hidden Dependencies:", "Real-world manufacturing relies on deep supply tiers. A manufacturer knows direct Tier 1 suppliers, but is blind to Tier 3 and 4 raw material nodes."),
        ("Deadlock Caused by Cycles:", "Circular dependencies (Supplier A needs B, B needs C, C needs A) create topological deadlocks, halting production schedules before contracts can execute."),
        ("Single Points of Failure (SPOFs):", "Suppliers with high downstream reliance and zero secondary backup sources pose catastrophic systemic failure risks."),
        ("Lead-Time Compounding:", "Delays compound non-linearly across dependency chains, requiring weighted shortest path algorithms to identify critical procurement paths.")
    ]
    for i, (head, body) in enumerate(points_prob):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {head} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(2)
        
        p_sub = tf.add_paragraph()
        p_sub.text = f"  {body}"
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(10)

    # Right: Algorithmic Deliverables
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "ADSA ALGORITHMIC DELIVERABLES")
    tb2 = s2.shapes.add_textbox(Inches(7.0), Inches(2.4), Inches(5.3), Inches(4.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    goals = [
        ("Dual Adjacency List Graph:", "O(V + E) space representation with bidirectional lookup (dependencies & dependents) optimized for sparse supplier networks."),
        ("Cycle Detection via 3-Color DFS:", "Linear time O(V + E) detection using White/Gray/Black node coloring to flag recursive deadlocks."),
        ("Procurement Ordering via Kahn's Algorithm:", "Topological sorting to establish valid component build sequences or identify cyclic blockers."),
        ("Reverse BFS Criticality Scoring:", "BFS traversal over predecessor edges to quantify systemic blast radius (number of affected downstream suppliers)."),
        ("Weighted Shortest Path via Dijkstra:", "Min-heap priority queue O((V + E) log V) computing lowest lead-time procurement chains from root manufacturer."),
        ("Dynamic Failure Simulation:", "Stress-testing node removals to determine impact on Tier 0 assembly and find alternate bypass routes.")
    ]
    for i, (head, body) in enumerate(goals):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = f"✓ {head} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        
        p_sub = tf2.add_paragraph()
        p_sub.text = f"  {body}"
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: Module Architecture & Work Distribution
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Architecture & Codebase Division of Work", "CODEBASE ORGANIZATION", 3)

    modules = [
        ("src/graph.py", "OWNER: Aksitha", [
            "Custom Graph class data structure",
            "Dual adjacency list implementation",
            "O(1) neighbor & predecessor lookups",
            "CSV ingestion & data sanitization",
            "Smoke test harness & representation"
        ], CYAN),
        ("src/traversal.py", "OWNER: Aksitha", [
            "Iterative Depth-First Search (DFS)",
            "Breadth-First Search (hop distance)",
            "3-Color cycle detection algorithm",
            "Kahn's Topological Sort build order",
            "Cycle path reconstruction logic"
        ], CYAN),
        ("src/risk_scoring.py", "OWNER: Khyathi", [
            "Reverse BFS downstream criticality",
            "Single Point of Failure (SPOF) audit",
            "Min-heap Dijkstra shortest lead-time",
            "Alternate path bypass routing algorithm",
            "Disruption blast-radius simulator"
        ], PURPLE),
        ("src/visualize.py", "OWNER: Khyathi", [
            "NetworkX DiGraph conversion helper",
            "Matplotlib dependency graph rendering",
            "Color coding (SPOF, cycle, normal)",
            "Node scaling by criticality score",
            "Automated CLI risk alert report"
        ], PURPLE)
    ]

    for i, (mod_name, owner, bullets, col) in enumerate(modules):
        left_pos = Inches(0.8 + i * 2.95)
        add_card(s3, left_pos, Inches(1.8), Inches(2.8), Inches(4.3), mod_name)
        
        tb = s3.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.35), Inches(2.4), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_own = tf.paragraphs[0]
        p_own.text = owner
        p_own.font.size = Pt(11)
        p_own.font.bold = True
        p_own.font.color.rgb = col
        p_own.space_after = Pt(12)
        
        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(10)
            pb.font.color.rgb = TEXT_MUTED
            pb.space_after = Pt(6)

    # Integration Card at Bottom
    add_card(s3, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.85), bg_color=RGBColor(24, 32, 47))
    tb_bot = s3.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.65))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    tf_bot.margin_left = tf_bot.margin_top = tf_bot.margin_right = tf_bot.margin_bottom = 0
    p_bot = tf_bot.paragraphs[0]
    p_bot.text = "INTEGRATION & VALIDATION (Aksitha + Khyathi Joint): "
    p_bot.font.bold = True
    p_bot.font.size = Pt(11)
    p_bot.font.color.rgb = AMBER
    p_bot_sub = tf_bot.add_paragraph()
    p_bot_sub.text = "Pipeline entry point (src/main.py), Dataset modeling (data/), and Automated Unit Test Suite (tests/test_graph_algorithms.py) verifying 100% algorithm accuracy."
    p_bot_sub.font.size = Pt(10)
    p_bot_sub.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 4: Graph Data Structure & Design Choice
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Graph Data Structure & Design Rationale", "MODULE 1 • SRC/GRAPH.PY", 4)

    # Left Card: Design Choice & Complexity
    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "DESIGN CHOICE: ADJACENCY LIST")
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    reasons = [
        ("Why NOT an Adjacency Matrix?", "Real-world supplier networks are SPARSE. Our network has 63 nodes and 76 edges. An adjacency matrix requires O(V^2) = 63 x 63 = 3,969 cells, of which over 98% would be empty zeros."),
        ("Space Complexity: O(V + E)", "Using defaultdict(list) stores only existing dependency edges. Memory scales linearly with network size instead of quadratically."),
        ("Neighbor & Predecessor Lookup: O(deg(v))", "Checking who a supplier depends on takes time proportional only to its active connections, rather than iterating across all 63 nodes."),
        ("Dual Adjacency Implementation:", "We maintain two concurrent hash maps:\n • self.adjacency: maps supplier -> [(neighbor, weight)]\n • self.reverse_adjacency: maps supplier -> [(dependent, weight)]\nThis enables instant O(1) predecessor lookup needed for reverse BFS.")
    ]
    for i, (h, b) in enumerate(reasons):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        p.space_after = Pt(2)
        
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Right Card: Actual Code Structure
    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "CODE STRUCTURE: CLASS GRAPH")
    tb2 = s4.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    code_lines = [
        "class Graph:",
        "    def __init__(self):",
        "        self.suppliers = {}          # supplier_id -> metadata",
        "        self.adjacency = defaultdict(list)         # depends ON",
        "        self.reverse_adjacency = defaultdict(list) # depended ON by",
        "",
        "    def add_supplier(self, supplier_id, name, tier, has_backup):",
        "        self.suppliers[supplier_id] = {",
        "            'name': name or supplier_id,",
        "            'tier': tier,",
        "            'has_backup': has_backup",
        "        }",
        "",
        "    def add_dependency(self, from_id, to_id, weight=1.0):",
        "        # Edge from_id -> to_id means: from_id DEPENDS ON to_id",
        "        self.adjacency[from_id].append((to_id, weight))",
        "        self.reverse_adjacency[to_id].append((from_id, weight))",
        "",
        "    def get_neighbors(self, supplier_id):",
        "        return self.adjacency.get(supplier_id, [])",
        "",
        "    def get_predecessors(self, supplier_id):",
        "        return self.reverse_adjacency.get(supplier_id, [])"
    ]
    for i, l in enumerate(code_lines):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = l
        p.font.size = Pt(9.5)
        p.font.name = "Consolas"
        if l.startswith("class ") or l.startswith("    def "):
            p.font.bold = True
            p.font.color.rgb = GREEN
        elif l.strip().startswith("#"):
            p.font.color.rgb = TEXT_MUTED
        else:
            p.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 5: Dataset Pipeline & Multi-Tier Schema
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Supply Chain Dataset & Multi-Tier Schema", "DATA PIPELINE • DATA/ DIRECTORY", 5)

    add_card(s5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.2), "5-TIER AUTOMOTIVE SUPPLY CHAIN STRUCTURE")
    
    tier_info = [
        ("Tier 0: Root Manufacturer", "1 Node", "Apex Motors (MFG) — Final vehicle assembly plant requiring all Tier 1 subsystems.", PURPLE),
        ("Tier 1: Major Subsystems", "6 Nodes", "Battery Pack (BP), Powertrain (PT), Chassis (CH), Electronics (EL), Interior (IN), Body (BD).", CYAN),
        ("Tier 2: Key Assemblies", "19 Nodes", "Battery Cells (BC), BMS, Inverter (INV), Motor (MOT), Circuit Boards (PCB), Steering, Suspension.", CYAN),
        ("Tier 3: Fabricators", "28 Nodes", "Microcontroller Foundry (MCU), Rare Earth Magnets (MAG), Silicon Wafer (SIL), Glass (GLS).", AMBER),
        ("Tier 4: Raw Material Mines", "9 Nodes", "Lithium (LITH), Cobalt (COBALT), Silica Quartz (SILICA), Iron Ore (IRONORE), Rubber (RUBBER).", ROSE)
    ]
    for i, (t_title, t_count, t_desc, col) in enumerate(tier_info):
        top_offset = Inches(2.3 + i * 0.32)
        tb = s5.shapes.add_textbox(Inches(1.0), top_offset, Inches(11.3), Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"{t_title} ({t_count}): "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = col
        p_desc = tf.add_paragraph()
        p_desc.text = t_desc
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = TEXT_MUTED

    # Bottom Two Cards: suppliers.csv and dependencies.csv
    add_card(s5, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.6), "DATA INGESTION: SUPPLIERS.CSV (63 ROWS)")
    tb_s = s5.shapes.add_textbox(Inches(1.0), Inches(4.8), Inches(5.2), Inches(2.0))
    tfs = tb_s.text_frame
    tfs.word_wrap = True
    tfs.margin_left = tfs.margin_top = tfs.margin_right = tfs.margin_bottom = 0
    s_lines = [
        "Columns: id, name, tier, has_backup",
        "• id: Unique alphanumeric identifier (e.g. MFG, BP, MCU, SILICA)",
        "• name: Legal operating entity name",
        "• tier: Supply hierarchy level (0 to 4)",
        "• has_backup: Boolean (True if secondary alternate supplier contracted)",
        "Data Fix: Cleaned Excel paste artifact 'MFG+EA2:E55' -> 'MFG' to re-link Apex Motors root node correctly."
    ]
    for i, l in enumerate(s_lines):
        p = tfs.paragraphs[0] if i == 0 else tfs.add_paragraph()
        p.text = l
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE if i == 0 or i == 5 else TEXT_MUTED
        if i == 5: p.font.color.rgb = AMBER
        p.space_after = Pt(3)

    add_card(s5, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.6), "DATA INGESTION: DEPENDENCIES.CSV (76 EDGES)")
    tb_d = s5.shapes.add_textbox(Inches(7.0), Inches(4.8), Inches(5.3), Inches(2.0))
    tfd = tb_d.text_frame
    tfd.word_wrap = True
    tfd.margin_left = tfd.margin_top = tfd.margin_right = tfd.margin_bottom = 0
    d_lines = [
        "Columns: from, to, weight",
        "• from: Dependent supplier (needs input)",
        "• to: Supplying entity (provides parts / materials)",
        "• weight: Procurement lead time in DAYS",
        "Example Edges:",
        "  MFG -> BP (weight: 10 days)  |  PT -> MOT (weight: 16 days)",
        "  CATH -> LITH (weight: 30 days)  |  MAG -> RAREEARTH (weight: 35 days)"
    ]
    for i, l in enumerate(d_lines):
        p = tfd.paragraphs[0] if i == 0 else tfd.add_paragraph()
        p.text = l
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE if i == 0 or i == 4 else TEXT_MUTED
        if i >= 5: p.font.color.rgb = CYAN; p.font.name = "Consolas"
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 6: Cycle Detection via 3-Color DFS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Cycle Detection Algorithm (3-Color DFS)", "MODULE 2 • SRC/TRAVERSAL.PY", 6)

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "ALGORITHM: 3-COLOR RECURSIVE DFS")
    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    c_steps = [
        ("Color Coding States:", "• WHITE (0): Unvisited node.\n• GRAY (1): Currently exploring on the active DFS path.\n• BLACK (2): Fully visited; all subtrees explored."),
        ("Back-Edge Detection:", "When traversing node u -> v:\nIf color[v] == GRAY: We encountered an ancestor on the current recursion path -> A CYCLE EXISTS!\nIf color[v] == WHITE: Recursively visit v."),
        ("Cycle Extraction Logic:", "cycle_start_index = path.index(neighbor)\ncycles.append(path[cycle_start_index:] + [neighbor])\nExtracts the exact sequence forming the loop."),
        ("Time & Space Complexity:", "• Time: O(V + E) — every node and edge examined at most twice.\n• Space: O(V) for color array and path stack.")
    ]
    for i, (h, b) in enumerate(c_steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        p.space_after = Pt(2)
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Right Card: Real Results
    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "DETECTION RESULTS: 2 REAL DEADLOCK CYCLES", border_color=AMBER)
    tb2 = s6.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p_r1 = tf2.paragraphs[0]
    p_r1.text = "CYCLE LOOP #1 (Battery Subsystem):"
    p_r1.font.bold = True
    p_r1.font.size = Pt(12)
    p_r1.font.color.rgb = AMBER
    p_r1.space_after = Pt(4)

    p_r1_c = tf2.add_paragraph()
    p_r1_c.text = "BMS ➔ TC ➔ BMS"
    p_r1_c.font.bold = True
    p_r1_c.font.size = Pt(16)
    p_r1_c.font.name = "Consolas"
    p_r1_c.font.color.rgb = TEXT_WHITE
    p_r1_c.space_after = Pt(4)

    p_r1_d = tf2.add_paragraph()
    p_r1_d.text = "• BMS (Battery Management System) depends on TC (Thermal Cooling, wt: 4d).\n• TC depends back on BMS (wt: 3d) for sensor control logic.\n• Impact: Neither can be fully assembled without the other."
    p_r1_d.font.size = Pt(10)
    p_r1_d.font.color.rgb = TEXT_MUTED
    p_r1_d.space_after = Pt(18)

    p_r2 = tf2.add_paragraph()
    p_r2.text = "CYCLE LOOP #2 (Powertrain Subsystem):"
    p_r2.font.bold = True
    p_r2.font.size = Pt(12)
    p_r2.font.color.rgb = AMBER
    p_r2.space_after = Pt(4)

    p_r2_c = tf2.add_paragraph()
    p_r2_c.text = "MOT ➔ INV ➔ MOT"
    p_r2_c.font.bold = True
    p_r2_c.font.size = Pt(16)
    p_r2_c.font.name = "Consolas"
    p_r2_c.font.color.rgb = TEXT_WHITE
    p_r2_c.space_after = Pt(4)

    p_r2_d = tf2.add_paragraph()
    p_r2_d.text = "• MOT (Electric Motor Assembly) depends on INV (Inverter Systems, wt: 5d).\n• INV depends on MOT (wt: 4d) for motor rotor calibration.\n• Impact: Mutual recursive dependency blocks procurement sign-off."
    p_r2_d.font.size = Pt(10)
    p_r2_d.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 7: Procurement Order via Topological Sort
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Topological Sort & Procurement Ordering", "MODULE 2 • SRC/TRAVERSAL.PY", 7)

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "KAHN'S ALGORITHM IMPLEMENTATION")
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    topo_steps = [
        ("Concept: Safe Assembly Sequencing", "In a dependency graph, procurement must start at leaf suppliers (raw materials) that have ZERO unresolved dependencies, working upwards to Tier 0."),
        ("Out-Degree Resolution Logic:", "remaining_deps = {node: len(get_neighbors(node))}\nqueue = deque([node for node in nodes if remaining_deps[node] == 0])"),
        ("Iterative Resolution:", "While queue is not empty:\n 1. Pop leaf node u and append to valid order list.\n 2. For each dependent v that relies on u (get_predecessors):\n    remaining_deps[v] -= 1\n    if remaining_deps[v] == 0: queue.append(v)"),
        ("DAG Validation Condition:", "is_valid = (len(order) == len(all_suppliers))\nIf order length < total suppliers, remaining nodes are locked in cycles!")
    ]
    for i, (h, b) in enumerate(topo_steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        p.space_after = Pt(2)
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Right Card: Kahn's Execution Result
    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "EXECUTION RESULT: ORDER BLOCKED BY CYCLES", border_color=ROSE)
    tb2 = s7.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p_stat = tf2.paragraphs[0]
    p_stat.text = "EXECUTION STATUS: INCOMPLETE (CYCLIC)"
    p_stat.font.bold = True
    p_stat.font.size = Pt(12)
    p_stat.font.color.rgb = ROSE
    p_stat.space_after = Pt(8)

    p_exp = tf2.add_paragraph()
    p_exp.text = "When running topological_sort(graph):\nKahn's algorithm successfully processes leaf raw materials (Lithium, Silica, Iron Ore, Rubber), but CANNOT resolve BMS, TC, MOT, and INV due to circular reference."
    p_exp.font.size = Pt(10.5)
    p_exp.font.color.rgb = TEXT_WHITE
    p_exp.space_after = Pt(12)

    p_log = tf2.add_paragraph()
    p_log.text = "Console Output from src/main.py:\n'Topological sort INCOMPLETE -- 2 cycle(s) block a valid procurement order.'"
    p_log.font.size = Pt(10)
    p_log.font.name = "Consolas"
    p_log.font.color.rgb = AMBER
    p_log.space_after = Pt(14)

    p_val = tf2.add_paragraph()
    p_val.text = "Business / Engineering Value:\nThis algorithm automatically flags production bottlenecks before factory contracts are signed, proving that supply agreements require restructuring (e.g. decoupled buffer inventory)."
    p_val.font.size = Pt(10)
    p_val.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: Structural Criticality via Reverse BFS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Structural Criticality & Downstream Blast Radius", "MODULE 3 • SRC/RISK_SCORING.PY", 8)

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "ALGORITHM: REVERSE BFS OVER PREDECESSORS")
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    rev_steps = [
        ("The 'Blast Radius' Question:", "If Supplier X is hit by a disaster or factory shutdown, how many other suppliers across the entire network will be impacted?"),
        ("Reverse Traversal Logic:", "Standard BFS follows get_neighbors ('who do I need').\nReverse BFS follows get_predecessors ('who relies on me').\nStarting at node X, explore all reachable nodes in the transposed graph."),
        ("Mathematical Formulation:", "Criticality(u) = | { v ∈ V : u reaches v in G_reversed } | - 1"),
        ("Key Discovery:", "Criticality is NOT determined by direct degree alone. Upstream raw material mines with low direct degree have immense multi-tier downstream impact.")
    ]
    for i, (h, b) in enumerate(rev_steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        p.space_after = Pt(2)
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Right Card: Top 5 Critical Suppliers Table
    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "TOP 5 MOST CRITICAL SUPPLIERS IN NETWORK")
    
    top5 = [
        ("SILICA", "Silica Quartz Mine", "Tier 4", "10 Nodes Affected", ROSE),
        ("MCU", "Microcontroller Foundry", "Tier 3", "9 Nodes Affected", ROSE),
        ("PETRO", "Petrochemical Refinery", "Tier 4", "9 Nodes Affected", ROSE),
        ("IRONORE", "Iron Ore Mine", "Tier 4", "7 Nodes Affected", AMBER),
        ("IRON", "Iron Ore Processor", "Tier 3", "6 Nodes Affected", AMBER)
    ]
    for i, (sid, sname, stier, sscore, col) in enumerate(top5):
        top_offset = Inches(2.35 + i * 0.8)
        card_t = add_card(s8, Inches(7.0), top_offset, Inches(5.3), Inches(0.7), bg_color=RGBColor(24, 32, 47))
        tb_t = s8.shapes.add_textbox(Inches(7.15), top_offset + Inches(0.08), Inches(5.0), Inches(0.55))
        tft = tb_t.text_frame
        tft.word_wrap = True
        tft.margin_left = tft.margin_top = tft.margin_right = tft.margin_bottom = 0
        
        pt1 = tft.paragraphs[0]
        pt1.text = f"#{i+1}  {sid} — {sname} ({stier})"
        pt1.font.bold = True
        pt1.font.size = Pt(11)
        pt1.font.color.rgb = TEXT_WHITE
        
        pt2 = tft.add_paragraph()
        pt2.text = f"Impact: {sscore} across automotive subsystems"
        pt2.font.size = Pt(9.5)
        pt2.font.bold = True
        pt2.font.color.rgb = col

    # =========================================================================
    # SLIDE 9: Single Points of Failure (SPOF) Analysis
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Single Points of Failure (SPOF) Analysis", "MODULE 3 • SRC/RISK_SCORING.PY", 9)

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "SPOF DEFINITION & DETECTION LOGIC")
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    spof_logic = [
        ("The Dual SPOF Condition:", "In find_single_points_of_failure(graph):\nA supplier node u is flagged if AND ONLY IF:\n 1. len(get_predecessors(u)) > 0 (At least 1 node depends on it)\n 2. metadata[u]['has_backup'] == False (Zero secondary source)"),
        ("Operational Implication:", "If a SPOF experiences disruption, the reliant systems have NO pre-contracted alternate route. Production immediately halts."),
        ("Detection Summary:", "Out of 63 suppliers in Apex Motors' network, exactly 16 SUPPLIERS (25.4%) are unhedged Single Points of Failure!"),
        ("Strategic Action:", "Gives procurement executives an automated target list for dual-sourcing contracts.")
    ]
    for i, (h, b) in enumerate(spof_logic):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        p.space_after = Pt(2)
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Right Card: All 16 Identified SPOFs
    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "16 IDENTIFIED SINGLE POINTS OF FAILURE", border_color=ROSE)
    tb2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p_spof_head = tf2.paragraphs[0]
    p_spof_head.text = "TIER 2 CRITICAL ASSEMBLIES (5 SPOFs):"
    p_spof_head.font.bold = True
    p_spof_head.font.size = Pt(10.5)
    p_spof_head.font.color.rgb = ROSE
    p_spof_head.space_after = Pt(2)

    p_t2 = tf2.add_paragraph()
    p_t2.text = "• BC (Battery Cell Mfg)  • MOT (Electric Motor Assembly)\n• PCB (Circuit Board Mfg)  • DIS (Display Panel)  • GLS (Glass Mfg)"
    p_t2.font.size = Pt(9.5)
    p_t2.font.color.rgb = TEXT_WHITE
    p_t2.space_after = Pt(10)

    p_t3_head = tf2.add_paragraph()
    p_t3_head.text = "TIER 3 SUBCOMPONENTS & FABRICATORS (6 SPOFs):"
    p_t3_head.font.bold = True
    p_t3_head.font.size = Pt(10.5)
    p_t3_head.font.color.rgb = AMBER
    p_t3_head.space_after = Pt(2)

    p_t3 = tf2.add_paragraph()
    p_t3.text = "• CATH (Cathode Material)  • SEP (Separator Film)\n• MCU (Microcontroller Foundry)  • MAG (Rare Earth Magnet)\n• TIRE (Tire Rubber Supplier)  • SIL (Silicon Wafer Supply)\n• LCD (LCD Panel Manufacturer)"
    p_t3.font.size = Pt(9.5)
    p_t3.font.color.rgb = TEXT_WHITE
    p_t3.space_after = Pt(10)

    p_t4_head = tf2.add_paragraph()
    p_t4_head.text = "TIER 4 RAW MATERIAL MINING (5 SPOFs):"
    p_t4_head.font.bold = True
    p_t4_head.font.size = Pt(10.5)
    p_t4_head.font.color.rgb = CYAN
    p_t4_head.space_after = Pt(2)

    p_t4 = tf2.add_paragraph()
    p_t4.text = "• LITH (Lithium Mining Co)  • COBALT (Cobalt Mining Co)\n• RAREEARTH (Rare Earth Ore Mine)  • RUBBER (Natural Rubber Plantation)"
    p_t4.font.size = Pt(9.5)
    p_t4.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 10: Dijkstra's Algorithm & Lead-Time Analysis
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Shortest Lead-Time via Dijkstra's Algorithm", "MODULE 3 • SRC/RISK_SCORING.PY", 10)

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "ALGORITHM: MIN-HEAP DIJKSTRA")
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    dijk_info = [
        ("Physical Interpretation of Weights:", "Edge weight = Supplier procurement lead time in DAYS.\nThe 'lowest-risk' or fastest delivery path from Apex Motors (MFG) to any supplier is the weighted shortest path."),
        ("Min-Heap Priority Queue:", "Implemented using Python's heapq module:\n• distances = {start: 0}\n• heap = [(0, start)]\n• Pops lowest cumulative lead time node greedily."),
        ("Time Complexity: O((V + E) log V):", "With 63 nodes and 76 edges, Dijkstra computes instantaneous results in under 2 milliseconds."),
        ("Network Summary Statistics:", "• Average Lead Time from MFG: 27.1 Days\n• Minimum Lead Time: 6.0 Days (IN - Interior Systems)\n• Maximum Lead Time: 85.0 Days (RAREEARTH - Rare Earth Mine)")
    ]
    for i, (h, b) in enumerate(dijk_info):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        p.space_after = Pt(2)
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Right Card: Lead-Time Path Spectrum
    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "LEAD-TIME PATH LENGTHS FROM ROOT (MFG)")
    tb2 = s10.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    lead_spectrum = [
        ("TIER 1 SUBSYSTEMS (Direct to MFG):", [
            "MFG -> IN (Interior): 6.0 days",
            "MFG -> EL (Electronics): 7.0 days",
            "MFG -> CH (Chassis): 8.0 days",
            "MFG -> BD (Body): 9.0 days",
            "MFG -> BP (Battery Pack): 10.0 days"
        ], GREEN),
        ("INTERMEDIATE ASSEMBLIES (Tier 2-3):", [
            "MFG -> ... -> BMS (Battery Mgmt): 20.0 days",
            "MFG -> ... -> BC (Battery Cell): 24.0 days",
            "MFG -> ... -> MOT (Electric Motor): 28.0 days",
            "MFG -> ... -> MCU (Microcontroller): 38.0 days"
        ], AMBER),
        ("DEEP RAW MATERIAL EXTRACTION (Tier 4):", [
            "MFG -> ... -> SILICA (Silica Quartz): 45.0 days",
            "MFG -> ... -> LITH (Lithium Mine): 64.0 days",
            "MFG -> ... -> COBALT (Cobalt Mine): 70.0 days",
            "MFG -> ... -> RAREEARTH (Rare Earth Ore): 85.0 days (LONGEST)"
        ], ROSE)
    ]
    for section_title, items, col in lead_spectrum:
        p_st = tf2.paragraphs[0] if tf2.paragraphs[0].text == "" else tf2.add_paragraph()
        p_st.text = section_title
        p_st.font.bold = True
        p_st.font.size = Pt(10)
        p_st.font.color.rgb = col
        p_st.space_after = Pt(2)
        for it in items:
            pi = tf2.add_paragraph()
            pi.text = f"  • {it}"
            pi.font.size = Pt(9.5)
            pi.font.color.rgb = TEXT_WHITE
            pi.font.name = "Consolas"
        tf2.add_paragraph().space_after = Pt(4)

    # =========================================================================
    # SLIDE 11: Disruption Simulation & Alternate Paths
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Dynamic Disruption Simulation & Alternate Path Routing", "MODULE 3 • SRC/RISK_SCORING.PY", 11)

    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "ALTERNATE PATH SEARCH: FIND_ALTERNATE_PATH")
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    alt_steps = [
        ("Operational Scenario:", "When a critical supplier node goes down (e.g. factory strike, export ban), can the upstream manufacturer reach the needed component through an alternate route?"),
        ("Algorithm Mechanics:", "find_alternate_path(graph, start, target, avoid_node):\n• Queue stores (current_node, path_so_far)\n• Performs BFS from start to target\n• Strictly skips neighbor == avoid_node\n• Returns shortest hop alternate path or None."),
        ("Time Complexity: O(V + E):", "Linear time BFS guaranteeing the shortest alternate bypass route in terms of supplier hops."),
        ("Integration with Simulation:", "Simulates real-world resilience: if an alternate path exists, disruption severity is downgraded from catastrophic to manageable.")
    ]
    for i, (h, b) in enumerate(alt_steps):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        p.space_after = Pt(2)
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Right Card: Simulated Case Study
    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "CASE STUDY: SIMULATING SILICA MINE HALT", border_color=ROSE)
    tb2 = s11.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    p_cs = tf2.paragraphs[0]
    p_cs.text = "SIMULATION INPUT: DISRUPT NODE 'SILICA' (Tier 4 Mine)"
    p_cs.font.bold = True
    p_cs.font.size = Pt(11)
    p_cs.font.color.rgb = ROSE
    p_cs.space_after = Pt(6)

    cascade_steps = [
        "1. Direct Dependents Hit: SIL (Silicon Wafer) & SAND (Silica Sand)",
        "2. Secondary Cascade: PCB (Circuit Board), SEN (Sensors), GLS (Glass)",
        "3. Tertiary Subsystems: EL (Electronics Subsystem), BD (Body/Exterior)",
        "4. Final Assembly: MFG (Apex Motors) HALTED! Final assembly stalls."
    ]
    for cs in cascade_steps:
        p = tf2.add_paragraph()
        p.text = cs
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(4)

    p_res = tf2.add_paragraph()
    p_res.text = "\nSIMULATION METRICS:"
    p_res.font.bold = True
    p_res.font.size = Pt(10.5)
    p_res.font.color.rgb = AMBER

    sim_m = [
        "• Downstream Blast Radius: 10 Suppliers Paralyzed",
        "• Assembly Halted: YES (Apex Motors Tier 0)",
        "• Has Contracted Backup: TRUE (Secondary mine contracted)",
        "• Recommendation: Activate dual-source contract to absorb capacity."
    ]
    for sm in sim_m:
        p = tf2.add_paragraph()
        p.text = sm
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 12: Visualization & Reporting Engine
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Graph Visualization & Automated Alert Engine", "MODULE 4 • SRC/VISUALIZE.PY", 12)

    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "VISUAL ENCODING RULES")
    tb = s12.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    vis_rules = [
        ("Design Philosophy:", "Uses NetworkX purely as a layout/drawing helper; all graph traversals, cycles, and risk scores originate from OUR OWN custom algorithms."),
        ("Visual Color Coding:", "• RED Nodes: Single Points of Failure (SPOFs) with zero backup.\n• ORANGE Nodes: Nodes trapped in detected circular dependencies.\n• BLUE Nodes: Standard stable suppliers."),
        ("Criticality-Proportional Sizing:", "Node size scales with reverse BFS downstream impact:\nnode_size = 300 + (criticality / max_criticality) * 1400\nMakes systemic bottlenecks visually prominent immediately."),
        ("Output Artifact Generation:", "Saved to: output/dependency_graph.png (DPI: 150)\nAccompanied by print_alerts() console risk digest.")
    ]
    for i, (h, b) in enumerate(vis_rules):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        p.space_after = Pt(2)
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Right Card: Embed Real Generated Image if it exists
    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "GENERATED GRAPH: OUTPUT/DEPENDENCY_GRAPH.PNG")
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "output", "dependency_graph.png"))
    if os.path.exists(img_path):
        try:
            s12.shapes.add_picture(img_path, Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.2))
        except Exception as e:
            tb_err = s12.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(2.0))
            tb_err.text_frame.text = f"Image render error: {e}"
    else:
        tb_no = s12.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(2.0))
        tb_no.text_frame.text = "Generated graph image available in output/dependency_graph.png"

    # =========================================================================
    # SLIDE 13: Testing & Validation Suite
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Testing, Verification & Code Integrity", "TEST SUITE • TESTS/", 13)

    add_card(s13, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0), "AUTOMATED UNIT TEST SUITE (100% PASS RATE)")
    tb = s13.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(11.3), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    tests = [
        ("test_graph_loading()", "PASSED", "Verifies 63 unique suppliers, 76 dependencies, Apex Motors root MFG tier 0, and correct metadata dictionary binding."),
        ("test_cycle_detection()", "PASSED", "Verifies exactly 2 circular loops detected via 3-color DFS. Asserts membership of BMS, TC, MOT, and INV."),
        ("test_spof_detection()", "PASSED", "Verifies all 16 Single Points of Failure. Asserts BC and MOT are flagged while SILICA (backup=True) is correctly exempted."),
        ("test_dijkstra()", "PASSED", "Verifies minimum lead-time distance calculations from root MFG: MFG=0d, BP=10d, PT=12d, and RAREEARTH=85d max."),
        ("test_criticality()", "PASSED", "Verifies reverse BFS predecessor reachability. Confirms SILICA >= 10 affected nodes and MCU >= 9 affected nodes."),
        ("test_alternate_path()", "PASSED", "Verifies alternate route search. Confirms MFG can reach target BP when avoiding intermediate CH.")
    ]
    for i, (t_func, t_stat, t_desc) in enumerate(tests):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"✓ {t_func}  [{t_stat}]"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = GREEN
        p.space_after = Pt(1)
        
        pd = tf.add_paragraph()
        pd.text = f"   {t_desc}"
        pd.font.size = Pt(10)
        pd.font.color.rgb = TEXT_MUTED
        pd.space_after = Pt(8)

    # =========================================================================
    # SLIDE 14: Summary & Next Steps
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Summary of Work Delivered & Future Roadmap", "PROJECT CONCLUSION", 14)

    add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "WHAT HAS BEEN IMPLEMENTED SO FAR")
    tb = s14.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(5.2), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    done_items = [
        ("High-Performance Graph Core (`src/graph.py`)", "Dual adjacency list O(V + E) memory layout, O(1) bi-directional neighbor and predecessor lookups."),
        ("Cycle & Sequencing Suite (`src/traversal.py`)", "3-Color DFS cycle detection discovering 2 real deadlocks; Kahn's topological sort build sequence validator."),
        ("Risk & Disruption Engine (`src/risk_scoring.py`)", "Reverse BFS blast-radius criticality scoring; 16-node SPOF detector; min-heap Dijkstra lead-time solver; alternate path router."),
        ("Clean 5-Tier Dataset (`data/`)", "63 active supplier facilities across 5 tiers; 76 lead-time weighted dependencies; cleaned manufacturer node typography."),
        ("Verification & Artifacts (`tests/`, `output/`)", "6 automated unit tests passing 100%; publication-ready Matplotlib dependency graph PNG output.")
    ]
    for i, (h, b) in enumerate(done_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"✓ {h}"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = CYAN
        pb = tf.add_paragraph()
        pb.text = f"  {b}"
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(6)

    add_card(s14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), "FUTURE EXTENSIONS & ROADMAP")
    tb2 = s14.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.3), Inches(4.3))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0

    future_items = [
        ("Dynamic Lead-Time Influx:", "Incorporate real-time shipping variance and port congestion stochastic edge weights into Dijkstra calculations."),
        ("Maximum Flow / Minimum Cut (Edmonds-Karp):", "Model daily parts throughput capacity to identify maximum throughput bottlenecks between Tier 4 mines and Tier 0 assembly."),
        ("Multi-Tier Inventory Buffer Optimization:", "Algorithmically determine optimal safety stock inventory levels for the 16 identified Single Points of Failure."),
        ("Automated Mitigation Contract Generation:", "Auto-suggest dual-sourcing partner candidates based on geographic proximity and tier compatibility.")
    ]
    for i, (h, b) in enumerate(future_items):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = f"➔ {h}"
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = AMBER
        pb = tf2.add_paragraph()
        pb.text = f"  {b}"
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_MUTED
        pb.space_after = Pt(8)

    # Save presentation
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "Supply_Chain_Dependency_Tracker_Review.pptx"
    build_presentation(out)
