from Graph.Adjacency_list_map import MapGraph
from Stack.linked_stack import LinkedStack


# DFS with adjacency list
# Time Complexity: O(V + E)
#   Each vertex is visited once: O(V)
#   Each edge is checked once or twice: O(E)
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   visited stores at most V vertices.
#   stack stores at most V vertices.
#   order stores at most V vertices.
#
# Total Space: O(V + E)
def dfs(graph, start_key):
    if start_key not in graph.vertices:
        return []

    visited = set()
    stack = LinkedStack()
    order = []

    start_vertex = graph.vertices[start_key]
    visited.add(start_key)
    stack.push(start_vertex)

    while not stack.is_empty():
        current_vertex = stack.pop()
        order.append(current_vertex.key)

        for edge in reversed(current_vertex.edges):
            neighbour = edge.to_vertex

            if neighbour.key not in visited:
                visited.add(neighbour.key)
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
