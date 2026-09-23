from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph


class MinHeap:
    def __init__(self):
        self.items = []        # stores [priority, index]
        self.index_map = {}    # vertex index -> heap index

    def is_empty(self):
        return len(self.items) == 0

    def contains(self, vertex_index):
        return vertex_index in self.index_map

    def insert(self, vertex_index, priority):
        if vertex_index in self.index_map:
            self.decrease_key(vertex_index, priority)
            return

        self.items.append([priority, vertex_index])
        self.index_map[vertex_index] = len(self.items) - 1
        self._rise(len(self.items) - 1)

    def decrease_key(self, vertex_index, new_priority):
        heap_index = self.index_map[vertex_index]

        if new_priority >= self.items[heap_index][0]:
            return

        self.items[heap_index][0] = new_priority
        self._rise(heap_index)

    def serve(self):
        if self.is_empty():
            raise IndexError("Cannot serve from an empty heap.")

        min_priority, min_vertex_index = self.items[0]
        last_item = self.items.pop()
        del self.index_map[min_vertex_index]

        if not self.is_empty():
            self.items[0] = last_item
            self.index_map[last_item[1]] = 0
            self._sink(0)

        return min_priority, min_vertex_index

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


# Dijkstra with adjacency matrix + custom min heap + decrease-key
# Requirement: all edge weights must be non-negative.
#
# Course note:
#   This is the matrix version of the FIT2004-style heap update approach.
#   Each vertex appears in the heap at most once, and index_map lets us update
#   its position after decrease_key/rise/sink operations.
#
# Time Complexity:
#   Full version: O(V^2 + V log V + E log V)
#   Simplified version: O(V^2 + E log V)
#   Matrix scanning:
#     Each finalized vertex scans one full matrix row: O(V).
#     In the code, this is the loop:
#       for to_index in range(vertex_count):
#           weight = graph.matrix[current_index][to_index]
#     It checks every possible destination column, including None entries.
#     At most V vertices are finalized, so matrix scanning costs O(V^2).
#   Heap operations:
#     Each vertex is inserted once and served once: O(V log V).
#     Each successful relaxation can call decrease_key: O(E log V).
#   Why simplified:
#     V log V is dominated by V^2, so the full version becomes
#     O(V^2 + E log V).
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V)
#   distance stores at most V entries.
#   previous stores at most V entries.
#   min_heap stores each vertex at most once.
#   min_heap.index_map stores at most V entries.
#
# Total Space: O(V^2)
def dijkstra_matrix_decrease_key(graph, start_key):
    if start_key not in graph.index_map:
        return {}, {}

    vertex_count = len(graph.vertices)
    distance = {}
    previous = {}
    min_heap = MinHeap()

    for index in range(vertex_count):
        key = graph.vertices[index].key
        distance[key] = inf
        previous[key] = None

    start_index = graph.index_map[start_key]
    distance[start_key] = 0

    for index in range(vertex_count):
        key = graph.vertices[index].key
        min_heap.insert(index, distance[key])

    while not min_heap.is_empty():
        current_distance, current_index = min_heap.serve()

        if current_distance == inf:
            break

        current_vertex = graph.vertices[current_index]

        for to_index in range(vertex_count):
            weight = graph.matrix[current_index][to_index]

            if weight is None:
                continue

            if weight < 0:
                raise ValueError("Dijkstra cannot handle negative edge weights.")

            if not min_heap.contains(to_index):
                continue

            neighbour = graph.vertices[to_index]
            new_distance = current_distance + weight

            if new_distance < distance[neighbour.key]:
                distance[neighbour.key] = new_distance
                previous[neighbour.key] = current_vertex.key
                min_heap.decrease_key(to_index, new_distance)

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

    distance, previous = dijkstra_matrix_decrease_key(graph, "A")

    print(distance)
    print(build_path(previous, "A", "F"))
