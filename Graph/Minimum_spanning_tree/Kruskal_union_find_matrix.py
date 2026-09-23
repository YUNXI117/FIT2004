import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph
from Graph.Union_find.Array_union_find import ArrayUnionFind


from Graph.Minimum_spanning_tree.Edge_sorting import sort_edges, quick_sort_edges


# Kruskal's Algorithm with adjacency matrix and array-based Union-Find.
# Optimized extension: adds path compression to the video's size-based forest.
# For the demonstrated walk-only find, see Kruskal_union_by_size_matrix.py.
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# parent[index] < 0 means this index is a root.
# abs(parent[index]) is the size of that set.
# parent[index] >= 0 means this index points to its parent index.
#
# Let V be the number of vertices and E the number of undirected edges.
# Assume O(1) weight comparisons/arithmetic and average O(1) dictionary access.
# The bounds below use this dictionary assumption, not worst-case hash collisions.
# Write log E as log(max(2, E)) to include graphs with fewer than two edges.
#
# Process:
#   1. Scan the matrix upper triangle and collect every undirected edge once.
#      Time: O(V^2). Extra Space: O(E).
#   2. Sort the E collected edges by nondecreasing weight.
#      Time: O(E log E) worst case with Python sort. Extra Space: O(E).
#   3. Create V singleton parent-array trees; every root initially stores -1.
#      Time: O(V) amortized. Extra Space: O(V).
#   4. Examine edges in sorted order. Find both roots with path compression;
#      if different, attach the smaller tree root to the larger tree root.
#      Time: O(E alpha(V)) amortized for all attempts after initialization.
#      Extra Space: O(log V) recursive stack per find; O(V) stored Union-Find.
#   5. Store each accepted original edge and stop after V - 1 accepted edges;
#      otherwise report a disconnected graph.
#      Time: O(V) total append work. Extra Space: O(V) for mst_edges.
#
# Time Complexity: O(V^2 + E log E + E alpha(V)) = O(V^2 + E log E)
#   Worst-case algorithmic work under the assumptions above:
#   scan the upper triangle of the matrix: O(V^2), even for a sparse graph
#   sort collected edges: O(E log E) worst case with Python's built-in sort
#   initialize V singleton sets: O(V) total, amortized over list appends
#   examine up to E edges, calling union (two finds) for each edge:
#     one find/union: O(log V) worst case; linking known roots alone is O(1)
#     path compression + union by size: O(alpha(V)) amortized per operation
#     initialization + all union/find operations: O(V + E alpha(V)) total
#   Amortized bounds constrain an entire worst-case operation sequence;
#   they are not an average over random inputs. alpha is inverse Ackermann.
#   At most V - 1 unions succeed, but as many as E edges may be examined.
#   total: O(V^2 + E log E + E alpha(V)) = O(V^2 + E log E)
#   For a connected simple graph this is also O(V^2 + E log V).
#   Using the single-operation worst-case bound instead gives the valid,
#   looser bound O(V^2 + E log E + E log V).
#
# Input Space: O(V^2)
# Auxiliary Space: O(V + E)
#   edges and sorting buffer: O(E); Union-Find and returned MST edges: O(V)
#   recursive find stack: O(log V)
# Total Space: O(V^2)
# Default sorter is Python sort. Pass sorter=quick_sort_edges for the lecture
# sorting choice; replace the sorting term by O(E^2) in worst-case analysis.
# Negative/zero weights are valid; self-loops are ignored. Empty graph -> ([], 0).
# Nonempty disconnected or directed graphs raise ValueError. Input is unchanged.
def kruskal_mst_matrix_union_find(graph, *, sorter=sort_edges):
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

    union_find = ArrayUnionFind()

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

    mst_edges, total_weight = kruskal_mst_matrix_union_find(graph)

    print(mst_edges)
    print(total_weight)
