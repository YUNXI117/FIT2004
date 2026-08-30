from Graph.Adjacency_matrix import AdjacencyMatrixGraph
from Queue.linked_queue import LinkedQueue


# Kahn's Algorithm with adjacency matrix
# Purpose: topological sort
# Requirement: graph must be a directed acyclic graph (DAG).
#
# Time Complexity: O(V^2)
#   We scan the whole V by V matrix to compute in-degree.
#   During the algorithm, each served vertex scans one full matrix row.
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V)
#   in_degree stores one number per vertex.
#   queue stores at most V vertex indexes.
#   order stores at most V vertex keys.
#
# Total Space: O(V^2)
def kahn_topological_sort_matrix(graph):
    if not graph.directed:
        raise ValueError("Kahn's algorithm only works on directed graphs.")

    vertex_count = len(graph.vertices)
    in_degree = [0] * vertex_count

    for from_index in range(vertex_count):
        for to_index in range(vertex_count):
            if graph.matrix[from_index][to_index] is not None:
                in_degree[to_index] += 1

    queue = LinkedQueue()

    for index in range(vertex_count):
        if in_degree[index] == 0:
            queue.append(index)

    order = []

    while not queue.is_empty():
        current_index = queue.serve()
        current_vertex = graph.vertices[current_index]
        order.append(current_vertex.key)

        for to_index in range(vertex_count):
            if graph.matrix[current_index][to_index] is not None:
                in_degree[to_index] -= 1

                if in_degree[to_index] == 0:
                    queue.append(to_index)

    if len(order) != vertex_count:
        raise ValueError("Graph has a cycle. Topological sort is not possible.")

    return order


if __name__ == "__main__":
    graph = AdjacencyMatrixGraph(directed=True)

    graph.add_edge("A", "C")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("B", "E")
    graph.add_edge("D", "F")
    graph.add_edge("E", "F")

    print(kahn_topological_sort_matrix(graph))
