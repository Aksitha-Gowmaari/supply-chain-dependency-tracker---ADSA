import os
import subprocess
import base64

# Load the output image as base64 to ensure it embeds seamlessly in the PDF
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "output", "dependency_graph.png"))
IMG_B64 = ""
if os.path.exists(IMAGE_PATH):
    with open(IMAGE_PATH, "rb") as img_file:
        IMG_B64 = f"data:image/png;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Supply Chain Dependency Tracker - Review Presentation</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

@page {{
    size: 14in 7.875in; /* 16:9 widescreen presentation slide size */
    margin: 0;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background-color: #0b0f19;
    color: #f8fafc;
    font-family: 'Plus Jakarta Sans', sans-serif;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}}

.slide {{
    width: 14in;
    height: 7.875in;
    page-break-after: always;
    break-after: page;
    position: relative;
    padding: 0.55in 0.8in 0.45in 0.8in;
    background: #0f172a;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}}

/* Slide Header */
.slide-header {{
    margin-bottom: 0.25in;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding-bottom: 0.15in;
}}

.kicker {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #06b6d4;
    text-transform: uppercase;
    margin-bottom: 4px;
}}

.slide-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
}}

.slide-num {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #64748b;
    background: rgba(255,255,255,0.03);
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.08);
}}

/* Grid layouts */
.grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.3in;
    flex: 1;
}}

.grid-4 {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.25in;
    flex: 1;
}}

/* Cards */
.card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 0.25in;
    display: flex;
    flex-direction: column;
}}

