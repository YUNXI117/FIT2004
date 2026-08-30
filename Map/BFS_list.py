from Map.Adjacency_list_map import MapGraph
from Queue.linked_queue import LinkedQueue
# If we use adjacency list, then the time comp is O(V+E)
#Space Complexity: O(V)
def bfs(graph, start_key):
    if start_key not in graph.vertices:
        return []

    visited = set()
    queue = LinkedQueue()
    order = []

    start_vertex = graph.vertices[start_key]
    visited.add(start_key)
    queue.append(start_vertex)
    #list: O(V)
    while not queue.is_empty():
        current_vertex = queue.serve()
        order.append(current_vertex.key)
        #list: O(X1 + X2 + ...) = O(E), where X is the number of edges which one vertex have
        for edge in current_vertex.edges:
            neighbour = edge.to_vertex

            if neighbour.key not in visited:
                visited.add(neighbour.key)
                queue.append(neighbour)

    return order


if __name__ == "__main__":
    graph = MapGraph(directed=False)

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")
    graph.add_edge("D", "F")

    print(bfs(graph, "A"))
