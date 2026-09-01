import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph
from Graph.Union_find.Set_array_disjoint_set import SetArrayDisjointSet


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


# Kruskal's Algorithm with adjacency matrix and set-array disjoint set.
# This is the lecture-style version:
#   set_array[set_id] stores all vertices in that set.
#   map_array[vertex] stores which set_id the vertex belongs to.
#
# Average Time Complexity: O(V^2 + E log E + V log V)
#   collect edges from matrix: O(V^2)
#   quick sort edges: O(E log E) average
#   find: O(1) average, because map_array is a dictionary
#   union: O(size of smaller set), because moved vertices need map_array updates
#
# Worst Time Complexity: O(V^2 + E^2 + V log V)
#   quick sort can be O(E^2) with bad pivots.
#
# Input Space: O(V^2)
# Auxiliary Space: O(V + E)
# Total Space: O(V^2)
def kruskal_mst_matrix_set_array(graph):
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

    disjoint_set = SetArrayDisjointSet()

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

    mst_edges, total_weight = kruskal_mst_matrix_set_array(graph)

    print(mst_edges)
    print(total_weight)
