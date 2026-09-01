import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph
from Queue.linked_queue import LinkedQueue


# BFS with adjacency matrix
# Time Complexity: O(V^2)
#   Each vertex is visited once.
#   For each visited vertex, we scan one full matrix row of length V.
#   Therefore V rows * V columns = O(V^2).
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V)
#   discovered stores vertex indexes that are already in the queue.
#   visited stores vertex indexes that have already been served from the queue.
#   queue stores at most V vertex indexes.
#   order stores at most V vertex keys.
#
# Total Space: O(V^2)
def bfs_matrix(graph, start_key):
    if start_key not in graph.index_map:
        return []

    discovered = set()
    visited = set()
    queue = LinkedQueue()
    order = []

    start_index = graph.index_map[start_key]

    discovered.add(start_index)
    queue.append(start_index)

    while not queue.is_empty():
        current_index = queue.serve()
        current_vertex = graph.vertices[current_index]

        discovered.discard(current_index)

        if current_index in visited:
            continue

        visited.add(current_index)
        order.append(current_vertex.key)

        for to_index in range(len(graph.vertices)):
            weight = graph.matrix[current_index][to_index]

            if weight is not None and to_index not in discovered and to_index not in visited:
                discovered.add(to_index)
                queue.append(to_index)

    return order


# Shortest distance with BFS
# Only works for unweighted graphs, or graphs where every edge has the same cost.
#
# Time Complexity: O(V^2)
# Input Space: O(V^2)
# Auxiliary Space: O(V)
# Total Space: O(V^2)
def bfs_shortest_distance_matrix(graph, start_key):
    if start_key not in graph.index_map:
        return {}

    discovered = set()
    visited = set()
    queue = LinkedQueue()
    distance = {}

    start_index = graph.index_map[start_key]

    discovered.add(start_index)
    distance[start_key] = 0
    queue.append(start_index)

    while not queue.is_empty():
        current_index = queue.serve()
        current_vertex = graph.vertices[current_index]

        discovered.discard(current_index)

        if current_index in visited:
            continue

        visited.add(current_index)

        for to_index in range(len(graph.vertices)):
            weight = graph.matrix[current_index][to_index]

            if weight is not None:
                neighbour = graph.vertices[to_index]

                if to_index not in discovered and to_index not in visited:
                    discovered.add(to_index)
                    distance[neighbour.key] = distance[current_vertex.key] + 1
                    queue.append(to_index)

    return distance


if __name__ == "__main__":
    graph = AdjacencyMatrixGraph(directed=False)

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    graph.add_edge("D", "F")

    print(bfs_matrix(graph, "A"))
    print(bfs_shortest_distance_matrix(graph, "A"))
