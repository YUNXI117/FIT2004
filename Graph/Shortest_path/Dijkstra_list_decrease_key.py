from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph


class MinHeap:
    def __init__(self):
        self.items = []        # stores [priority, key]
        self.index_map = {}    # key -> index in self.items

    def is_empty(self):
        return len(self.items) == 0

    def contains(self, key):
        return key in self.index_map

    def insert(self, key, priority):
        if key in self.index_map:
            self.decrease_key(key, priority)
            return

        self.items.append([priority, key])
        self.index_map[key] = len(self.items) - 1
        self._rise(len(self.items) - 1)

    def decrease_key(self, key, new_priority):
        index = self.index_map[key]

        if new_priority >= self.items[index][0]:
            return

        self.items[index][0] = new_priority
        self._rise(index)

    def serve(self):
        if self.is_empty():
            raise IndexError("Cannot serve from an empty heap.")

        min_priority, min_key = self.items[0]
        last_item = self.items.pop()
        del self.index_map[min_key]

        if not self.is_empty():
            self.items[0] = last_item
            self.index_map[last_item[1]] = 0
            self._sink(0)

        return min_priority, min_key

    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return index * 2 + 1

    def _right_child(self, index):
        return index * 2 + 2

    def _is_smaller(self, first_index, second_index):
        return self.items[first_index][0] < self.items[second_index][0]

    def _swap(self, first_index, second_index):
        self.items[first_index], self.items[second_index] = (
            self.items[second_index],
            self.items[first_index],
        )

        self.index_map[self.items[first_index][1]] = first_index
        self.index_map[self.items[second_index][1]] = second_index

    def _rise(self, index):
        while index > 0:
            parent_index = self._parent(index)

            if not self._is_smaller(index, parent_index):
                break

            self._swap(index, parent_index)
            index = parent_index

    def _sink(self, index):
        while self._left_child(index) < len(self.items):
            left_index = self._left_child(index)
            right_index = self._right_child(index)
            smaller_child_index = left_index

            if right_index < len(self.items) and self._is_smaller(right_index, left_index):
                smaller_child_index = right_index

            if not self._is_smaller(smaller_child_index, index):
                break

            self._swap(index, smaller_child_index)
            index = smaller_child_index


# Dijkstra with adjacency list + custom min heap + decrease-key
# Requirement: all edge weights must be non-negative.
#
# Course note:
#   This is the preferred FIT2004-style heap approach: each vertex appears in
#   the heap at most once, and index_map lets us update its position after
#   decrease_key/rise/sink operations.
#
# Main idea:
#   distance[key] stores the best distance found so far from start_key to key.
#   previous[key] stores the vertex before key on the shortest path.
#   A vertex is finalized once it has been served from min_heap.
#   min_heap starts with every vertex, keyed by its current distance estimate.
#   min_heap.index_map tells us where each vertex is inside the heap array.
#
# Time Complexity: O((V + E) log V)
#   Each vertex is inserted into the heap once: O(V log V).
#   Each vertex is served from the heap at most once: O(V log V).
#   Each successful relaxation can call decrease_key: O(E log V).
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   distance stores at most V entries.
#   previous stores at most V entries.
#   min_heap stores each vertex at most once.
#   min_heap.index_map stores at most V entries.
#
# Total Space: O(V + E)
def dijkstra_decrease_key(graph, start_key):
    if start_key not in graph.vertices:
        return {}, {}

    distance = {}
    previous = {}

    for key in graph.vertices:
        distance[key] = inf
        previous[key] = None

    min_heap = MinHeap()

    distance[start_key] = 0

    for key in graph.vertices:
        min_heap.insert(key, distance[key])

    while not min_heap.is_empty():
        current_distance, current_key = min_heap.serve()

        if current_distance == inf:
            break

        current_vertex = graph.vertices[current_key]

        for edge in current_vertex.edges:
            if edge.weight < 0:
                raise ValueError("Dijkstra cannot handle negative edge weights.")

            neighbour = edge.to_vertex

            if not min_heap.contains(neighbour.key):
                continue

            new_distance = current_distance + edge.weight

            if new_distance < distance[neighbour.key]:
                distance[neighbour.key] = new_distance
                previous[neighbour.key] = current_key
                min_heap.decrease_key(neighbour.key, new_distance)

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

    distance, previous = dijkstra_decrease_key(graph, "A")

    print(distance)
    print(build_path(previous, "A", "F"))
