from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph


# Bellman-Ford with adjacency matrix
# Purpose: single-source shortest path.
# Requirement: graph can have negative edges, but must not have a negative cycle.
#
# Standard Bellman-Ford, when the edges are already available, is O(VE) time
# and O(V) auxiliary space. This matrix version first collects the existing
# edges from the matrix so that the relaxation loop can iterate over E real
# edges instead of scanning V^2 cells every round.
#
# Time Complexity: O(V^2 + VE + E) = O(V^2 + VE), worst O(V^3)
#   We scan the matrix once to collect edges: O(V^2).
#   Then we relax all edges V - 1 times: O(VE).
#   Then we scan all collected edges once more to detect a negative cycle: O(E).
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V + E)
#   distance stores at most V entries.
#   previous stores at most V entries.
#   edges stores at most E edge records.
#
# Total Space: O(V^2)
def bellman_ford_matrix(graph, start_key):
    if start_key not in graph.index_map:
        return {}, {}

    vertex_count = len(graph.vertices)
    distance = {}
    previous = {}

    for vertex in graph.vertices:
        distance[vertex.key] = inf
        previous[vertex.key] = None

    distance[start_key] = 0
    edges = []

    for from_index in range(vertex_count):
        for to_index in range(vertex_count):
            weight = graph.matrix[from_index][to_index]

            if weight is not None:
                from_key = graph.vertices[from_index].key
                to_key = graph.vertices[to_index].key
                edges.append((from_key, to_key, weight))

    for _ in range(vertex_count - 1):
        updated = False

        for from_key, to_key, weight in edges:
            if distance[from_key] == inf:
                continue

            new_distance = distance[from_key] + weight

            if new_distance < distance[to_key]:
                distance[to_key] = new_distance
                previous[to_key] = from_key
                updated = True

        if not updated:
            break

    for from_key, to_key, weight in edges:
        if distance[from_key] != inf and distance[from_key] + weight < distance[to_key]:
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
    graph = AdjacencyMatrixGraph(directed=True)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 5)
    graph.add_edge("B", "C", -2)
    graph.add_edge("C", "D", 3)

    distance, previous = bellman_ford_matrix(graph, "A")

    print(distance)
    print(build_path(previous, "A", "D"))
