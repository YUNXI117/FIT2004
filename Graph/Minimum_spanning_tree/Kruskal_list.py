import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph
from Graph.Union_find.Disjoint_set import DisjointSet


from Graph.Minimum_spanning_tree.Edge_sorting import sort_edges, quick_sort_edges


# Kruskal's Algorithm with adjacency list
# Rank + compression extension; the video demonstrates size-based parent arrays.
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# Process:
#   1. Collect every undirected edge once and build vertex_order.
#      Time: O(V + E). Extra Space: O(V + E).
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
# Time Complexity: O(V + E log E); connected graphs simplify to O(E log E).
#   Assume average O(1) dictionary access and unit-cost weight operations.
#   Collect each undirected edge once: O(V + E); initialize sets: O(V).
#   Default sorting: O(E log E) worst case; logs mean log(max(2, E)).
#   Single find/full union: O(log V) worst-case parent steps; known-root link O(1).
#   Compression + rank: O(alpha(V)) amortized per operation, so all operations
#   including initialization cost O(V + E alpha(V)). alpha is inverse Ackermann.
#   Amortized is a bound over any operation sequence, not average random inputs.
#   There may be E union attempts, even though at most V-1 succeed.
#   Full bound: O(V + E log E + E alpha(V)); connected simple graph: O(E log V).
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V + E)
#   edges stores each logical undirected edge once.
#   disjoint_set stores at most V vertices.
#   mst_edges stores V - 1 edges.
#   Python sorting buffer: O(E); recursive find stack: O(log V).
#
# Total Space: O(V + E)
# Default sorter is Python sort. Pass sorter=quick_sort_edges for the lecture
# sorting choice; replace the sorting term by O(E^2) in worst-case analysis.
# Negative/zero weights are valid; self-loops are ignored. Empty graph -> ([], 0).
# Nonempty disconnected or directed graphs raise ValueError. Input is unchanged.
def kruskal_mst(graph, *, sorter=sort_edges):
    if graph.directed:
        raise ValueError("Kruskal's algorithm only works on undirected graphs.")

    if len(graph.vertices) == 0:
        return [], 0

    edges = []
    vertex_order = {key: index for index, key in enumerate(graph.vertices)}

    for from_key, vertex in graph.vertices.items():
        for edge in vertex.edges:
            to_key = edge.to_vertex.key

            if vertex_order[from_key] < vertex_order[to_key]:
                edges.append((edge.weight, from_key, to_key))

    sorter(edges)

    disjoint_set = DisjointSet()

    for key in graph.vertices:
        disjoint_set.make_set(key)

    mst_edges = []
    total_weight = 0

    # Invariant: accepted edges form a forest contained in some MST.
    # union returns False exactly when both endpoints already share a component.
    for weight, from_key, to_key in edges:
        if disjoint_set.union(from_key, to_key):
            mst_edges.append((from_key, to_key, weight))
            total_weight += weight

            if len(mst_edges) == len(graph.vertices) - 1:
                break

    if len(mst_edges) != len(graph.vertices) - 1:
        raise ValueError("Graph is disconnected. MST is not possible.")

    return mst_edges, total_weight


if __name__ == "__main__":
    graph = MapGraph(directed=False)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "B", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    graph.add_edge("D", "E", 2)
    graph.add_edge("D", "F", 6)
    graph.add_edge("E", "F", 3)

    mst_edges, total_weight = kruskal_mst(graph)

    print(mst_edges)
    print(total_weight)
