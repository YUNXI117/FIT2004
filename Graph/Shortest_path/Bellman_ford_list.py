from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph


# Bellman-Ford with adjacency list
# Purpose: single-source shortest path.
# Requirement: graph can have negative edges, but must not have a negative cycle.
#
# Time Complexity: O(VE)
#   We relax all edges V - 1 times.
#   Then we scan all edges one more time to detect a negative cycle.
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   distance stores at most V entries.
#   previous stores at most V entries.
#
# Total Space: O(V + E)
def bellman_ford(graph, start_key):
    if start_key not in graph.vertices:
        return {}, {}

    distance = {}
    previous = {}

    for key in graph.vertices:
        distance[key] = inf
        previous[key] = None

    distance[start_key] = 0

    for _ in range(len(graph.vertices) - 1):
        updated = False

        for from_key in graph.vertices:
            from_vertex = graph.vertices[from_key]

            if distance[from_key] == inf:
                continue

            for edge in from_vertex.edges:
                to_key = edge.to_vertex.key
                weight = edge.weight

                new_distance = distance[from_key] + weight

                if new_distance < distance[to_key]:
                    distance[to_key] = new_distance
                    previous[to_key] = from_key
                    updated = True

        if not updated:
            break

    for from_key in graph.vertices:
        from_vertex = graph.vertices[from_key]

        if distance[from_key] == inf:
            continue

        for edge in from_vertex.edges:
            to_key = edge.to_vertex.key
            weight = edge.weight

            if distance[from_key] + weight < distance[to_key]:
                raise ValueError("Graph contains a negative-weight cycle.")

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
    graph = MapGraph(directed=True)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 5)
    graph.add_edge("B", "C", -2)
    graph.add_edge("C", "D", 3)

    distance, previous = bellman_ford(graph, "A")

    print(distance)
    print(build_path(previous, "A", "D"))
