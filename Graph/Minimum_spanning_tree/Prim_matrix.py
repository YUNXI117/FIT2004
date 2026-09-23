from math import inf
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Graph.Representation.Adjacency_matrix import AdjacencyMatrixGraph


# Prim's Algorithm with adjacency matrix
# Representation/queue extension: the video (~15:18--21:20) explains the
# Dijkstra-like Prim update and heap bound; this file uses a linear minimum scan.
# Purpose: minimum spanning tree (MST)
# Requirement: graph must be connected and undirected.
# Negative/zero weights are valid. Membership in visited prevents cycles.
# min_weight[v] is the lightest single edge from the current tree to v,
# NOT the sum of a path from the start vertex. parent[v] records that edge.
# Picking the smallest candidate is a safe cut edge: selected edges remain
# contained in some MST. Equal-weight choices need not give the same MST.
#
# Time Complexity: O(V^2)
#   Assume average O(1) dictionary/set access and O(1) weight operations.
#   We repeat V times.
#   Each time, we scan all vertices to find the unvisited vertex with the
#   smallest edge weight connecting it to the current MST.
#   Then we scan one full matrix row to update candidate edges.
#
# Input Space: O(V^2)
#   The graph stores a V by V matrix.
#
# Auxiliary Space: O(V)
#   visited stores at most V vertex indexes.
#   min_weight stores one value per vertex.
#   parent stores one previous vertex index per vertex.
#   mst_edges stores V - 1 edges.
#
# Total Space: O(V^2)
# Input is unchanged; empty graph returns ([], 0). Disconnected/directed graphs
# raise ValueError; an unknown start_key raises KeyError.
def prim_mst_matrix(graph, start_key=None):
    if graph.directed:
        raise ValueError("Prim's algorithm only works on undirected graphs.")

    vertex_count = len(graph.vertices)

    if vertex_count == 0:
        return [], 0

    if start_key is None:
        start_key = graph.vertices[0].key

    if start_key not in graph.index_map:
        raise KeyError(start_key)

    visited = set()
    min_weight = [inf] * vertex_count
    parent = [None] * vertex_count
    mst_edges = []
    total_weight = 0

    start_index = graph.index_map[start_key]
    min_weight[start_index] = 0

    for _ in range(vertex_count):
        current_index = None
        current_min_weight = inf

        for index in range(vertex_count):
            if index not in visited and min_weight[index] < current_min_weight:
                current_index = index
                current_min_weight = min_weight[index]

        if current_index is None:
            break

        visited.add(current_index)

        if parent[current_index] is not None:
            from_vertex = graph.vertices[parent[current_index]]
            to_vertex = graph.vertices[current_index]
            mst_edges.append((from_vertex.key, to_vertex.key, min_weight[current_index]))
            total_weight += min_weight[current_index]

        for to_index in range(vertex_count):
            weight = graph.matrix[current_index][to_index]

            if weight is not None and to_index not in visited and weight < min_weight[to_index]:
                min_weight[to_index] = weight
                parent[to_index] = current_index

    if len(visited) != vertex_count:
        raise ValueError("Graph is disconnected. MST is not possible.")

    return mst_edges, total_weight


if __name__ == "__main__":
    graph = AdjacencyMatrixGraph(directed=False)

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "B", 1)
    graph.add_edge("B", "D", 5)
    graph.add_edge("C", "D", 8)
    graph.add_edge("D", "E", 2)
    graph.add_edge("D", "F", 6)
    graph.add_edge("E", "F", 3)

    mst_edges, total_weight = prim_mst_matrix(graph, "A")

    print(mst_edges)
    print(total_weight)
