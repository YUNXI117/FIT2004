import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph
from Graph.Union_find.Python_set_disjoint_set import PythonSetDisjointSet
from Graph.Minimum_spanning_tree.Edge_sorting import sort_edges, quick_sort_edges


# Kruskal's Algorithm with adjacency matrix and Python-set components
# Lecture05 mentions the Python-set option around 32:00--35:00.
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# Each component is a Python set; map_array maps each vertex to its set slot.
# The lecture's table-based example is separately in Kruskal_set_array_*.
#
# Process:
#   1. Scan the matrix upper triangle and collect every undirected edge once.
#      Time: O(V^2). Extra Space: O(E).
#   2. Sort the E collected edges by nondecreasing weight.
#      Time: O(E log E) worst case with Python sort. Extra Space: O(E).
#   3. Create V singleton Python sets and a vertex-to-set map.
#      Time: O(V) amortized. Extra Space: O(V).
#   4. Examine edges in sorted order. Find both set slots; if they differ,
#      move the smaller set into the larger one and record the original edge.
#      Time: O(E + V log V) total under average O(1) hashing.
#      Extra Space: O(V) for components, the map, and at most V - 1 MST edges.
#   5. Stop after V - 1 accepted edges; otherwise report a disconnected graph.
#      Time: O(1) after the scan. Extra Space: O(1).
#
# Time Complexity: O(V^2 + E log E + V log V)
#   Assume average O(1) dictionary/set access and O(1) weight operations.
#   Scan the matrix upper triangle to collect edges: O(V^2).
#   Default sorting: O(E log E) worst case.
#   Find: average O(1).
#   One successful union: O(1 + smaller set size); individually up to O(V).
#   All successful unions move O(V log V) vertices in total because every moved
#   vertex joins a component at least twice as large.
#   At most E unions are attempted, although at most V - 1 succeed.
#   For a simple graph: O(V^2 + E log V).
#
# Input Space: O(V^2)
#   The graph stores a V by V adjacency matrix.
#
# Auxiliary Space: O(V + E)
#   edges and the sorting buffer use O(E).
#   component sets, map_array, and mst_edges use O(V).
#
# Total Space: O(V^2)
# Default sorter is Python sort. Pass sorter=quick_sort_edges for the lecture
# sorting choice; replace the sorting term by O(E^2) in worst-case analysis.
# Negative/zero weights are valid; self-loops are ignored. Empty graph -> ([], 0).
# Nonempty disconnected or directed graphs raise ValueError. Input is unchanged.
def kruskal_mst_matrix_python_set(graph, *, sorter=sort_edges):
    if graph.directed:
        raise ValueError("Kruskal's algorithm only works on undirected graphs.")

    vertex_count = len(graph.vertices)

    if vertex_count == 0:
        return [], 0

    edges = []

    for from_index in range(vertex_count):
        for to_index in range(from_index + 1, vertex_count):
            weight = graph.matrix[from_index][to_index]

            if weight is not None:
                from_key = graph.vertices[from_index].key
                to_key = graph.vertices[to_index].key
                edges.append((weight, from_key, to_key))

    sorter(edges)

    union_find = PythonSetDisjointSet()

    for vertex in graph.vertices:
        union_find.make_set(vertex.key)

    mst_edges = []
    total_weight = 0

    # Invariant: accepted edges form a forest contained in some MST.
    # union returns False exactly when both endpoints already share a component.
    for weight, from_key, to_key in edges:
        if union_find.union(from_key, to_key):
            mst_edges.append((from_key, to_key, weight))
            total_weight += weight

            if len(mst_edges) == vertex_count - 1:
                break

    if len(mst_edges) != vertex_count - 1:
        raise ValueError("Graph is disconnected. MST is not possible.")

    return mst_edges, total_weight


if __name__ == "__main__":
    graph = AdjacencyMatrixGraph(directed=False)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "B", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    graph.add_edge("D", "E", 2)
    graph.add_edge("D", "F", 6)
    graph.add_edge("E", "F", 3)

    mst_edges, total_weight = kruskal_mst_matrix_python_set(graph)

    print(mst_edges)
    print(total_weight)
