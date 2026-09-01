import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph
from Graph.Union_find.Disjoint_set import DisjointSet
# Tree is no cycle and undirected


def quick_sort_edges(edges):
    quick_sort_edges_aux(edges, 0, len(edges) - 1)


def quick_sort_edges_aux(edges, low, high):
    if low < high:
        pivot_index = partition(edges, low, high)
        quick_sort_edges_aux(edges, low, pivot_index - 1)
        quick_sort_edges_aux(edges, pivot_index + 1, high)


def partition(edges, low, high):
    pivot = edges[high][0]
    i = low - 1

    for j in range(low, high):
        if edges[j][0] <= pivot:
            i += 1
            edges[i], edges[j] = edges[j], edges[i]

    edges[i + 1], edges[high] = edges[high], edges[i + 1]
    return i + 1


# Kruskal's Algorithm with adjacency list
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# Time Complexity:
#   Average: O(E log E)
#   Worst: O(E^2), if quick sort repeatedly chooses bad pivots.
#   We collect all edges and quick sort them by weight.
#   Union-find operations are almost O(1) each with path compression and rank.
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V + E)
#   edges stores all edge objects from the adjacency lists.
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

    for key in graph.vertices:
        vertex = graph.vertices[key]

        for edge in vertex.edges:
            edges.append((edge.weight, edge.from_vertex.key, edge.to_vertex.key))

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
