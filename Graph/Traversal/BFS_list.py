import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph
from Queue.linked_queue import LinkedQueue


# BFS with adjacency list
# Time Complexity: O(V + E)
#   Each vertex is visited once: O(V)
#   Each edge is checked once or twice: O(E)
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   discovered stores vertices that are already in the queue.
#   visited stores vertices that have already been served from the queue.
#   queue stores at most V vertices.
#   order stores at most V vertices.
#
# Total Space: O(V + E)
def bfs(graph, start_key):
    if start_key not in graph.vertices:
        return []

    discovered = set()
    visited = set()
    queue = LinkedQueue()
    order = []

    start_vertex = graph.vertices[start_key]
    discovered.add(start_key)
    queue.append(start_vertex)
    while not queue.is_empty():
        current_vertex = queue.serve()
        current_key = current_vertex.key

        discovered.discard(current_key)

        if current_key in visited:
            continue

        visited.add(current_key)
        order.append(current_key)
        for edge in current_vertex.edges:
            neighbour = edge.to_vertex

            if neighbour.key not in discovered and neighbour.key not in visited:
                discovered.add(neighbour.key)
                queue.append(neighbour)

    return order


# Shortest distance with BFS
# Only works for unweighted graphs, or graphs where every edge has the same cost.
#
# Time Complexity: O(V + E)
# Input Space: O(V + E)
# Auxiliary Space: O(V)
# Total Space: O(V + E)
def bfs_shortest_distance(graph, start_key):
    if start_key not in graph.vertices:
        return {}

    discovered = set()
    visited = set()
    queue = LinkedQueue()
    distance = {}

    start_vertex = graph.vertices[start_key]
    discovered.add(start_key)
    distance[start_key] = 0
    queue.append(start_vertex)

    while not queue.is_empty():
        current_vertex = queue.serve()
        current_key = current_vertex.key

        discovered.discard(current_key)

        if current_key in visited:
            continue

        visited.add(current_key)

        for edge in current_vertex.edges:
            neighbour = edge.to_vertex

            if neighbour.key not in discovered and neighbour.key not in visited:
                discovered.add(neighbour.key)
                distance[neighbour.key] = distance[current_key] + 1
                queue.append(neighbour)

    return distance


if __name__ == "__main__":
    graph = MapGraph(directed=False)

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    graph.add_edge("D", "F")

    print(bfs(graph, "A"))
    print(bfs_shortest_distance(graph, "A"))
