import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_list_map import MapGraph
from Stack.linked_stack import LinkedStack


# DFS modification with adjacency list
# Purpose: topological sort using DFS finish order.
# Requirement: graph must be a directed acyclic graph (DAG).
#
# Time Complexity: O(V + E)
#   Each vertex is visited once.
#   Each edge is checked once during DFS.
#
# Input Space: O(V + E)
#   The graph stores vertices and adjacency lists.
#
# Auxiliary Space: O(V)
#   state stores one mark per vertex.
#   recursion stack can contain at most V vertices.
#   topological_stack stores at most V vertex keys.
#   order stores the final topological order.
#
# Total Space: O(V + E)

#https://www.geeksforgeeks.org/dsa/topological-sort-using-dfs/
def dfs_topological_sort(graph):
    if not graph.directed:
        raise ValueError("DFS topological sort only works on directed graphs.")

    state = {}

    for key in graph.vertices:
        state[key] = "unvisited"

    topological_stack = LinkedStack()

    def dfs_visit(vertex):
        state[vertex.key] = "visiting"

        for edge in vertex.edges:
            neighbour = edge.to_vertex

            if state[neighbour.key] == "visiting":
                raise ValueError("Graph has a cycle. Topological sort is not possible.")

            if state[neighbour.key] == "unvisited":
                dfs_visit(neighbour)

        state[vertex.key] = "visited"
        topological_stack.push(vertex.key)

    for key in graph.vertices:
        if state[key] == "unvisited":
            dfs_visit(graph.vertices[key])

    order = []

    while not topological_stack.is_empty():
        order.append(topological_stack.pop())

    return order


if __name__ == "__main__":
    graph = MapGraph(directed=True)

    graph.add_edge("A", "C")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("B", "E")
    graph.add_edge("D", "F")
    graph.add_edge("E", "F")

    print(dfs_topological_sort(graph))
