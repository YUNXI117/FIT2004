from Graph.Adjacency_matrix import AdjacencyMatrixGraph
from Queue.linked_queue import LinkedQueue
# If we use adjacency matrix, then the time comp is O(V^2)

#Input space: O(V^2)
#Aux space: O(V)
#Total space: O(V^2)
def bfs_matrix(graph, start_key):
    if start_key not in graph.index_map:
        return []

    visited = set()
    queue = LinkedQueue()
    order = []

    start_index = graph.index_map[start_key]

    visited.add(start_key)
    queue.append(start_index)

    while not queue.is_empty():
        current_index = queue.serve()
        current_vertex = graph.vertices[current_index]
        order.append(current_vertex.key)

        for to_index in range(len(graph.vertices)):
            weight = graph.matrix[current_index][to_index]

            if weight is not None:
                neighbour = graph.vertices[to_index]
                #O(1), that's the reason why we use set
                if neighbour.key not in visited:
                    visited.add(neighbour.key)
                    queue.append(to_index)

    return order


# Shortest distance with BFS
# Only works for unweighted graphs, or graphs where every edge has the same cost.
#
# Time Complexity: O(V^2)
# Input Space: O(V^2)
# Auxiliary Space: O(V)
# Total Space: O(V^2)
def bfs_shortest_distance_matrix(graph, start_key):
    if start_key not in graph.index_map:
        return {}

    visited = set()
    queue = LinkedQueue()
    distance = {}

    start_index = graph.index_map[start_key]

    visited.add(start_key)
    distance[start_key] = 0
    queue.append(start_index)

    while not queue.is_empty():
        current_index = queue.serve()
        current_vertex = graph.vertices[current_index]

        for to_index in range(len(graph.vertices)):
            weight = graph.matrix[current_index][to_index]

            if weight is not None:
                neighbour = graph.vertices[to_index]

                if neighbour.key not in visited:
                    visited.add(neighbour.key)
                    distance[neighbour.key] = distance[current_vertex.key] + 1
                    queue.append(to_index)

    return distance


if __name__ == "__main__":
    graph = AdjacencyMatrixGraph(directed=False)

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    graph.add_edge("D", "F")

    print(bfs_matrix(graph, "A"))
    print(bfs_shortest_distance_matrix(graph, "A"))
