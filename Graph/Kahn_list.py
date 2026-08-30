from Graph.Adjacency_list_map import MapGraph
from Queue.linked_queue import LinkedQueue


# Kahn's Algorithm with adjacency list
# Purpose: topological sort
# Requirement: graph must be a directed acyclic graph (DAG).
#
# Time Complexity: O(V + E)
#   We compute in-degree by checking every vertex and every edge.
#   Then each vertex enters the queue at most once.
#   Each edge is processed once when its from-vertex is served.
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   in_degree stores at most V entries.
#   queue stores at most V vertices.
#   order stores at most V vertex keys.
#
# Total Space: O(V + E)
def kahn_topological_sort(graph):
    if not graph.directed:
        raise ValueError("Kahn's algorithm only works on directed graphs.")

    in_degree = {}

    for key in graph.vertices:
        in_degree[key] = 0

    for key in graph.vertices:
        vertex = graph.vertices[key]

        for edge in vertex.edges:
            neighbour = edge.to_vertex
            in_degree[neighbour.key] += 1

    queue = LinkedQueue()

    for key in in_degree:
        if in_degree[key] == 0:
            queue.append(graph.vertices[key])

    order = []

    while not queue.is_empty():
        current_vertex = queue.serve()
        order.append(current_vertex.key)

        for edge in current_vertex.edges:
            neighbour = edge.to_vertex
            in_degree[neighbour.key] -= 1

            if in_degree[neighbour.key] == 0:
                queue.append(neighbour)

    if len(order) != len(graph.vertices):
        raise ValueError("Graph has a cycle. Topological sort is not possible.")

    return order


if __name__ == "__main__":
    graph = MapGraph(directed=True)

    graph.add_edge("A", "C")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("B", "E")
    graph.add_edge("D", "F")
    graph.add_edge("E", "F")

    print(kahn_topological_sort(graph))
