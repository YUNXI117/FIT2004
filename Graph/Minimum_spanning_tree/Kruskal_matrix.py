import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph
from Graph.Union_find.Disjoint_set import DisjointSet


def quick_sort_edges(edges):
    """Sort edges by weight; the name is kept for existing callers."""
    edges.sort(key=lambda edge: edge[0])


# Kruskal's Algorithm with adjacency matrix
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# Time Complexity: O(V^2 + E log E)
#   We scan the whole matrix to collect edges: O(V^2).
#   Then we sort the collected edges by weight: O(E log E).
#   Union-find operations take O(alpha(V)) amortized time each with path
#   compression and union by rank.
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V + E)
#   edges stores at most E edges.
#   disjoint_set stores at most V vertices.
#   mst_edges stores V - 1 edges.
#
# Total Space: O(V^2)
def kruskal_mst_matrix(graph):
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

    quick_sort_edges(edges)

    disjoint_set = DisjointSet()

    for vertex in graph.vertices:
        disjoint_set.make_set(vertex.key)

    mst_edges = []
    total_weight = 0

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
