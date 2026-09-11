from heapq import heappop, heappush
from itertools import count
from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph


# Dijkstra with adjacency matrix + built-in priority queue
# Requirement: all edge weights must be non-negative.
#
# This version uses Python heapq, so it uses the duplicate approach:
#   If a vertex distance improves, we push a new heap entry.
#   Old heap entries are ignored after that vertex has already been visited.
#
# Time Complexity: O(V^2 + E log V)
#   Matrix scanning:
#     Each finalized vertex scans one full matrix row: O(V).
#     At most V vertices are finalized, so matrix scanning costs O(V^2).
#   Heap operations:
#     Each successful edge relaxation can push one heap entry.
#     With duplicate heap entries, there can be O(E) heap pushes.
#     heapq operations cost O(log E), and since E <= V^2, log E = O(log V).
#     So heap operations cost O(E log V).
#
# Important note:
#   You cannot always simplify O(V^2 + E log V) to O(E log V),
#   because V^2 is not always bounded by E. In a sparse graph, E can be O(V).
#   For dense graphs, where E is close to V^2, O(E log V) is a reasonable
#   simplified bound.
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V + E)
#   distance stores at most V entries.
#   previous stores at most V entries.
#   visited stores at most V entries.
#   priority_queue can store duplicate entries after distance improvements.
#
# Total Space: O(V^2)
def dijkstra_matrix_heap(graph, start_key):
    if start_key not in graph.index_map:
        return {}, {}

    distance = {}
    previous = {}

    for vertex in graph.vertices:
        distance[vertex.key] = inf
        previous[vertex.key] = None

    visited = set()
    priority_queue = []
    tie_breaker = count()

    start_index = graph.index_map[start_key]
    distance[start_key] = 0
    heappush(priority_queue, (0, next(tie_breaker), start_index))

    while len(priority_queue) > 0:
        current_distance, _, current_index = heappop(priority_queue)

        if current_index in visited:
            continue

        visited.add(current_index)
        current_vertex = graph.vertices[current_index]

        for to_index in range(len(graph.vertices)):
            weight = graph.matrix[current_index][to_index]

            if weight is None:
                continue

            if weight < 0:
                raise ValueError("Dijkstra cannot handle negative edge weights.")

            if to_index in visited:
                continue

            neighbour = graph.vertices[to_index]
            new_distance = current_distance + weight

            if new_distance < distance[neighbour.key]:
                distance[neighbour.key] = new_distance
                previous[neighbour.key] = current_vertex.key
                heappush(priority_queue, (new_distance, next(tie_breaker), to_index))

    return distance, previous


def build_path(previous, start_key, target_key):
    if target_key not in previous:
        return []

    path = []
    current_key = target_key

    while current_key is not None:
        path.append(current_key)

        if current_key == start_key:
            break

        current_key = previous[current_key]

    if path[-1] != start_key:
        return []

    path.reverse()
    return path


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

    distance, previous = dijkstra_matrix_heap(graph, "A")

    print(distance)
    print(build_path(previous, "A", "F"))
