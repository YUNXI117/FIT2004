from heapq import heappop, heappush
from itertools import count
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph


# Prim's Algorithm with adjacency list
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
#
# Time Complexity: O(E log V)
#   Each edge can be pushed into the priority queue.
#   The duplicate heap can contain O(E) entries, so each heap operation is
#   O(log E). Since E <= V^2 in a simple graph, log E = O(log V).
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(E)
#   visited stores at most V vertices.
#   priority_queue can store at most E edges.
#   mst_edges stores V - 1 edges.
#
# Total Space: O(V + E)
def prim_mst(graph, start_key=None):
    if graph.directed:
        raise ValueError("Prim's algorithm only works on undirected graphs.")

    if len(graph.vertices) == 0:
        return [], 0

    if start_key is None:
        start_key = next(iter(graph.vertices))

    if start_key not in graph.vertices:
        raise KeyError(start_key)

    visited = set()
    priority_queue = []
    tie_breaker = count()
    mst_edges = []
    total_weight = 0

    start_vertex = graph.vertices[start_key]
    visited.add(start_key)

    for edge in start_vertex.edges:
        heappush(priority_queue, (edge.weight, next(tie_breaker), start_key, edge.to_vertex))

    while len(priority_queue) > 0 and len(visited) < len(graph.vertices):
        weight, _, from_key, to_vertex = heappop(priority_queue)

        if to_vertex.key in visited:
            continue

        visited.add(to_vertex.key)
        mst_edges.append((from_key, to_vertex.key, weight))
        total_weight += weight

        for edge in to_vertex.edges:
            if edge.to_vertex.key not in visited:
                heappush(priority_queue, (edge.weight, next(tie_breaker), to_vertex.key, edge.to_vertex))

    if len(visited) != len(graph.vertices):
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

    mst_edges, total_weight = prim_mst(graph, "A")

    print(mst_edges)
    print(total_weight)
