import os
import sys
import csv
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Ensure src/ is on Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from graph import load_graph_from_csv
from traversal import detect_cycles, topological_sort, bfs
from risk_scoring import (
    compute_criticality,
    find_single_points_of_failure,
    dijkstra,
    find_alternate_path
)

app = FastAPI(
    title="Supply Chain Intelligence API",
    description="Enterprise API for supply chain graph topology, risk scoring, cycle detection, and disruption simulation.",
    version="2.0.0"
)

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(FRONTEND_DIR):
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
SUPPLIERS_CSV = os.path.join(DATA_DIR, "suppliers.csv")
DEPENDENCIES_CSV = os.path.join(DATA_DIR, "dependencies.csv")


def get_current_graph():
    """Build fresh Graph instance from CSV files."""
    return load_graph_from_csv(SUPPLIERS_CSV, DEPENDENCIES_CSV)


def classify_risk(is_spof: bool, in_cycle: bool, criticality_score: int, lead_time: float) -> str:
    """Classify node risk tier based on structural factors."""
    if is_spof or criticality_score >= 8 or in_cycle:
        return "critical"
    elif criticality_score >= 4 or lead_time >= 35:
        return "high"
    elif criticality_score >= 2 or lead_time >= 20:
        return "medium"
    return "low"


# ---------------------------------------------------------
# Models
# ---------------------------------------------------------
class DisruptionRequest(BaseModel):
    supplier_id: str


# ---------------------------------------------------------
# Health & Root
# ---------------------------------------------------------
@app.get("/dashboard")
def dashboard():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Frontend index.html not found"}


@app.get("/")
def home():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "service": "SupplyChain Intelligence Platform API",
        "version": "2.0.0",
        "engine": "ADSA Graph Architecture"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "engine": "operational",
        "graph_loaded": True
    }


# ---------------------------------------------------------
# Overview KPIs
# ---------------------------------------------------------
@app.get("/api/overview")
def get_overview():
    graph = get_current_graph()
    cycles = detect_cycles(graph)
    spofs = find_single_points_of_failure(graph)
    criticality = dict(compute_criticality(graph))
    lead_times = dijkstra(graph, "MFG")
    _order, is_acyclic = topological_sort(graph)

    cycle_nodes = set()
    for c in cycles:
        cycle_nodes.update(c)

    risk_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for node in graph.get_all_suppliers():
        level = classify_risk(
            is_spof=node in spofs,
            in_cycle=node in cycle_nodes,
            criticality_score=criticality.get(node, 0),
            lead_time=lead_times.get(node, 999)
        )
        risk_counts[level] += 1

    valid_leads = [v for k, v in lead_times.items() if k != "MFG"]
    avg_lead = round(sum(valid_leads) / len(valid_leads), 1) if valid_leads else 0
    max_lead = round(max(valid_leads), 1) if valid_leads else 0

    return {
        "total_suppliers": graph.num_suppliers(),
        "total_dependencies": graph.num_dependencies(),
        "total_cycles": len(cycles),
        "total_spofs": len(spofs),
        "risk_distribution": risk_counts,
        "is_acyclic": is_acyclic,
        "avg_lead_time_days": avg_lead,
        "max_lead_time_days": max_lead,
        "system_status": "VULNERABILITIES_DETECTED" if (spofs or cycles) else "OPTIMAL"
    }


