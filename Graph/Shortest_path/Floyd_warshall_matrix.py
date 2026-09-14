from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph


# Floyd-Warshall with adjacency matrix
# Purpose: all-pairs shortest path.
# Requirement: graph can have negative edges, but must not have a negative cycle.
#
# Time Complexity: O(V^3)
#   We try every intermediate vertex between every pair of vertices.
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V^2)
#   distance stores all pairs of vertices.
#   next_index stores path reconstruction information for all pairs.
#
# Total Space: O(V^2)
def floyd_warshall_matrix(graph):
    vertex_count = len(graph.vertices)
    keys = []

    for vertex in graph.vertices:
        keys.append(vertex.key)

    distance = [[inf] * vertex_count for _ in range(vertex_count)]
    next_index = [[None] * vertex_count for _ in range(vertex_count)]

    for index in range(vertex_count):
        distance[index][index] = 0
        next_index[index][index] = index

    for from_index in range(vertex_count):
        for to_index in range(vertex_count):
            weight = graph.matrix[from_index][to_index]

            if weight is not None and weight < distance[from_index][to_index]:
                distance[from_index][to_index] = weight
                next_index[from_index][to_index] = to_index

    for middle in range(vertex_count):
        for from_index in range(vertex_count):
            for to_index in range(vertex_count):
                if distance[from_index][middle] == inf or distance[middle][to_index] == inf:
                    continue

                new_distance = distance[from_index][middle] + distance[middle][to_index]

                if new_distance < distance[from_index][to_index]:
                    distance[from_index][to_index] = new_distance
                    next_index[from_index][to_index] = next_index[from_index][middle]

    for index in range(vertex_count):
        if distance[index][index] < 0:
            raise ValueError("Graph contains a negative-weight cycle.")

    return build_distance_table(keys, distance), keys, next_index


def build_distance_table(keys, distance):
    distance_table = {}

    for from_index in range(len(keys)):
        from_key = keys[from_index]
        distance_table[from_key] = {}

        for to_index in range(len(keys)):
            to_key = keys[to_index]
            distance_table[from_key][to_key] = distance[from_index][to_index]

    return distance_table


def build_path(keys, next_index, start_key, target_key):
    if start_key not in keys or target_key not in keys:
        return []

    key_to_index = {}

    for index in range(len(keys)):
        key_to_index[keys[index]] = index

    start_index = key_to_index[start_key]
    target_index = key_to_index[target_key]

    if next_index[start_index][target_index] is None:
        return []

    path = [start_key]
    current_index = start_index

    while current_index != target_index:
        current_index = next_index[current_index][target_index]
        path.append(keys[current_index])

    return path


if __name__ == "__main__":
    graph = AdjacencyMatrixGraph(directed=True)

    graph.add_edge("A", "B", 3)
    graph.add_edge("A", "C", 8)
    graph.add_edge("B", "C", -2)
    graph.add_edge("C", "D", 1)
    graph.add_edge("A", "D", 10)

    distance, keys, next_index = floyd_warshall_matrix(graph)

    print(distance)
    print(build_path(keys, next_index, "A", "D"))
