from Graph.Adjacency_matrix import AdjacencyMatrixGraph
from Stack.linked_stack import LinkedStack


# DFS with adjacency matrix
# Time Complexity: O(V^2)
#   Each vertex is visited once.
#   For each visited vertex, we scan one full matrix row of length V.
#   Therefore V rows * V columns = O(V^2).
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V)
#   visited stores at most V vertex indexes.
#   stack stores at most V vertex indexes.
#   order stores at most V vertex keys.
#
# Total Space: O(V^2)
def dfs_matrix(graph, start_key):
    if start_key not in graph.index_map:
        return []

    visited = set()
    stack = LinkedStack()
    order = []

    start_index = graph.index_map[start_key]
    visited.add(start_index)
    stack.push(start_index)

    while not stack.is_empty():
        current_index = stack.pop()
        current_vertex = graph.vertices[current_index]
        order.append(current_vertex.key)

        for to_index in range(len(graph.vertices) - 1, -1, -1):
            weight = graph.matrix[current_index][to_index]

            if weight is not None and to_index not in visited:
                visited.add(to_index)
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
