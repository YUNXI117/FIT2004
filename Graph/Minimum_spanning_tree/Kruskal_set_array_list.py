import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph
from Graph.Union_find.Set_array_disjoint_set import SetArrayDisjointSet


from Graph.Minimum_spanning_tree.Edge_sorting import sort_edges, quick_sort_edges


# Kruskal's Algorithm with adjacency list and set-array disjoint set.
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# This is the lecture-style version:
#   Lecture05 ~36:00--44:00, set/map-table demonstration.
#   set_array[set_id] stores all vertices in that set.
#   map_array[vertex] stores which set_id the vertex belongs to.
#   Here components are Python lists; the map is a dictionary for arbitrary keys.
#
# Process:
#   1. Collect every undirected edge once and build vertex_order.
#      Time: O(V + E). Extra Space: O(V + E).
#   2. Sort the E collected edges by nondecreasing weight.
#      Time: O(E log E) worst case with Python sort. Extra Space: O(E).
#   3. Put every vertex in its own list inside set_array and record its slot
#      in map_array. Time: O(V) amortized. Extra Space: O(V).
#   4. Examine edges in sorted order. Read both slots in average O(1); when
#      different, move the smaller list and update every moved vertex's map.
#      Time: O(E + V log V) total under average O(1) hashing.
#      Extra Space: O(V) for set_array, map_array, and at most V - 1 MST edges.
#   5. Stop after V - 1 accepted edges; otherwise report a disconnected graph.
#      Time: O(1) after the scan. Extra Space: O(1).
#
# Assume average O(1) dictionary access and unit-cost weight operations.
# Time Complexity: O(V + E log E + V log V)
#   collect edges O(V + E); initialize singleton sets O(V)
#   sort edges: O(E log E)
#   find: O(1) average, because map_array is a dictionary
#   one union: O(1 + smaller size) amortized work; O(V) individual worst case
#   all successful unions: O(V log V), because moved vertices need map_array
#   updates and the smaller set is always moved into the larger set
#   every moved vertex's component doubles, so it moves at most log2(V) times
#   up to E attempts, at most V-1 successes: O(E + V log V) after initialization
#   The movement bound holds for any merge sequence, not just random inputs.
#   Hashing and list resizing have separate average/amortized assumptions.
#   Connected simple graph: O(E log V). Logs mean log(max(2, size)).
#
# Input Space: O(V + E)
# Auxiliary Space: O(V + E)
#   edge list/sort buffer O(E); component lists, map and MST output O(V)
# Total Space: O(V + E)
# Default sorter is Python sort. Pass sorter=quick_sort_edges for the lecture
# sorting choice; replace the sorting term by O(E^2) in worst-case analysis.
# Negative/zero weights are valid; self-loops are ignored. Empty graph -> ([], 0).
# Nonempty disconnected or directed graphs raise ValueError. Input is unchanged.
def kruskal_mst_set_array(graph, *, sorter=sort_edges):
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

    disjoint_set = SetArrayDisjointSet()

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

    mst_edges, total_weight = kruskal_mst_set_array(graph)

    print(mst_edges)
    print(total_weight)
