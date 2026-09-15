import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph
from Graph.Union_find.Disjoint_set import DisjointSet


def quick_sort_edges(edges):
    """Sort edges by weight with Python sort; not hand-written quicksort."""
    edges.sort(key=lambda edge: edge[0])


# Kruskal's Algorithm with adjacency list
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# Time Complexity: O(E log E)
#   We collect each undirected edge once and sort the edges by weight.
#   Union-find operations take O(alpha(V)) amortized time each with path
#   compression and union by rank.
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V + E)
#   edges stores each logical undirected edge once.
#   disjoint_set stores at most V vertices.
#   mst_edges stores V - 1 edges.
#
# Total Space: O(V + E)
def kruskal_mst(graph):
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

    quick_sort_edges(edges)

    disjoint_set = DisjointSet()

    for key in graph.vertices:
        disjoint_set.make_set(key)

    mst_edges = []
    total_weight = 0

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
