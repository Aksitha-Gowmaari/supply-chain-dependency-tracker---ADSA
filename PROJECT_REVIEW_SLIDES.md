# Supply Chain Dependency Tracker & Risk Analysis
## ADSA Course Project Review — Comprehensive Technical Report & Slide Presentation

> **Project Team / Authors:** Aksitha & Khyathi  
> **Course:** Advanced Data Structures & Algorithms (ADSA)  
> **Presentation File (PPTX):** [Supply_Chain_Dependency_Tracker_Review.pptx](file:///c:/Users/aksia/OneDrive/Desktop/supply-chain-dependency-tracker---ADSA/Supply_Chain_Dependency_Tracker_Review.pptx)  
> **Scope:** Core Data Structures, Graph Algorithms, Traversal Pipelines, Risk Scoring, Testing & Real Dataset Findings.

---

### Slide 1: Title & Project Overview
- **Title:** Supply Chain Dependency Tracker & Risk Analysis
- **Subtitle:** Graph Architecture, Cycle Detection, Criticality Ranking & Failure Simulation
- **Key Metrics Highlighted:**
  - **63 Suppliers:** Multi-tier network spanning Tier 0 (Root Manufacturer) to Tier 4 (Raw Material Mines).
  - **76 Directed Dependencies:** Weighted edges representing lead-time in days.
  - **2 Circular Deadlocks:** Detected via 3-Color Depth-First Search.
  - **16 Single Points of Failure (SPOFs):** Suppliers with dependent systems and zero secondary backup source.

---

### Slide 2: Problem Statement & ADSA Objectives
- **The Supply Chain Problem:**
  - Real manufacturing networks are deep, sparse directed graphs.
  - Manufacturers are blind to sub-tier disruptions (e.g., Tier 3 fabricators or Tier 4 mining halts).
  - Circular dependencies create procurement deadlocks where components mutually wait on one another.
- **ADSA Algorithmic Objectives:**
  1. Construct a memory-efficient $O(V + E)$ Dual Adjacency List graph structure.
  2. Implement cycle detection using 3-Color Depth-First Search (DFS).
  3. Validate procurement sequence validity using Kahn's Topological Sort algorithm.
  4. Quantify systemic vulnerability using Reverse BFS criticality ranking.
  5. Identify lowest-risk lead-time routes from root assembly using Dijkstra's algorithm.
  6. Simulate dynamic node disruption and alternate bypass route discovery.

---

### Slide 3: Architecture & Division of Work
- **`src/graph.py` (Owner: Aksitha):**
  - Custom `Graph` class with dual adjacency lists (`adjacency` and `reverse_adjacency`).
  - Safe CSV data ingestion and node metadata sanitization.
- **`src/traversal.py` (Owner: Aksitha):**
  - Iterative DFS & BFS implementations.
  - 3-Color Cycle Detection with cycle path extraction.
  - Kahn's algorithm for topological sorting and build order validation.
- **`src/risk_scoring.py` (Owner: Khyathi):**
  - Reverse BFS Downstream Criticality / Blast-Radius scoring.
  - Single Point of Failure (SPOF) identification.
  - Min-Heap Dijkstra algorithm for shortest lead-time path computation.
  - `find_alternate_path` for dynamic bypass routing under disruptions.
- **`src/visualize.py` (Owner: Khyathi):**
  - NetworkX DiGraph helper and Matplotlib rendering with color-coded node sizes.
  - Automated CLI risk alert reporting.
- **`src/main.py` & `tests/` (Joint Integration):**
  - End-to-end pipeline execution and automated unit test suite.

---

### Slide 4: Graph Representation & Design Rationale
- **Why Adjacency List over Adjacency Matrix?**
  - **Sparsity:** The network has 63 vertices and 76 edges (Graph Density $\approx 1.9\%$).
  - **Space Complexity:** Adjacency list requires $O(V + E)$ memory compared to an adjacency matrix requiring $O(V^2) = 63^2 = 3,969$ cells, where $>98\%$ are redundant zeros.
  - **Lookup Time:** Retrieving dependencies takes $O(\text{deg}(v))$ rather than scanning an entire row of length $V$.
- **Dual Adjacency Implementation:**
  ```python
  self.adjacency = defaultdict(list)          # from_id -> [(to_id, weight)]
  self.reverse_adjacency = defaultdict(list)  # to_id   -> [(from_id, weight)]
  ```
  - `self.adjacency`: Answers *"Who does supplier $X$ depend on?"*
  - `self.reverse_adjacency`: Answers *"Who depends on supplier $X$?"* (Provides instant $O(1)$ predecessor lookup needed for reverse blast radius calculation).

---

### Slide 5: Supply Chain Dataset Modeling
- **5-Tier Automotive Model:**
  - **Tier 0:** Apex Motors (`MFG`) — Root automotive manufacturer.
  - **Tier 1 (6 Nodes):** Major Subsystems (`BP` Battery Pack, `PT` Powertrain, `CH` Chassis, `EL` Electronics, `IN` Interior, `BD` Body).
  - **Tier 2 (19 Nodes):** Key Components (`BC` Battery Cell, `BMS`, `MOT` Motor, `INV` Inverter, `PCB`, `GLS` Glass, `STL` Steel, etc.).
  - **Tier 3 (28 Nodes):** Subcomponents & Fabricators (`MCU` Microcontroller, `MAG` Magnets, `SIL` Silicon, `LCD`, `PAD` Brake Pads, etc.).
  - **Tier 4 (9 Nodes):** Raw Material Mines (`LITH` Lithium, `COBALT` Cobalt, `SILICA` Silica, `RAREEARTH` Rare Earth, `RUBBER`, `PETRO`).
- **Data Cleansing Resolution:**
  - Row 2 of `suppliers.csv` originally contained `"MFG+EA2:E55"` due to an Excel formula copy artifact. Corrected to `"MFG"` with defensive string splitting in `load_graph_from_csv` to ensure Apex Motors metadata connects cleanly across all tiers.

---

### Slide 6: Cycle Detection Algorithm (3-Color DFS)
- **Algorithm State Representation:**
  - `WHITE (0)`: Unvisited node.
  - `GRAY (1)`: Currently active on the DFS recursion stack.
  - `BLACK (2)`: Fully explored node and all descendants.
- **Back-Edge Detection:**
  - If a directed edge $u \to v$ encounters a node where `color[v] == GRAY`, a back-edge is found, proving the existence of a circular dependency.
- **Findings in the Dataset:**
  1. **Loop 1:** `BMS ➔ TC ➔ BMS`  
     *Battery Management System depends on Thermal Cooling (4d), which depends on BMS (3d).*
  2. **Loop 2:** `MOT ➔ INV ➔ MOT`  
     *Electric Motor Assembly depends on Inverter Systems (5d), which depends on Motor (4d).*
- **Practical Impact:** Neither component can finish procurement first without decoupled buffering or redesigned contracts.

---

### Slide 7: Topological Sort & Procurement Sequencing
- **Kahn's Algorithm Implementation:**
  - Evaluates remaining outgoing dependencies for every node:
    ```python
    remaining_deps = {node: len(graph.get_neighbors(node)) for node in nodes}
    queue = deque([node for node in nodes if remaining_deps[node] == 0])
    ```
  - Leaf raw materials (zero unresolved dependencies) enter the queue first.
  - As nodes resolve, dependent predecessors have their remaining counts decremented.
- **Execution Outcome:**
  - `is_valid = False`: Full build order blocked by the 2 circular loops.
  - Serves as an automated validation gate preventing procurement deadlock.

---

### Slide 8: Structural Criticality via Reverse BFS
- **Algorithm Mechanics:**
  - Performs Breadth-First Search following `reverse_adjacency` edges starting from node $v$.
  - $\text{Criticality}(v) = |\{u \in V : v \text{ reaches } u \text{ in } G_{\text{reversed}}\}| - 1$.
- **Top 5 Critical Systemic Bottlenecks:**
  1. **`SILICA` (Silica Quartz Mine, Tier 4):** Affects **10 other suppliers** if disrupted.
  2. **`MCU` (Microcontroller Foundry, Tier 3):** Affects **9 other suppliers** if disrupted.
  3. **`PETRO` (Petrochemical Refinery, Tier 4):** Affects **9 other suppliers** if disrupted.
  4. **`IRONORE` (Iron Ore Mine, Tier 4):** Affects **7 other suppliers** if disrupted.
  5. **`IRON` (Iron Ore Processor, Tier 3):** Affects **6 other suppliers** if disrupted.
- **Key Insight:** Raw material extraction facilities (Tier 4) have a vastly larger systemic blast radius than high-level Tier 1 subsystem suppliers.

---

### Slide 9: Single Points of Failure (SPOF) Analysis
- **Definition:**
  - A node is flagged as a Single Point of Failure if it has active dependents and no secondary backup:
    $$\text{len}(\text{get\_predecessors}(u)) > 0 \quad \land \quad \text{has\_backup} == \text{False}$$
- **Results:**
  - **16 of 63 suppliers (25.4%)** are unhedged Single Points of Failure:
    - **Tier 2 (5):** `BC` (Battery Cell), `MOT` (Motor), `PCB`, `DIS` (Display), `GLS` (Glass).
    - **Tier 3 (7):** `CATH` (Cathode), `SEP` (Separator), `MCU` (Microcontroller), `MAG` (Magnets), `TIRE`, `SIL` (Silicon Wafer), `LCD`.
    - **Tier 4 (4):** `LITH` (Lithium), `COBALT`, `RAREEARTH`, `RUBBER`.

---

### Slide 10: Dijkstra's Algorithm & Lead-Time Analysis
- **Algorithm Mechanics:**
  - Min-heap priority queue via Python's `heapq` module ($O((V + E) \log V)$).
  - Finds the minimum cumulative lead-time in days from Apex Motors (`MFG`) to every reachable supplier.
- **Lead-Time Spectrum:**
  - **Shortest Paths (Direct Tier 1):**
    - `MFG ➔ IN` (Interior Systems): **6.0 days**
    - `MFG ➔ EL` (Electronics): **7.0 days**
    - `MFG ➔ CH` (Chassis): **8.0 days**
    - `MFG ➔ BD` (Body): **9.0 days**
    - `MFG ➔ BP` (Battery Pack): **10.0 days**
  - **Longest Paths (Deep Tier 4 Mines):**
    - `MFG ➔ ... ➔ LITH` (Lithium Mine): **64.0 days**
    - `MFG ➔ ... ➔ COBALT` (Cobalt Mine): **70.0 days**
    - `MFG ➔ ... ➔ RAREEARTH` (Rare Earth Ore): **85.0 days** *(Longest procurement path)*
  - **Network Average Lead Time:** **27.1 days**.

---

### Slide 11: Disruption Simulation & Alternate Paths
- **Algorithm (`find_alternate_path`):**
  - Evaluates whether target node $T$ is still reachable from start node $S$ when an intermediate supplier node $A$ is avoided:
    ```python
    def find_alternate_path(graph, start, target, avoid_node):
        queue = deque([(start, [start])])
        while queue:
            node, path = queue.popleft()
            if node == target: return path
            for neighbor, _ in graph.get_neighbors(node):
                if neighbor == avoid_node or neighbor in visited: continue
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
        return None
    ```
- **Simulated Case Study — Disruption of `SILICA` (Tier 4 Mine):**
  - Direct dependents hit: `SIL` (Silicon Wafer) and `SAND` (Silica Sand).
  - Secondary cascades: `PCB`, `SEN`, `GLS`.
  - Tertiary cascades: `EL` (Electronics) and `BD` (Body).
  - Root assembly: `MFG` **HALTED**.
  - Total blast radius: **10 suppliers paralyzed**.

---

### Slide 12: Graph Visualization & Reporting
- **Visual Encoding via NetworkX & Matplotlib:**
  - **Red Nodes:** Single Points of Failure (16 nodes).
  - **Orange Nodes:** Circular dependency participants (4 nodes: `BMS`, `TC`, `MOT`, `INV`).
  - **Blue Nodes:** Stable suppliers.
  - **Node Size:** Proportional to reverse BFS criticality score ($300 + (\text{score} / \text{max}) \times 1400$).
- **Output Artifact:**
  - Saved to [`output/dependency_graph.png`](file:///c:/Users/aksia/OneDrive/Desktop/supply-chain-dependency-tracker---ADSA/output/dependency_graph.png) (embedded directly in presentation Slide 12).

---

### Slide 13: Testing & Code Verification
- **Automated Unit Tests in [`tests/test_graph_algorithms.py`](file:///c:/Users/aksia/OneDrive/Desktop/supply-chain-dependency-tracker---ADSA/tests/test_graph_algorithms.py):**
  1. `test_graph_loading()`: Validates 63 suppliers, 76 dependencies, Apex Motors root MFG tier 0.
  2. `test_cycle_detection()`: Validates 2 circular loops (`BMS ⇄ TC` and `MOT ⇄ INV`).
  3. `test_spof_detection()`: Validates 16 Single Points of Failure and backup flag logic.
  4. `test_dijkstra()`: Validates lead-time shortest paths (MFG: 0d, BP: 10d, RAREEARTH: 85d).
  5. `test_criticality()`: Validates reverse BFS reachability (SILICA: 10, MCU: 9).
  6. `test_alternate_path()`: Validates alternate route bypass routing.
- **Results:** **100% Pass Rate (6/6 passing)**.

---

### Slide 14: Summary & Future Roadmap
- **Accomplishments Delivered:**
  - $O(V + E)$ Dual Adjacency List graph structure.
  - 3-Color DFS cycle detection & Kahn's Topological Sort.
  - Reverse BFS blast-radius scoring & 16-node SPOF audit.
  - Min-Heap Dijkstra lead-time solver & dynamic alternate path router.
  - 100% test coverage with verified dataset modeling.
- **Future Roadmap:**
  - Stochastic lead-time weights modeling port congestion.
  - Edmonds-Karp Max-Flow / Min-Cut to evaluate volume throughput bottlenecks.
  - Algorithmic safety stock calculation for the 16 Single Points of Failure.
