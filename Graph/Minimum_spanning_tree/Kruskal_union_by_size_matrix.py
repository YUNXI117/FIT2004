import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph
from Graph.Union_find.Array_union_find_no_compression import ArrayUnionFindNoCompression
from Graph.Minimum_spanning_tree.Edge_sorting import sort_edges, quick_sort_edges


# Kruskal's Algorithm with adjacency matrix and union by size
# Lecture05 parent-array version (~44:00--61:00), without path compression.
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# parent[index] < 0 means index is a root and abs(parent[index]) is set size.
# parent[index] >= 0 means the value is the parent index.
# The parent forest tracks components; it is not the returned MST.
#
# Process:
#   1. Scan the matrix upper triangle and collect every undirected edge once.
#      Time: O(V^2). Extra Space: O(E).
#   2. Sort the E collected edges by nondecreasing weight.
#      Time: O(E log E) worst case with Python sort. Extra Space: O(E).
#   3. Create V singleton parent-array trees; every root initially stores -1.
#      Time: O(V) amortized. Extra Space: O(V).
#   4. For every examined edge, same_set performs two Finds to test whether
#      the endpoints already have the same root.
#      Time: O(E log V) worst case. Extra Space: O(1) per iterative Find.
#   5. For at most V - 1 accepted edges, call the ADT union(u, v). Following
#      the FIT1008 ADT interface, union performs Find again internally, then
#      links the smaller root to the larger root and records the original edge.
#      Time: O(V log V) worst case. Extra Space: O(V) for mst_edges.
#   6. Stop after V - 1 accepted edges; otherwise report a disconnected graph.
#      Time: O(1) after the scan. Extra Space: O(1).
#
# Time Complexity: O(V^2 + E log E + E log V + V log V)
#   Assume average O(1) dictionary access and O(1) weight operations.
#   Scan the matrix upper triangle to collect edges: O(V^2).
#   Default sorting: O(E log E) worst case.
#   Initialize V singleton sets: O(V).
#   same_set on up to E edges: O(E log V).
#   At most V - 1 calls to the ADT union; union repeats two Finds internally,
#   so all successful Union calls cost O(V log V). Root linking alone is O(1).
#   Union by size gives height O(log V): every depth increase at least doubles
#   the component size. This version has no inverse-Ackermann bound.
#   For a connected simple graph, the complete bound simplifies to
#   O(V^2 + E log V).
#
# Input Space: O(V^2)
#   The graph stores a V by V adjacency matrix.
#
# Auxiliary Space: O(V + E)
#   edges and the sorting buffer use O(E).
#   Union-Find and mst_edges use O(V).
#   Iterative find uses O(1) temporary space.
#
# Total Space: O(V^2)
# Default sorter is Python sort. Pass sorter=quick_sort_edges for the lecture
# sorting choice; replace the sorting term by O(E^2) in worst-case analysis.
# Negative/zero weights are valid; self-loops are ignored. Empty graph -> ([], 0).
# Nonempty disconnected or directed graphs raise ValueError. Input is unchanged.
def kruskal_mst_matrix_union_by_size(graph, *, sorter=sort_edges):
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

    union_find = ArrayUnionFindNoCompression()

    for vertex in graph.vertices:
        union_find.make_set(vertex.key)

    mst_edges = []
    total_weight = 0

    # FIT1008 ADT-style workflow used in the lecture:
    # same_set performs Find for the edge check; a successful union(u, v)
    # performs Find again internally before linking the two roots.
    # Invariant: accepted edges form a forest contained in some MST.
    for weight, from_key, to_key in edges:
        if not union_find.same_set(from_key, to_key):
            union_find.union(from_key, to_key)
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

    mst_edges, total_weight = kruskal_mst_matrix_union_by_size(graph)

    print(mst_edges)
    print(total_weight)