# ---------------------------------------------------------
# Network Graph (Vis.js / Cytoscape formatted)
# ---------------------------------------------------------
@app.get("/api/network-graph")
def get_network_graph():
    graph = get_current_graph()
    cycles = detect_cycles(graph)
    spofs = set(find_single_points_of_failure(graph))
    criticality = dict(compute_criticality(graph))
    lead_times = dijkstra(graph, "MFG")

    cycle_nodes = set()
    cycle_edge_set = set()
    for c in cycles:
        cycle_nodes.update(c)
        for i in range(len(c) - 1):
            cycle_edge_set.add((c[i], c[i+1]))

    nodes = []
    for node_id in graph.get_all_suppliers():
        meta = graph.get_metadata(node_id)
        is_spof = node_id in spofs
        is_cycle = node_id in cycle_nodes
        crit_score = criticality.get(node_id, 0)
        lead_time = lead_times.get(node_id, None)

        risk_level = classify_risk(is_spof, is_cycle, crit_score, lead_time if lead_time is not None else 999)

        tier_val = meta.get("tier", 1)
        try:
            tier_num = int(tier_val)
        except (ValueError, TypeError):
            tier_num = 1

        nodes.append({
            "id": node_id,
            "label": node_id,
            "name": meta.get("name", node_id),
            "tier": tier_num,
            "has_backup": meta.get("has_backup", False),
            "is_spof": is_spof,
            "is_cycle": is_cycle,
            "criticality": crit_score,
            "lead_time": lead_time,
            "in_degree": len(graph.get_predecessors(node_id)),
            "out_degree": len(graph.get_neighbors(node_id)),
            "risk_level": risk_level
        })

    edges = []
    for from_id in graph.get_all_suppliers():
        for to_id, weight in graph.get_neighbors(from_id):
            is_c = (from_id, to_id) in cycle_edge_set
            edges.append({
                "from": from_id,
                "to": to_id,
                "weight": weight,
                "is_cycle": is_c,
                "label": f"{weight}d"
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "cycles": cycles,
        "spofs": list(spofs)
    }


# ---------------------------------------------------------
# Risk Summary & Criticality
# ---------------------------------------------------------
@app.get("/api/risk-summary")
def get_risk_summary():
    graph = get_current_graph()
    cycles = detect_cycles(graph)
    spofs = find_single_points_of_failure(graph)
    criticality = compute_criticality(graph)
    lead_times = dijkstra(graph, "MFG")

    cycle_nodes = set()
    for c in cycles:
        cycle_nodes.update(c)

    risk_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for node in graph.get_all_suppliers():
        crit_score = dict(criticality).get(node, 0)
        level = classify_risk(
            is_spof=node in spofs,
            in_cycle=node in cycle_nodes,
            criticality_score=crit_score,
            lead_time=lead_times.get(node, 999)
        )
        risk_counts[level] += 1

    spof_details = []
    for node_id in spofs:
        meta = graph.get_metadata(node_id)
        dependents = [d for d, _ in graph.get_predecessors(node_id)]
        crit_score = dict(criticality).get(node_id, 0)
        spof_details.append({
            "id": node_id,
            "name": meta.get("name", node_id),
            "tier": meta.get("tier", 1),
            "dependent_count": len(dependents),
            "dependents": dependents,
            "criticality_score": crit_score,
            "lead_time": lead_times.get(node_id, None)
        })

    spof_details.sort(key=lambda x: (x["criticality_score"], x["dependent_count"]), reverse=True)

    top_critical = []
    for node_id, score in criticality[:10]:
        meta = graph.get_metadata(node_id)
        top_critical.append({
            "id": node_id,
            "name": meta.get("name", node_id),
            "tier": meta.get("tier", 1),
            "impact_score": score,
            "has_backup": meta.get("has_backup", False),
            "is_spof": node_id in spofs,
            "lead_time": lead_times.get(node_id, None)
        })

    formatted_cycles = []
    for c in cycles:
        formatted_cycles.append({
            "cycle_path": c,
            "readable": " ➔ ".join(c),
            "length": len(c) - 1
        })

    return {
        "risk_distribution": risk_counts,
        "total_spofs": len(spofs),
        "spof_list": spof_details,
        "total_cycles": len(cycles),
        "cycle_list": formatted_cycles,
        "top_critical_suppliers": top_critical
    }


# ---------------------------------------------------------
# Suppliers Directory
# ---------------------------------------------------------
@app.get("/api/suppliers")
def get_suppliers(
    search: Optional[str] = None,
    tier: Optional[str] = None,
    risk: Optional[str] = None
):
    graph = get_current_graph()
    spofs = set(find_single_points_of_failure(graph))
    criticality = dict(compute_criticality(graph))
    lead_times = dijkstra(graph, "MFG")
    cycles = detect_cycles(graph)

    cycle_nodes = set()
    for c in cycles:
        cycle_nodes.update(c)

    results = []
    for node_id in graph.get_all_suppliers():
        meta = graph.get_metadata(node_id)
        name = meta.get("name", node_id)
        tier_val = meta.get("tier", 1)
        has_backup = meta.get("has_backup", False)
        is_spof = node_id in spofs
        is_cycle = node_id in cycle_nodes
        crit = criticality.get(node_id, 0)
        lead = lead_times.get(node_id, None)
        level = classify_risk(is_spof, is_cycle, crit, lead if lead is not None else 999)

        # Filters
        if search:
            q = search.lower()
            if q not in node_id.lower() and q not in name.lower():
                continue

        if tier is not None and str(tier_val) != str(tier):
            continue

        if risk:
            if risk == "spof" and not is_spof:
                continue
            elif risk == "cycle" and not is_cycle:
                continue
            elif risk in ["critical", "high", "medium", "low"] and level != risk:
                continue

        # Neighbors / Predecessors
        depends_on = [{"id": to, "weight": w} for to, w in graph.get_neighbors(node_id)]
        relied_on_by = [{"id": fr, "weight": w} for fr, w in graph.get_predecessors(node_id)]

        results.append({
            "id": node_id,
            "name": name,
            "tier": tier_val,
            "has_backup": has_backup,
            "is_spof": is_spof,
            "is_cycle": is_cycle,
            "risk_level": level,
            "criticality": crit,
            "lead_time": lead,
            "depends_on": depends_on,
            "relied_on_by": relied_on_by
        })

    return {
        "total": len(results),
        "suppliers": results
    }


# ---------------------------------------------------------
# Dependencies List
# ---------------------------------------------------------
@app.get("/api/dependencies")
def get_dependencies():
    graph = get_current_graph()
    spofs = set(find_single_points_of_failure(graph))
    cycles = detect_cycles(graph)

    cycle_edges = set()
    for c in cycles:
        for i in range(len(c) - 1):
            cycle_edges.add((c[i], c[i+1]))

    deps = []
    for from_id in graph.get_all_suppliers():
        for to_id, weight in graph.get_neighbors(from_id):
            is_cycle_edge = (from_id, to_id) in cycle_edges
            to_is_spof = to_id in spofs

            if is_cycle_edge or (to_is_spof and weight >= 15):
                exposure = "critical"
            elif to_is_spof or weight >= 20:
                exposure = "high"
            elif weight >= 10:
                exposure = "medium"
            else:
                exposure = "low"

            from_meta = graph.get_metadata(from_id)
            to_meta = graph.get_metadata(to_id)

            deps.append({
                "from": from_id,
                "from_name": from_meta.get("name", from_id),
                "to": to_id,
                "to_name": to_meta.get("name", to_id),
                "weight": weight,
                "is_cycle_edge": is_cycle_edge,
                "to_is_spof": to_is_spof,
                "exposure": exposure
            })

    return {
        "total_dependencies": len(deps),
        "dependencies": deps
    }


# ---------------------------------------------------------
# Backward Compatible Endpoints
# ---------------------------------------------------------
@app.get("/suppliers")
def legacy_suppliers():
    return get_suppliers()


@app.get("/dependencies")
def legacy_dependencies():
    return get_dependencies()


@app.get("/cycles")
def legacy_cycles():
    graph = get_current_graph()
    cycles = detect_cycles(graph)
    return {
        "total_cycles": len(cycles),
        "cycles": cycles
    }


# ---------------------------------------------------------
# Disruption Simulation Engine
# ---------------------------------------------------------
@app.post("/api/simulate-disruption")
def simulate_disruption(payload: DisruptionRequest):
    node_id = payload.supplier_id.strip()
    graph = get_current_graph()

    if node_id not in graph.get_all_suppliers():
        raise HTTPException(status_code=404, detail=f"Supplier '{node_id}' not found in network.")

    meta = graph.get_metadata(node_id)
    name = meta.get("name", node_id)
    has_backup = meta.get("has_backup", False)

    # Compute cascade blast radius (all suppliers that depend directly or indirectly on node_id)
    # This is a BFS traversal on the REVERSE adjacency graph
    from collections import deque
    affected = []
    visited = {node_id}
    queue = deque([node_id])

    while queue:
        curr = queue.popleft()
        for dep, _weight in graph.get_predecessors(curr):
            if dep not in visited:
                visited.add(dep)
                queue.append(dep)
                affected.append({
                    "id": dep,
                    "name": graph.get_metadata(dep).get("name", dep),
                    "tier": graph.get_metadata(dep).get("tier", 1),
                    "direct_parent": curr
                })

    mfg_impacted = any(a["id"] == "MFG" for a in affected) or node_id == "MFG"

    # Check alternate path if this supplier supplies something to its direct parents
    alternate_routes = []
    for parent, _w in graph.get_predecessors(node_id):
        # Can parent reach anything that node_id was providing?
        for child, _cw in graph.get_neighbors(node_id):
            alt_path = find_alternate_path(graph, start=parent, target=child, avoid_node=node_id)
            if alt_path:
                alternate_routes.append({
                    "from": parent,
                    "to": child,
                    "bypass_path": " ➔ ".join(alt_path)
                })

    severity = "CRITICAL" if mfg_impacted or len(affected) >= 5 else "HIGH" if len(affected) >= 2 else "MODERATE"

    return {
        "disrupted_node": node_id,
        "name": name,
        "tier": meta.get("tier", 1),
        "has_backup": has_backup,
        "severity": severity,
        "affected_count": len(affected),
        "mfg_halted": mfg_impacted,
        "affected_suppliers": affected,
        "alternate_routes_found": len(alternate_routes),
        "alternate_routes": alternate_routes[:5],
        "recommendation": (
            "EMERGENCY: Immediate procurement intervention required. Dual-sourcing or buffer inventory activation needed."
            if not has_backup else
            "Backup protocol active. Engage pre-contracted secondary suppliers to mitigate lead-time slippage."
        )
    }


# ---------------------------------------------------------
# Alternate Route Finder
# ---------------------------------------------------------
@app.get("/api/alternate-path")
def check_alternate_path(
    start: str = Query(..., description="Start supplier ID"),
    target: str = Query(..., description="Target supplier ID"),
    avoid: str = Query(..., description="Disrupted supplier ID to avoid")
):
    graph = get_current_graph()
    path = find_alternate_path(graph, start=start, target=target, avoid_node=avoid)
    return {
        "start": start,
        "target": target,
        "avoid": avoid,
        "has_alternate_path": path is not None,
        "alternate_path": path,
        "path_str": " ➔ ".join(path) if path else "No viable bypass path found."
    }


# ---------------------------------------------------------
# Procurement Order (Topological Sort)
# ---------------------------------------------------------
@app.get("/api/procurement-order")
def get_procurement_order():
    graph = get_current_graph()
    order, is_valid = topological_sort(graph)
    cycles = detect_cycles(graph)

    return {
        "is_acyclic": is_valid,
        "total_suppliers_ordered": len(order),
        "recommended_order": order if is_valid else [],
        "blocking_cycles": [" ➔ ".join(c) for c in cycles] if not is_valid else [],
        "message": "Valid build order established." if is_valid else f"Build order blocked by {len(cycles)} circular dependencies."
    }