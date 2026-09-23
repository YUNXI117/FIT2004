import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph
from Graph.Union_find.Disjoint_set import DisjointSet


from Graph.Minimum_spanning_tree.Edge_sorting import sort_edges, quick_sort_edges


# Kruskal's Algorithm with adjacency matrix
# Rank + compression extension; the video demonstrates size-based parent arrays.
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# Process:
#   1. Scan the matrix upper triangle and collect every undirected edge once.
#      Time: O(V^2). Extra Space: O(E).
#   2. Sort the E collected edges by nondecreasing weight.
#      Time: O(E log E) worst case with Python sort. Extra Space: O(E).
#   3. Create V singleton dictionary-based trees with rank 0.
#      Time: O(V) under average O(1) hashing. Extra Space: O(V).
#   4. Examine edges in sorted order. Find both roots with path compression;
#      if different, link the lower-rank root below the higher-rank root.
#      Time: O(E alpha(V)) amortized for all attempts after initialization.
#      Extra Space: O(log V) recursive stack per find; O(V) stored Union-Find.
#   5. Store each accepted original edge and stop after V - 1 accepted edges;
#      otherwise report a disconnected graph.
#      Time: O(V) total append work. Extra Space: O(V) for mst_edges.
#
# Time Complexity: O(V^2 + E log E)
#   Assume average O(1) dictionary access and unit-cost weight operations.
#   We scan the whole matrix to collect edges: O(V^2).
#   Then we sort the collected edges by weight: O(E log E).
#   Union-find operations take O(alpha(V)) amortized time each with path
#   compression and union by rank.
#   Single find/full union: O(log V) worst-case parent steps; root linking O(1).
#   Initialize O(V); up to E attempts (at most V-1 successes): O(E alpha(V)).
#   alpha is inverse Ackermann. Amortized bounds a whole operation sequence,
#   not average random inputs; hashing is a separate average-case assumption.
#   Full bound: O(V^2 + E log E + E alpha(V)). Logs mean log(max(2, E)).
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V + E)
#   edges stores at most E edges.
#   disjoint_set stores at most V vertices.
#   mst_edges stores V - 1 edges.
#   Python sorting buffer: O(E); recursive find stack: O(log V).
#
# Total Space: O(V^2)
# Default sorter is Python sort. Pass sorter=quick_sort_edges for the lecture
# sorting choice; replace the sorting term by O(E^2) in worst-case analysis.
# Negative/zero weights are valid; self-loops are ignored. Empty graph -> ([], 0).
# Nonempty disconnected or directed graphs raise ValueError. Input is unchanged.
def kruskal_mst_matrix(graph, *, sorter=sort_edges):
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

    disjoint_set = DisjointSet()

    for vertex in graph.vertices:
        disjoint_set.make_set(vertex.key)

    mst_edges = []
    total_weight = 0

    # Invariant: accepted edges form a forest contained in some MST.
    # union returns False exactly when both endpoints already share a component.
    for weight, from_key, to_key in edges:
        if disjoint_set.union(from_key, to_key):
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

    mst_edges, total_weight = kruskal_mst_matrix(graph)

    print(mst_edges)
    print(total_weight)
