import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph
from Graph.Union_find.Set_array_disjoint_set import SetArrayDisjointSet


def quick_sort_edges(edges):
    """Sort edges by weight; the name is kept for existing callers."""
    edges.sort(key=lambda edge: edge[0])


# Kruskal's Algorithm with adjacency list and set-array disjoint set.
# This is the lecture-style version:
#   set_array[set_id] stores all vertices in that set.
#   map_array[vertex] stores which set_id the vertex belongs to.
#
# Time Complexity: O(E log E + V log V)
#   sort edges: O(E log E)
#   find: O(1) average, because map_array is a dictionary
#   all successful unions: O(V log V), because moved vertices need map_array
#   updates and the smaller set is always moved into the larger set
#
# Input Space: O(V + E)
# Auxiliary Space: O(V + E)
# Total Space: O(V + E)
def kruskal_mst_set_array(graph):
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

    disjoint_set = SetArrayDisjointSet()

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

    mst_edges, total_weight = kruskal_mst_set_array(graph)

    print(mst_edges)
    print(total_weight)
