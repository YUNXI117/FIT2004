import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph
from Stack.linked_stack import LinkedStack


# DFS with adjacency list
# Course note:
#   This iterative DFS uses a stack. Because a stack is last-in-first-out, we
#   push neighbours in reverse edge-list order so they are visited in the
#   original edge-list order.
#
# Time Complexity: O(V + E)
#   Each vertex is visited once: O(V)
#   Each edge is checked once or twice: O(E)
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   discovered stores at most V vertices.
#   visited stores at most V vertices.
#   stack stores at most V vertices.
#   order stores at most V vertices.
#
# Total Space: O(V + E)
def dfs(graph, start_key):
    if start_key not in graph.vertices:
        return []

    discovered = set()
    visited = set()
    stack = LinkedStack()
    order = []

    start_vertex = graph.vertices[start_key]
    discovered.add(start_key)
    stack.push(start_vertex)

    while not stack.is_empty():
        current_vertex = stack.pop()
        current_key = current_vertex.key

        discovered.discard(current_key)

        if current_key in visited:
            continue

        visited.add(current_key)
        order.append(current_key)

        for edge in reversed(current_vertex.edges):
            neighbour = edge.to_vertex

            if neighbour.key not in discovered and neighbour.key not in visited:
                discovered.add(neighbour.key)
                stack.push(neighbour)

    return order


if __name__ == "__main__":
    graph = MapGraph(directed=False)

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    graph.add_edge("D", "F")

    print(dfs(graph, "A"))
