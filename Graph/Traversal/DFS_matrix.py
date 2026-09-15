import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph
from Stack.linked_stack import LinkedStack


# DFS with adjacency matrix
# Course note:
#   This iterative DFS uses a stack. Because a stack is last-in-first-out, we
#   scan the matrix row from right to left so lower-index neighbours are popped
#   and visited first.
#
# Time Complexity: O(V^2)
#   Each vertex is visited once.
#   For each visited vertex, we scan one full matrix row of length V.
#   Therefore V rows * V columns = O(V^2).
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V)
#   discovered stores at most V vertex indexes.
#   visited stores at most V vertex indexes.
#   stack stores at most V vertex indexes.
#   order stores at most V vertex keys.
#
# Total Space: O(V^2)
def dfs_matrix(graph, start_key):
    if start_key not in graph.index_map:
        return []

    discovered = set()
    visited = set()
    stack = LinkedStack()
    order = []

    start_index = graph.index_map[start_key]
    discovered.add(start_index)
    stack.push(start_index)

    while not stack.is_empty():
        current_index = stack.pop()
        current_vertex = graph.vertices[current_index]

        discovered.discard(current_index)

        if current_index in visited:
            continue

        visited.add(current_index)
        order.append(current_vertex.key)

        for to_index in range(len(graph.vertices) - 1, -1, -1):
            weight = graph.matrix[current_index][to_index]

            if weight is not None and to_index not in discovered and to_index not in visited:
                discovered.add(to_index)
                stack.push(to_index)

    return order


if __name__ == "__main__":
    graph = AdjacencyMatrixGraph(directed=False)

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    graph.add_edge("D", "F")

    print(dfs_matrix(graph, "A"))
