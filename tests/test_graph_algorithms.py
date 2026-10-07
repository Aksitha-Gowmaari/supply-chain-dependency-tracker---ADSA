import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from graph import load_graph_from_csv, Graph
from traversal import detect_cycles, topological_sort, bfs, dfs
from risk_scoring import compute_criticality, find_single_points_of_failure, dijkstra, find_alternate_path

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
SUPPLIERS_CSV = os.path.join(DATA_DIR, "suppliers.csv")
DEPENDENCIES_CSV = os.path.join(DATA_DIR, "dependencies.csv")


def test_graph_loading():
    graph = load_graph_from_csv(SUPPLIERS_CSV, DEPENDENCIES_CSV)
    assert graph.num_suppliers() == 63
    assert graph.num_dependencies() == 76
    assert "MFG" in graph.get_all_suppliers()
    meta = graph.get_metadata("MFG")
    assert meta.get("name") == "Apex Motors (Main Manufacturer)"
    assert meta.get("tier") == 0


def test_cycle_detection():
    graph = load_graph_from_csv(SUPPLIERS_CSV, DEPENDENCIES_CSV)
    cycles = detect_cycles(graph)
    assert len(cycles) == 2
    # Verify BMS/TC and MOT/INV cycles
    cycle_nodes = {node for c in cycles for node in c}
    assert "BMS" in cycle_nodes and "TC" in cycle_nodes
    assert "MOT" in cycle_nodes and "INV" in cycle_nodes


def test_spof_detection():
    graph = load_graph_from_csv(SUPPLIERS_CSV, DEPENDENCIES_CSV)
    spofs = find_single_points_of_failure(graph)
    assert len(spofs) == 16
    assert "BC" in spofs
    assert "MOT" in spofs
    assert "SILICA" not in spofs  # SILICA has backup True


def test_dijkstra():
    graph = load_graph_from_csv(SUPPLIERS_CSV, DEPENDENCIES_CSV)
    lead_times = dijkstra(graph, "MFG")
    assert lead_times["MFG"] == 0
    assert lead_times["BP"] == 10
    assert lead_times["PT"] == 12
    assert "RAREEARTH" in lead_times
    assert lead_times["RAREEARTH"] == 85.0


def test_criticality():
    graph = load_graph_from_csv(SUPPLIERS_CSV, DEPENDENCIES_CSV)
    crit = dict(compute_criticality(graph))
    assert crit["SILICA"] >= 10
    assert crit["MCU"] >= 9


def test_alternate_path():
    graph = load_graph_from_csv(SUPPLIERS_CSV, DEPENDENCIES_CSV)
    # Testing alternate route
    path = find_alternate_path(graph, "MFG", "BP", avoid_node="CH")
    assert path is not None
    assert path[0] == "MFG"
