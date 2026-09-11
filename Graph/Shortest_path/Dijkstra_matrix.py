from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph


# Dijkstra with adjacency matrix + linear search
# Requirement: all edge weights must be non-negative.
#
# This file is the matrix-specific version without a heap.
# It finds the next vertex by scanning all vertices, then scans one full matrix
# row to relax neighbours. Because it does not use heap operations, there is
# no extra log V factor.
#
# If you take the adjacency-list heap version and change the graph storage to
# an adjacency matrix, the time is O(V^2 + E log V): scanning matrix rows costs
# O(V^2), and heap operations cost O(E log V).
#
# Time Complexity: O(V^2)
#   We repeat V times.
#   Each time, we scan all vertices to find the unvisited vertex with the
#   smallest known distance: O(V).
#   Then we scan one full matrix row to relax neighbours: O(V).
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V)
#   distance stores at most V entries.
#   previous stores at most V entries.
#   visited stores at most V entries.
#
# Total Space: O(V^2)
def dijkstra_matrix(graph, start_key):
    if start_key not in graph.index_map:
        return {}, {}

    distance = {}
    previous = {}

    for vertex in graph.vertices:
        distance[vertex.key] = inf
        previous[vertex.key] = None

    visited = set()
    distance[start_key] = 0

    for _ in range(len(graph.vertices)):
        current_index = None
        current_distance = inf

        for index in range(len(graph.vertices)):
            vertex = graph.vertices[index]

            if vertex.key not in visited and distance[vertex.key] < current_distance:
                current_index = index
                current_distance = distance[vertex.key]

        if current_index is None:
            break

        current_vertex = graph.vertices[current_index]
        visited.add(current_vertex.key)

        for to_index in range(len(graph.vertices)):
            weight = graph.matrix[current_index][to_index]

            if weight is None:
                continue

            if weight < 0:
                raise ValueError("Dijkstra cannot handle negative edge weights.")

            neighbour = graph.vertices[to_index]

            if neighbour.key in visited:
                continue

            new_distance = distance[current_vertex.key] + weight

            if new_distance < distance[neighbour.key]:
                distance[neighbour.key] = new_distance
                previous[neighbour.key] = current_vertex.key

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

    distance, previous = dijkstra_matrix(graph, "A")

    print(distance)
    print(build_path(previous, "A", "F"))
