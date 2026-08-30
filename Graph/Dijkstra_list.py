from heapq import heappop, heappush
from itertools import count
from math import inf

from Graph.Adjacency_list_map import MapGraph


# Dijkstra with adjacency list
# Requirement: all edge weights must be non-negative.
#
# Time Complexity: O((V + E) log V) ~ O(E * log V)
#   Each vertex can be removed from the priority queue.
#   Each edge can cause a priority queue push.
#   Each priority queue operation costs O(log V).
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V + E)
#   distance stores at most V entries.
#   previous stores at most V entries.
#   visited stores at most V entries.
#   priority_queue can store extra entries when a vertex distance is improved.
#
# Total Space: O(V + E)
def dijkstra(graph, start_key):
    if start_key not in graph.vertices:
        return {}, {}

    distance = {}
    previous = {}

    for key in graph.vertices:
        distance[key] = inf
        previous[key] = None

    visited = set()
    priority_queue = []
    tie_breaker = count()

    start_vertex = graph.vertices[start_key]
    distance[start_key] = 0
    heappush(priority_queue, (0, next(tie_breaker), start_vertex))

    while len(priority_queue) > 0:
        current_distance, _, current_vertex = heappop(priority_queue)

        if current_vertex.key in visited:
            continue

        visited.add(current_vertex.key)

        for edge in current_vertex.edges:
            if edge.weight < 0:
                raise ValueError("Dijkstra cannot handle negative edge weights.")

            neighbour = edge.to_vertex

            if neighbour.key in visited:
                continue

            new_distance = current_distance + edge.weight

            if new_distance < distance[neighbour.key]:
                distance[neighbour.key] = new_distance
                previous[neighbour.key] = current_vertex.key
                heappush(priority_queue, (new_distance, next(tie_breaker), neighbour))

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

    distance, previous = dijkstra(graph, "A")

    print(distance)
    print(build_path(previous, "A", "F"))
