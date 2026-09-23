from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph


# Dijkstra with adjacency list + linear search
# Requirement: all edge weights must be non-negative.
#
# Time Complexity: O(V^2 + E), usually written as O(V^2)
#   We repeat at most V rounds.
#   In each round, we scan all vertices to find the unvisited vertex with the
#   smallest known distance: O(V).
#   Across the whole algorithm, all adjacency-list edges are relaxed: O(E).
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   distance stores at most V entries.
#   previous stores at most V entries.
#   visited stores at most V entries.
#
# Total Space: O(V + E)
def dijkstra_linear(graph, start_key):
    if start_key not in graph.vertices:
        return {}, {}

    distance = {}
    previous = {}

    for key in graph.vertices:
        distance[key] = inf
        previous[key] = None

    visited = set()
    distance[start_key] = 0

    for _ in range(len(graph.vertices)):
        current_key = None
        current_distance = inf

        for key in graph.vertices:
            if key not in visited and distance[key] < current_distance:
                current_key = key
                current_distance = distance[key]

        if current_key is None:
            break

        visited.add(current_key)
        current_vertex = graph.vertices[current_key]

        for edge in current_vertex.edges:
            if edge.weight < 0:
                raise ValueError("Dijkstra cannot handle negative edge weights.")

            neighbour = edge.to_vertex

            if neighbour.key in visited:
                continue

            new_distance = distance[current_key] + edge.weight

            if new_distance < distance[neighbour.key]:
                distance[neighbour.key] = new_distance
                previous[neighbour.key] = current_key

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
    graph = MapGraph(directed=False)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "B", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    graph.add_edge("D", "E", 2)
    graph.add_edge("D", "F", 6)
    graph.add_edge("E", "F", 3)

    distance, previous = dijkstra_linear(graph, "A")

    print(distance)
    print(build_path(previous, "A", "F"))
