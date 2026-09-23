from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph


class MinHeap:
    """Vertex priority queue with one entry per key and an inverse index map.

    items[i] = [priority, vertex_key]; index_map[vertex_key] = i.
    Every swap must update both map entries or decrease_key targets a wrong item.
    Compare priorities only, so tied weights never require ordering vertex keys.
    Sifting traverses O(log V) levels; storage is O(V). Dictionary accesses use
    average O(1) costs, and Python list resizing uses amortized O(1) appends/pops.
    """
    def __init__(self):
        self.items = []
        self.index_map = {}

    def is_empty(self):
        return len(self.items) == 0

    def contains(self, key):
        return key in self.index_map

    def insert(self, key, priority):
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


# Prim's Algorithm with adjacency list + vertex priority queue
# Lecture05 ~15:18--21:20: reuse Dijkstra's queue/update structure, but use
# edge.weight, NOT distance[u] + edge.weight, as the candidate priority.
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
# Negative/zero weights are valid, even when the input contains negative cycles:
# only edges to unselected vertices are accepted, so the result stays acyclic.
#
# Time Complexity: O((V + E) log V), simplified to O(E log V) when connected.
# Bounds assume average O(1) dict access and O(1) weight comparisons/arithmetic.
# Heap sifting: O(log V) worst case; contains: average O(1).
# Insert/serve also use resizable lists: an individual resize can cost O(V),
# but all V insertions/deletions have O(V) total resizing work. Their standard
# O(log V) per-operation bounds use amortized array costs and average hashing.
# Initialization inserts V vertices individually: O(V log V); scans O(V + E).
#   This matches the course-notes version: each vertex is stored in the
#   priority queue with key min_weight[v].
#   Each vertex is served once: O(V log V).
#   Each successful edge relaxation can call decrease_key: O(E log V).
#   Heap holds one entry per unselected vertex, so its size is O(V), not O(E).
# Correctness invariant: selected edges extend to some MST. min_weight[v]
# is the cheapest edge from the selected tree to v; parent[v] realizes it.
# Serving the smallest key chooses a lightest edge across the current cut.
# Different tie choices can produce different trees with the same minimum sum.
# Input is not mutated; empty graph returns ([], 0); disconnected/directed
# graphs raise ValueError; an unknown start_key raises KeyError.
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   min_weight stores at most V values.
#   parent stores at most V previous vertices.
#   min_heap stores each unselected vertex at most once.
#   mst_edges stores V - 1 edges.
#
# Total Space: O(V + E)
def prim_mst(graph, start_key=None):
    if graph.directed:
        raise ValueError("Prim's algorithm only works on undirected graphs.")

    if len(graph.vertices) == 0:
        return [], 0

    if start_key is None:
        start_key = next(iter(graph.vertices))

    if start_key not in graph.vertices:
        raise KeyError(start_key)

    min_weight = {}
    # Absence means no chosen incoming edge; None itself can be a vertex key.
    parent = {}
    min_heap = MinHeap()
    mst_edges = []
    total_weight = 0

    for key in graph.vertices:
        min_weight[key] = inf

    min_weight[start_key] = 0

    for key in graph.vertices:
        min_heap.insert(key, min_weight[key])

    while not min_heap.is_empty():
        current_weight, current_key = min_heap.serve()

        if current_weight == inf:
            break

        if current_key in parent:
            mst_edges.append((parent[current_key], current_key, current_weight))
            total_weight += current_weight

        current_vertex = graph.vertices[current_key]

        for edge in current_vertex.edges:
            neighbour = edge.to_vertex

            if min_heap.contains(neighbour.key) and edge.weight < min_weight[neighbour.key]:
                # Prim uses this edge alone, not a source-to-neighbour path sum.
                min_weight[neighbour.key] = edge.weight
                parent[neighbour.key] = current_key
                min_heap.decrease_key(neighbour.key, edge.weight)

    if len(mst_edges) != len(graph.vertices) - 1:
        raise ValueError("Graph is disconnected. MST is not possible.")

    return mst_edges, total_weight


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

    mst_edges, total_weight = prim_mst(graph, "A")

    print(mst_edges)
    print(total_weight)
