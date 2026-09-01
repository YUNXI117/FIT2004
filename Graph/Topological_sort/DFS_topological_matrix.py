import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph


# DFS modification with adjacency matrix
# Purpose: topological sort using DFS finish order.
# Requirement: graph must be a directed acyclic graph (DAG).
#
# Time Complexity: O(V^2)
#   Each vertex is visited once.
#   For each vertex, DFS scans one full matrix row of length V.
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V)
#   state stores one mark per vertex.
#   recursion stack can contain at most V vertices.
#   order stores at most V vertex keys.
#
# Total Space: O(V^2)
def dfs_topological_sort_matrix(graph):
    if not graph.directed:
        raise ValueError("DFS topological sort only works on directed graphs.")

    vertex_count = len(graph.vertices)
    state = ["unvisited"] * vertex_count
    order = []

    def dfs_visit(index):
        state[index] = "visiting"

        for to_index in range(vertex_count):
            if graph.matrix[index][to_index] is None:
                continue

            if state[to_index] == "visiting":
                raise ValueError("Graph has a cycle. Topological sort is not possible.")

            if state[to_index] == "unvisited":
                dfs_visit(to_index)

        state[index] = "visited"
        order.append(graph.vertices[index].key)

    for index in range(vertex_count):
        if state[index] == "unvisited":
            dfs_visit(index)

    order.reverse()
    return order


if __name__ == "__main__":
    graph = AdjacencyMatrixGraph(directed=True)

    graph.add_edge("A", "C")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")
    graph.add_edge("B", "E")
    graph.add_edge("D", "F")
    graph.add_edge("E", "F")

    print(dfs_topological_sort_matrix(graph))