.card-title {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #06b6d4;
    text-transform: uppercase;
    margin-bottom: 0.15in;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.card-title.warn {{ color: #f59e0b; }}
.card-title.crit {{ color: #f43f5e; }}
.card-title.purple {{ color: #a855f7; }}

/* Typography & Lists */
p, li {{
    font-size: 11.5px;
    line-height: 1.55;
    color: #cbd5e1;
}}

strong {{
    color: #ffffff;
}}

.bullet-item {{
    margin-bottom: 0.12in;
}}

.bullet-title {{
    font-weight: 700;
    font-size: 12px;
    color: #ffffff;
    margin-bottom: 2px;
}}

.bullet-desc {{
    font-size: 11px;
    color: #94a3b8;
    line-height: 1.5;
}}

.code-box {{
    background: #090d16;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 0.18in;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    line-height: 1.5;
    color: #e2e8f0;
}}

.code-kw {{ color: #38bdf8; font-weight: bold; }}
.code-fn {{ color: #a78bfa; font-weight: bold; }}
.code-cmt {{ color: #64748b; font-style: italic; }}
.code-str {{ color: #34d399; }}

.badge {{
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 9.5px;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}}

.badge.crit {{ background: rgba(244,63,94,0.15); color: #f43f5e; border: 1px solid rgba(244,63,94,0.3); }}
.badge.warn {{ background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }}
.badge.good {{ background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }}
.badge.cyan {{ background: rgba(6,182,212,0.15); color: #06b6d4; border: 1px solid rgba(6,182,212,0.3); }}

/* Slide 1 Specifics */
.hero-title-box {{
    margin: auto 0;
}}

.hero-super {{
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2.5px;
    color: #06b6d4;
    margin-bottom: 0.15in;
}}

.hero-main-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 44px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 0.12in;
    letter-spacing: -1.5px;
}}

.hero-sub {{
    font-size: 18px;
    color: #94a3b8;
    margin-bottom: 0.35in;
    max-width: 900px;
}}

.hero-meta {{
    display: flex;
    gap: 0.4in;
    align-items: center;
    border-left: 3px solid #8b5cf6;
    padding-left: 0.25in;
}}

.hero-team {{
    font-size: 14px;
    font-weight: 700;
    color: #a855f7;
}}

.hero-course {{
    font-size: 13px;
    color: #64748b;
}}

.title-stat-bar {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.25in;
    margin-top: 0.4in;
}}

.t-stat-card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 0.18in;
}}

.t-stat-num {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 2px;
}}

.t-stat-lbl {{
    font-size: 10.5px;
    color: #06b6d4;
    font-weight: 600;
}}

.img-container {{
    flex: 1;
    background: #090d16;
    border: 1px solid #334155;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 8px;
}}

.img-container img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 6px;
}}

/* Footer */
.slide-footer {{
    margin-top: 0.2in;
    display: flex;
    justify-content: space-between;
    font-size: 9.5px;
    color: #64748b;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 0.1in;
}}
</style>
</head>
<body>

<!-- SLIDE 1: Title -->
<div class="slide">
    <div class="hero-title-box">
        <div class="hero-super">ADVANCED DATA STRUCTURES &amp; ALGORITHMS • COURSE PROJECT</div>
        <h1 class="hero-main-title">Supply Chain Dependency Tracker</h1>
        <p class="hero-sub">Graph Architecture, 3-Color Cycle Detection, Structural Criticality &amp; Disruption Simulation</p>
        <div class="hero-meta">
            <div class="hero-team">Project Team: Aksitha &amp; Khyathi</div>
            <div class="hero-course">Implementation Review • Code, Algorithms &amp; Dataset Results</div>
        </div>
    </div>
    <div class="title-stat-bar">
        <div class="t-stat-card">
            <div class="t-stat-num">63 Suppliers</div>
            <div class="t-stat-lbl">Tier 0 to Tier 4 Nodes</div>
        </div>
        <div class="t-stat-card">
            <div class="t-stat-num">76 Dependencies</div>
            <div class="t-stat-lbl">Lead-Time Weighted Edges</div>
        </div>
        <div class="t-stat-card">
            <div class="t-stat-num" style="color:#f59e0b;">02 Cycles Detected</div>
            <div class="t-stat-lbl">3-Color DFS Deadlocks</div>
        </div>
        <div class="t-stat-card">
            <div class="t-stat-num" style="color:#f43f5e;">16 SPOFs Active</div>
            <div class="t-stat-lbl">Single Points of Failure</div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 01 of 14</span>
    </div>
</div>

<!-- SLIDE 2: Problem Statement -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">ADSA FOUNDATION &amp; MOTIVATION</div>
            <div class="slide-title">Problem Statement &amp; Algorithmic Objectives</div>
        </div>
        <div class="slide-num">02</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title crit">The Multi-Tier Supply Problem</div>
            <div class="bullet-item">
                <div class="bullet-title">• Multi-Tier Opacity</div>
                <div class="bullet-desc">Modern manufacturing relies on deep multi-tier suppliers. Manufacturers manage Tier 1 suppliers directly but are blind to Tier 3 and 4 raw material nodes.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">• Circular Deadlocks</div>
                <div class="bullet-desc">Circular dependencies (A needs B, B needs C, C needs A) create topological deadlocks where procurement order cannot resolve, stalling production.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">• Single Points of Failure (SPOF)</div>
                <div class="bullet-desc">Suppliers with high downstream reliance and zero secondary backup source pose severe systemic risk to final assembly.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">• Lead-Time Compounding</div>
                <div class="bullet-desc">Procurement delays compound across chains, necessitating weighted shortest-path analysis to isolate critical bottlenecks.</div>
            </div>
        </div>
        <div class="card">
            <div class="card-title">ADSA Algorithmic Objectives</div>
            <div class="bullet-item">
                <div class="bullet-title">✓ Dual Adjacency List Graph</div>
                <div class="bullet-desc">Memory-efficient O(V + E) sparse graph structure with bidirectional neighbor and predecessor lookups.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">✓ 3-Color Depth-First Search (DFS)</div>
                <div class="bullet-desc">Linear time O(V + E) cycle detection using White/Gray/Black coloring to detect back-edges.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">✓ Kahn's Topological Sort</div>
                <div class="bullet-desc">Build ordering validation based on remaining out-degree dependency resolution.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">✓ Reverse BFS Criticality Scoring</div>
                <div class="bullet-desc">BFS over transposed predecessor edges to quantify systemic blast radius.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">✓ Min-Heap Dijkstra Algorithm</div>
                <div class="bullet-desc">O((V + E) log V) shortest weighted lead-time calculation from root vehicle manufacturer.</div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 02 of 14</span>
    </div>
</div>

<!-- SLIDE 3: Division of Work -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">CODEBASE ARCHITECTURE</div>
            <div class="slide-title">System Architecture &amp; Module Distribution</div>
        </div>
        <div class="slide-num">03</div>
    </div>
    <div class="grid-4" style="margin-bottom:0.25in;">
        <div class="card">
            <div class="card-title">src/graph.py</div>
            <div style="font-size:10.5px; font-weight:700; color:#06b6d4; margin-bottom:8px;">OWNER: Aksitha</div>
            <p>• Custom Graph class<br>• Dual adjacency lists<br>• O(1) neighbor/pred lookups<br>• CSV ingestion &amp; cleansing<br>• Smoke test harness</p>
        </div>
        <div class="card">
            <div class="card-title">src/traversal.py</div>
            <div style="font-size:10.5px; font-weight:700; color:#06b6d4; margin-bottom:8px;">OWNER: Aksitha</div>
            <p>• Iterative DFS &amp; BFS<br>• 3-Color cycle detector<br>• Cycle path reconstruction<br>• Kahn's topological sort<br>• Build sequence validator</p>
        </div>
        <div class="card">
            <div class="card-title purple">src/risk_scoring.py</div>
            <div style="font-size:10.5px; font-weight:700; color:#a855f7; margin-bottom:8px;">OWNER: Khyathi</div>
            <p>• Reverse BFS criticality<br>• SPOF audit algorithm<br>• Min-heap Dijkstra lead times<br>• Alternate route bypass<br>• Disruption simulator</p>
        </div>
        <div class="card">
            <div class="card-title purple">src/visualize.py</div>
            <div style="font-size:10.5px; font-weight:700; color:#a855f7; margin-bottom:8px;">OWNER: Khyathi</div>
            <p>• NetworkX DiGraph converter<br>• Matplotlib drawing pipeline<br>• Color-coded risk nodes<br>• Criticality-scaled sizing<br>• Automated CLI alert report</p>
        </div>
    </div>
    <div class="card" style="padding:0.18in; background:#162032; border-color:#06b6d4;">
        <div style="font-size:11px; font-weight:700; color:#06b6d4; margin-bottom:4px;">JOINT INTEGRATION &amp; VERIFICATION (Aksitha + Khyathi)</div>
        <p style="font-size:11px; color:#e2e8f0;">End-to-end execution pipeline (<code>src/main.py</code>), 5-tier dataset modeling (<code>data/</code>), and automated unit test suite (<code>tests/test_graph_algorithms.py</code>) validating 100% algorithm correctness.</p>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 03 of 14</span>
    </div>
</div>

<!-- SLIDE 4: Graph Data Structure -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">MODULE 1 • SRC/GRAPH.PY</div>
            <div class="slide-title">Graph Data Structure &amp; Design Rationale</div>
        </div>
        <div class="slide-num">04</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">Design Choice: Adjacency List</div>
            <div class="bullet-item">
                <div class="bullet-title">Why NOT an Adjacency Matrix?</div>
                <div class="bullet-desc">Supplier networks are SPARSE. With 63 nodes and 76 edges, a matrix requires V² = 3,969 cells, of which &gt;98% are empty zeros. Adjacency lists save massive memory.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Space Complexity: O(V + E)</div>
                <div class="bullet-desc">Using <code>defaultdict(list)</code> stores only active directed relationships, scaling linearly with network expansion.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Dual Adjacency Architecture</div>
                <div class="bullet-desc">
                    • <code>self.adjacency[u]</code>: Stores outgoing edges (dependencies: "who do I need").<br>
                    • <code>self.reverse_adjacency[v]</code>: Stores incoming edges (dependents: "who relies on me"). Provides instant O(1) predecessor lookups needed for blast radius.
                </div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Edge Semantics</div>
                <div class="bullet-desc">Edge <code>from_id -&gt; to_id</code> with weight W denotes that <code>from_id</code> depends on <code>to_id</code> with a procurement lead time of W days.</div>
            </div>
        </div>
        <div class="card">
            <div class="card-title">Core Implementation Code</div>
            <div class="code-box">
<span class="code-kw">class</span> Graph:
    <span class="code-kw">def</span> <span class="code-fn">__init__</span>(self):
        self.suppliers = {{}}  <span class="code-cmt"># metadata</span>
        self.adjacency = defaultdict(list)
        self.reverse_adjacency = defaultdict(list)

    <span class="code-kw">def</span> <span class="code-fn">add_dependency</span>(self, from_id, to_id, weight=1.0):
        <span class="code-cmt"># from_id depends on to_id</span>
        self.adjacency[from_id].append((to_id, weight))
        self.reverse_adjacency[to_id].append((from_id, weight))

    <span class="code-kw">def</span> <span class="code-fn">get_neighbors</span>(self, supplier_id):
        <span class="code-cmt"># who does this supplier depend on?</span>
        return self.adjacency.get(supplier_id, [])

    <span class="code-kw">def</span> <span class="code-fn">get_predecessors</span>(self, supplier_id):
        <span class="code-cmt"># who depends on this supplier?</span>
        return self.reverse_adjacency.get(supplier_id, [])
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 04 of 14</span>
    </div>
</div>

<!-- SLIDE 5: Dataset Modeling -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">DATA PIPELINE &amp; MODELING</div>
            <div class="slide-title">5-Tier Automotive Supply Chain Schema</div>
        </div>
        <div class="slide-num">05</div>
    </div>
    <div class="card" style="margin-bottom:0.25in; padding:0.18in;">
        <div class="card-title">Hierarchy Modeling across 5 Tiers (63 Nodes, 76 Edges)</div>
        <div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:12px; font-size:11px;">
            <div style="background:#090d16; padding:10px; border-radius:8px; border-left:3px solid #8b5cf6;">
                <strong style="color:#a855f7;">Tier 0 (1 Node)</strong><br>
                Apex Motors (MFG) - Final assembly plant.
            </div>
            <div style="background:#090d16; padding:10px; border-radius:8px; border-left:3px solid #06b6d4;">
                <strong style="color:#06b6d4;">Tier 1 (6 Nodes)</strong><br>
                Subsystems: BP, PT, CH, EL, IN, BD.
            </div>
            <div style="background:#090d16; padding:10px; border-radius:8px; border-left:3px solid #38bdf8;">
                <strong style="color:#38bdf8;">Tier 2 (19 Nodes)</strong><br>
                Assemblies: BC, BMS, MOT, INV, PCB, GLS.
            </div>
            <div style="background:#090d16; padding:10px; border-radius:8px; border-left:3px solid #f59e0b;">
                <strong style="color:#f59e0b;">Tier 3 (28 Nodes)</strong><br>
                Fabricators: MCU, MAG, SIL, TIRE, LCD.
            </div>
            <div style="background:#090d16; padding:10px; border-radius:8px; border-left:3px solid #f43f5e;">
                <strong style="color:#f43f5e;">Tier 4 (9 Nodes)</strong><br>
                Mines: LITH, COBALT, SILICA, IRONORE.
            </div>
        </div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">suppliers.csv Schema</div>
            <p><strong>Columns:</strong> <code>id, name, tier, has_backup</code></p>
            <p style="margin-top:6px;">• <code>id</code>: Alphanumeric node identifier (e.g. MFG, BP, MCU, SILICA).<br>
            • <code>has_backup</code>: Boolean indicating if a secondary source is contracted.<br>
            • <strong>Data Cleansing:</strong> Resolved Excel paste formula typo <code>MFG+EA2:E55</code> to <code>MFG</code> in row 2, restoring Apex Motors' Tier 0 root connections.</p>
        </div>
        <div class="card">
            <div class="card-title">dependencies.csv Schema</div>
            <p><strong>Columns:</strong> <code>from, to, weight</code></p>
            <p style="margin-top:6px;">• <code>from -&gt; to</code>: Directed relationship (<code>from</code> depends on <code>to</code>).<br>
            • <code>weight</code>: Procurement lead time in DAYS.<br>
            • <strong>Sample Edges:</strong><br>
            &nbsp;&nbsp;<code>MFG -&gt; BP (10d)</code> | <code>PT -&gt; MOT (16d)</code><br>
            &nbsp;&nbsp;<code>CATH -&gt; LITH (30d)</code> | <code>MAG -&gt; RAREEARTH (35d)</code></p>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 05 of 14</span>
    </div>
</div>

<!-- SLIDE 6: Cycle Detection -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">MODULE 2 • SRC/TRAVERSAL.PY</div>
            <div class="slide-title">Cycle Detection Algorithm via 3-Color DFS</div>
        </div>
        <div class="slide-num">06</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">Algorithm: 3-Color DFS</div>
            <div class="bullet-item">
                <div class="bullet-title">Node Coloring State Machine</div>
                <div class="bullet-desc">
                    • <strong>WHITE (0):</strong> Unvisited node.<br>
                    • <strong>GRAY (1):</strong> Currently exploring on active recursion stack.<br>
                    • <strong>BLACK (2):</strong> Fully explored node and all descendants.
                </div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Back-Edge Rule</div>
                <div class="bullet-desc">If directed traversal encounters neighbor with <code>color == GRAY</code>, a back-edge is found, proving a cycle exists.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Cycle Path Extraction</div>
                <div class="bullet-desc"><code>cycle_start = path.index(neighbor)</code><br>Extracts the exact subpath loop: <code>path[cycle_start:] + [neighbor]</code>.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Complexity: O(V + E)</div>
                <div class="bullet-desc">Linear time DFS guarantees complete discovery of all cyclic bottlenecks without redundant checks.</div>
            </div>
        </div>
        <div class="card" style="border-color:#f59e0b;">
            <div class="card-title warn">Detection Results: 2 Real Deadlock Cycles</div>
            <div style="background:#090d16; padding:14px; border-radius:8px; margin-bottom:14px; border-left:3px solid #f59e0b;">
                <div style="font-size:10px; font-weight:700; color:#f59e0b; margin-bottom:2px;">CYCLE LOOP #1 (Battery Subsystem)</div>
                <div style="font-family:'JetBrains Mono'; font-size:14px; font-weight:700; color:#fff; margin-bottom:4px;">BMS ➔ TC ➔ BMS</div>
                <p style="font-size:10.5px; color:#94a3b8;">• Battery Management System depends on Thermal Cooling (4d).<br>• Thermal Cooling depends back on BMS (3d) for temperature control.<br>• Result: Circular lock halts procurement sign-off.</p>
            </div>
            <div style="background:#090d16; padding:14px; border-radius:8px; border-left:3px solid #f59e0b;">
                <div style="font-size:10px; font-weight:700; color:#f59e0b; margin-bottom:2px;">CYCLE LOOP #2 (Powertrain Subsystem)</div>
                <div style="font-family:'JetBrains Mono'; font-size:14px; font-weight:700; color:#fff; margin-bottom:4px;">MOT ➔ INV ➔ MOT</div>
                <p style="font-size:10.5px; color:#94a3b8;">• Electric Motor depends on Inverter Systems (5d).<br>• Inverter depends back on Motor (4d) for rotor calibration.<br>• Result: Neither component can be built first.</p>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 06 of 14</span>
    </div>
</div>

<!-- SLIDE 7: Topological Sort -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">MODULE 2 • SRC/TRAVERSAL.PY</div>
            <div class="slide-title">Topological Sort &amp; Procurement Sequencing</div>
        </div>
        <div class="slide-num">07</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">Kahn's Algorithm Implementation</div>
            <div class="bullet-item">
                <div class="bullet-title">Procurement Scheduling Concept</div>
                <div class="bullet-desc">In manufacturing, procurement must start at leaf nodes (raw material mines with 0 unresolved dependencies) and advance toward Tier 0 assembly.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Out-Degree Resolution Logic</div>
                <div class="bullet-desc">
                    <code>remaining_deps = {{n: len(get_neighbors(n)) for n in nodes}}</code><br>
                    Queue initialized with suppliers having <code>remaining_deps == 0</code>.
                </div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Iterative Processing</div>
                <div class="bullet-desc">Pop supplier u, add to order. For each reliant predecessor v (from <code>get_predecessors(u)</code>), decrement <code>remaining_deps[v]</code>. If 0, push v to queue.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">DAG Validation Gate</div>
                <div class="bullet-desc">Valid order if and only if <code>len(order) == len(nodes)</code>. If less, cycles block the sequence.</div>
            </div>
        </div>
        <div class="card" style="border-color:#f43f5e;">
            <div class="card-title crit">Execution Outcome: Blocked by Cycles</div>
            <div style="background:#090d16; padding:16px; border-radius:8px; margin-bottom:14px;">
                <div style="font-size:12px; font-weight:700; color:#f43f5e; margin-bottom:6px;">Status: Incomplete Build Order</div>
                <p style="font-size:11px; color:#cbd5e1;">Kahn's algorithm orders leaf suppliers (Lithium, Rubber, Silica, Quartz) successfully, but terminates prematurely because <strong>BMS, TC, MOT, and INV</strong> have mutually unresolved dependencies.</p>
                <div class="code-box" style="margin-top:10px; font-size:10px; color:#f59e0b;">
Topological sort INCOMPLETE -- 2 cycle(s) block a valid order.
                </div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Engineering Value</div>
                <div class="bullet-desc">The algorithm prevents costly factory deadlocks by programmatically proving contract restructuring or decoupled buffering is required before procurement initiation.</div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 07 of 14</span>
    </div>
</div>

<!-- SLIDE 8: Structural Criticality -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">MODULE 3 • SRC/RISK_SCORING.PY</div>
            <div class="slide-title">Structural Criticality via Reverse BFS</div>
        </div>
        <div class="slide-num">08</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">Reverse BFS Blast Radius Algorithm</div>
            <div class="bullet-item">
                <div class="bullet-title">The Operational Blast Radius</div>
                <div class="bullet-desc">If Supplier X suffers an outage, how many other suppliers across the network will be disrupted?</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Predecessor Traversal</div>
                <div class="bullet-desc">Normal BFS follows outgoing dependencies (<code>get_neighbors</code>). Reverse BFS follows incoming dependencies (<code>get_predecessors</code>) on the transposed graph.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Criticality Metric</div>
                <div class="bullet-desc"><code>Criticality(X) = len(reachable_predecessors)</code>.<br>Measures total downstream dependent entities.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Algorithmic Discovery</div>
                <div class="bullet-desc">Criticality is NOT simply out-degree. Deep Tier 4 mines with only 2 direct customers impact over 10 manufacturing entities downstream.</div>
            </div>
        </div>
        <div class="card">
            <div class="card-title">Top 5 Systemic Bottlenecks Discovered</div>
            <div style="display:flex; flex-direction:column; gap:8px;">
                <div style="background:#090d16; padding:8px 12px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
                    <div><strong style="color:#f43f5e;">#1 SILICA</strong> (Silica Quartz Mine, Tier 4)</div>
                    <span class="badge crit">Affects 10 Suppliers</span>
                </div>
                <div style="background:#090d16; padding:8px 12px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
                    <div><strong style="color:#f43f5e;">#2 MCU</strong> (Microcontroller Foundry, Tier 3)</div>
                    <span class="badge crit">Affects 9 Suppliers</span>
                </div>
                <div style="background:#090d16; padding:8px 12px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
                    <div><strong style="color:#f43f5e;">#3 PETRO</strong> (Petrochemical Refinery, Tier 4)</div>
                    <span class="badge crit">Affects 9 Suppliers</span>
                </div>
                <div style="background:#090d16; padding:8px 12px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
                    <div><strong style="color:#f59e0b;">#4 IRONORE</strong> (Iron Ore Mine, Tier 4)</div>
                    <span class="badge warn">Affects 7 Suppliers</span>
                </div>
                <div style="background:#090d16; padding:8px 12px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
                    <div><strong style="color:#f59e0b;">#5 IRON</strong> (Iron Ore Processor, Tier 3)</div>
                    <span class="badge warn">Affects 6 Suppliers</span>
                </div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 08 of 14</span>
    </div>
</div>

<!-- SLIDE 9: Single Points of Failure -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">MODULE 3 • SRC/RISK_SCORING.PY</div>
            <div class="slide-title">Single Points of Failure (SPOF) Analysis</div>
        </div>
        <div class="slide-num">09</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title crit">Dual-Condition SPOF Detection</div>
            <div class="bullet-item">
                <div class="bullet-title">SPOF Logic Formula</div>
                <div class="bullet-desc">A supplier node u is an active Single Point of Failure if and only if:
                <br><code>len(get_predecessors(u)) &gt; 0 and not has_backup</code></div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">High Systemic Vulnerability</div>
                <div class="bullet-desc">If a SPOF is disrupted, dependent suppliers have NO alternate supplier lined up. Disruption instantly halts downstream assembly.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Audit Result: 16 of 63 Nodes (25.4%)</div>
                <div class="bullet-desc">Over a quarter of the network operates with unhedged single-supplier contracts, providing an exact roadmap for secondary vendor onboarding.</div>
            </div>
        </div>
        <div class="card">
            <div class="card-title">16 Identified SPOFs by Tier</div>
            <div style="font-size:11px;">
                <div style="margin-bottom:8px;">
                    <strong style="color:#f43f5e;">Tier 2 Critical Assemblies (5 Nodes):</strong><br>
                    BC (Battery Cell), MOT (Motor Assembly), PCB (Circuit Boards), DIS (Display Panel), GLS (Glass).
                </div>
                <div style="margin-bottom:8px;">
                    <strong style="color:#f59e0b;">Tier 3 Subcomponents (7 Nodes):</strong><br>
                    CATH (Cathode), SEP (Separator), MCU (Microcontroller), MAG (Magnets), TIRE (Rubber), SIL (Silicon Wafer), LCD (LCD Panel).
                </div>
                <div>
                    <strong style="color:#06b6d4;">Tier 4 Raw Material Mining (4 Nodes):</strong><br>
                    LITH (Lithium Mine), COBALT (Cobalt Mine), RAREEARTH (Rare Earth Mine), RUBBER (Plantation).
                </div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 09 of 14</span>
    </div>
</div>

<!-- SLIDE 10: Dijkstra's Algorithm -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">MODULE 3 • SRC/RISK_SCORING.PY</div>
            <div class="slide-title">Dijkstra's Lead-Time Optimization</div>
        </div>
        <div class="slide-num">10</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">Min-Heap Dijkstra Implementation</div>
            <div class="bullet-item">
                <div class="bullet-title">Edge Weights = Lead Time in Days</div>
                <div class="bullet-desc">The shortest path from Apex Motors (MFG) to any supplier node represents the minimum procurement delivery window.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Priority Queue via heapq</div>
                <div class="bullet-desc">Greedily extracts minimum cumulative lead time node with time complexity O((V + E) log V). Runs in &lt;2ms.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">Network Statistics from MFG</div>
                <div class="bullet-desc">
                    • <strong>Average Lead Time:</strong> 27.1 Days<br>
                    • <strong>Shortest Subsystem:</strong> 6.0 Days (IN - Interior)<br>
                    • <strong>Longest Critical Chain:</strong> 85.0 Days (RAREEARTH Mine)
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-title">Shortest Lead-Time Spectrum from MFG</div>
            <div style="display:flex; flex-direction:column; gap:6px; font-size:10.5px; font-family:'JetBrains Mono';">
                <div style="background:#090d16; padding:6px 10px; border-radius:4px; color:#34d399;">
                    MFG -&gt; IN (Interior Systems): 6.0 days
                </div>
                <div style="background:#090d16; padding:6px 10px; border-radius:4px; color:#34d399;">
                    MFG -&gt; EL (Electronics): 7.0 days
                </div>
                <div style="background:#090d16; padding:6px 10px; border-radius:4px; color:#34d399;">
                    MFG -&gt; BP (Battery Pack): 10.0 days
                </div>
                <div style="background:#090d16; padding:6px 10px; border-radius:4px; color:#f59e0b;">
                    MFG -&gt; ... -&gt; BC (Battery Cell): 24.0 days
                </div>
                <div style="background:#090d16; padding:6px 10px; border-radius:4px; color:#f59e0b;">
                    MFG -&gt; ... -&gt; MCU (Microcontroller): 38.0 days
                </div>
                <div style="background:#090d16; padding:6px 10px; border-radius:4px; color:#f43f5e;">
                    MFG -&gt; ... -&gt; LITH (Lithium Mine): 64.0 days
                </div>
                <div style="background:#090d16; padding:6px 10px; border-radius:4px; color:#f43f5e;">
                    MFG -&gt; ... -&gt; RAREEARTH (Rare Earth): 85.0 days [MAX]
                </div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 10 of 14</span>
    </div>
</div>

<!-- SLIDE 11: Disruption Simulation -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">MODULE 3 • SRC/RISK_SCORING.PY</div>
            <div class="slide-title">Disruption Simulation &amp; Alternate Pathing</div>
        </div>
        <div class="slide-num">11</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">find_alternate_path Algorithm</div>
            <div class="bullet-item">
                <div class="bullet-title">Dynamic Resilience Check</div>
                <div class="bullet-desc">Evaluates if target is reachable from start when an intermediate supplier is disrupted (removed from graph).</div>
            </div>
            <div class="code-box">
<span class="code-kw">def</span> <span class="code-fn">find_alternate_path</span>(graph, start, target, avoid_node):
    queue = deque([(start, [start])])
    visited = {{start}}
    <span class="code-kw">while</span> queue:
        node, path = queue.popleft()
        <span class="code-kw">if</span> node == target: <span class="code-kw">return</span> path
        <span class="code-kw">for</span> neighbor, _ <span class="code-kw">in</span> graph.get_neighbors(node):
            <span class="code-kw">if</span> neighbor == avoid_node <span class="code-kw">or</span> neighbor <span class="code-kw">in</span> visited:
                <span class="code-kw">continue</span>
            visited.add(neighbor)
            queue.append((neighbor, path + [neighbor]))
    <span class="code-kw">return</span> <span class="code-kw">None</span>
            </div>
        </div>
        <div class="card" style="border-color:#f43f5e;">
            <div class="card-title crit">Simulated Case Study: SILICA Mine Shutdown</div>
            <div style="font-size:11px;">
                <p><strong>1. Direct Dependents Hit:</strong> SIL (Silicon Wafer) &amp; SAND (Silica Sand)</p>
                <p><strong>2. Secondary Cascade:</strong> PCB (Circuit Boards), SEN (Sensors), GLS (Glass)</p>
                <p><strong>3. Major Subsystems:</strong> EL (Electronics) and BD (Body &amp; Exterior)</p>
                <p><strong>4. Final Assembly Impact:</strong> <strong>APEX MFG HALTED</strong></p>
                <div style="background:#090d16; padding:10px; border-radius:6px; margin-top:10px; border-left:3px solid #f43f5e;">
                    <strong>Simulation Metrics:</strong><br>
                    • Blast Radius: 10 Suppliers Paralyzed<br>
                    • Final Assembly Impact: HALTED (Tier 0)<br>
                    • Secondary Backup Contracted: YES<br>
                    • Strategy: Engage pre-contracted secondary mine immediately.
                </div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 11 of 14</span>
    </div>
</div>

<!-- SLIDE 12: Graph Visualization -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">MODULE 4 • SRC/VISUALIZE.PY</div>
            <div class="slide-title">Graph Visualization &amp; Alert Engine</div>
        </div>
        <div class="slide-num">12</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">Visual Encoding Principles</div>
            <div class="bullet-item">
                <div class="bullet-title">• Color Coding Semantics</div>
                <div class="bullet-desc">
                    - <strong style="color:#f43f5e;">RED:</strong> Single Point of Failure (SPOF)<br>
                    - <strong style="color:#f59e0b;">ORANGE:</strong> Trapped in circular dependency<br>
                    - <strong style="color:#38bdf8;">BLUE:</strong> Standard stable supplier
                </div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">• Node Size Proportional to Blast Radius</div>
                <div class="bullet-desc"><code>node_size = 300 + (score / max_score) * 1400</code><br>Visually emphasizes high-impact nodes like SILICA and MCU instantly.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">• Automated Report Generation</div>
                <div class="bullet-desc">Outputs generated plot to <code>output/dependency_graph.png</code> accompanied by plain-text CLI risk alert summary.</div>
            </div>
        </div>
        <div class="card">
            <div class="card-title">Generated Output Plot (output/dependency_graph.png)</div>
            <div class="img-container">
                {"<img src='" + IMG_B64 + "' alt='Dependency Graph'/>" if IMG_B64 else "<p style='color:#64748b;'>Graph image generated in output/dependency_graph.png</p>"}
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 12 of 14</span>
    </div>
</div>

<!-- SLIDE 13: Testing & Validation -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">QUALITY ASSURANCE &amp; TESTING</div>
            <div class="slide-title">Automated Unit Testing Suite (100% Pass Rate)</div>
        </div>
        <div class="slide-num">13</div>
    </div>
    <div class="card" style="flex:1;">
        <div class="card-title" style="color:#10b981;">6 Verified Test Cases in tests/test_graph_algorithms.py</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; font-size:11px;">
            <div style="background:#090d16; padding:12px; border-radius:8px; border-left:3px solid #10b981;">
                <strong style="color:#10b981;">✓ test_graph_loading() [PASSED]</strong><br>
                <span style="color:#94a3b8;">Verifies 63 suppliers, 76 dependencies, Apex Motors root MFG tier 0, and metadata dictionary bindings.</span>
            </div>
            <div style="background:#090d16; padding:12px; border-radius:8px; border-left:3px solid #10b981;">
                <strong style="color:#10b981;">✓ test_cycle_detection() [PASSED]</strong><br>
                <span style="color:#94a3b8;">Verifies exactly 2 circular loops detected via 3-color DFS. Asserts membership of BMS, TC, MOT, and INV.</span>
            </div>
            <div style="background:#090d16; padding:12px; border-radius:8px; border-left:3px solid #10b981;">
                <strong style="color:#10b981;">✓ test_spof_detection() [PASSED]</strong><br>
                <span style="color:#94a3b8;">Verifies all 16 SPOFs identified. Asserts BC and MOT are flagged while SILICA (backup=True) is exempted.</span>
            </div>
            <div style="background:#090d16; padding:12px; border-radius:8px; border-left:3px solid #10b981;">
                <strong style="color:#10b981;">✓ test_dijkstra() [PASSED]</strong><br>
                <span style="color:#94a3b8;">Verifies minimum lead-time distance calculations from root MFG: MFG=0d, BP=10d, PT=12d, and RAREEARTH=85d max.</span>
            </div>
            <div style="background:#090d16; padding:12px; border-radius:8px; border-left:3px solid #10b981;">
                <strong style="color:#10b981;">✓ test_criticality() [PASSED]</strong><br>
                <span style="color:#94a3b8;">Verifies reverse BFS predecessor reachability. Confirms SILICA &gt;= 10 affected nodes and MCU &gt;= 9 affected nodes.</span>
            </div>
            <div style="background:#090d16; padding:12px; border-radius:8px; border-left:3px solid #10b981;">
                <strong style="color:#10b981;">✓ test_alternate_path() [PASSED]</strong><br>
                <span style="color:#94a3b8;">Verifies alternate route search. Confirms MFG can reach target BP when avoiding intermediate CH.</span>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 13 of 14</span>
    </div>
</div>

<!-- SLIDE 14: Summary & Roadmap -->
<div class="slide">
    <div class="slide-header">
        <div>
            <div class="kicker">CONCLUSION &amp; FUTURE WORK</div>
            <div class="slide-title">Summary of Work Delivered &amp; Roadmap</div>
        </div>
        <div class="slide-num">14</div>
    </div>
    <div class="grid-2">
        <div class="card">
            <div class="card-title">Accomplishments Delivered So Far</div>
            <div class="bullet-item">
                <div class="bullet-title">✓ High-Performance Graph Engine</div>
                <div class="bullet-desc">Dual adjacency list O(V + E) memory layout with O(1) bi-directional neighbor and predecessor lookups.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">✓ Traversal &amp; Sequencing Algorithms</div>
                <div class="bullet-desc">3-Color DFS cycle detection discovering 2 deadlocks; Kahn's topological sort build sequence validator.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">✓ Multi-Factor Risk Assessment</div>
                <div class="bullet-desc">Reverse BFS blast-radius scoring; 16-node SPOF audit; min-heap Dijkstra lead-time solver; alternate path router.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">✓ Verification &amp; Visual Artifacts</div>
                <div class="bullet-desc">6 unit tests passing 100%; publication-ready Matplotlib dependency graph PNG output.</div>
            </div>
        </div>
        <div class="card">
            <div class="card-title warn">Future Algorithmic Roadmap</div>
            <div class="bullet-item">
                <div class="bullet-title">➔ Stochastic Lead-Time Variations</div>
                <div class="bullet-desc">Incorporate dynamic shipping delay variances and port congestion probabilities into Dijkstra calculations.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">➔ Maximum Flow / Minimum Cut (Edmonds-Karp)</div>
                <div class="bullet-desc">Model component volume throughput capacities to identify delivery bottlenecks from Tier 4 mines to Tier 0 assembly.</div>
            </div>
            <div class="bullet-item">
                <div class="bullet-title">➔ Safety Stock Buffer Optimization</div>
                <div class="bullet-desc">Algorithmically compute optimal inventory buffer sizing for the 16 identified Single Points of Failure.</div>
            </div>
        </div>
    </div>
    <div class="slide-footer">
        <span>ADSA Technical Review Presentation</span>
        <span>Slide 14 of 14</span>
    </div>
</div>

</body>
</html>
"""

html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "presentation_slides.html"))
pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Supply_Chain_Dependency_Tracker_Review.pdf"))

with open(html_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"HTML presentation generated at: {html_path}")

# Detect browser for print-to-pdf
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

browser_exe = CHROME_PATH if os.path.exists(CHROME_PATH) else EDGE_PATH if os.path.exists(EDGE_PATH) else None

if browser_exe:
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        html_path
    ]
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"SUCCESS: High-resolution PDF generated at: {pdf_path}")
else:
    print("No headless Chrome/Edge found to convert HTML to PDF.")
