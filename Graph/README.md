# Graph Algorithms Map

Use this folder by problem type, not by algorithm name.

## Representation

Graph storage:
- `Representation/Adjacency_list_map.py`: adjacency list with dictionary mapping keys to vertices.
- `Representation/Adjacency_linked_list.py`: adjacency list where each vertex stores edges in a linked list.
- `Representation/Adjacency_matrix.py`: adjacency matrix.

Edge contract:
- These classes store at most one edge per ordered pair in a directed graph, or one logical edge per vertex pair in an undirected graph.
- Calling `add_edge` again updates that edge to the new weight. In an undirected graph, adding the reverse direction updates the same logical edge.
- A self-loop is stored once. `None` is reserved to mean "no edge" and is not a valid edge weight.

Complexity:
- Adjacency list space: `O(V + E)`.
- Adjacency matrix space: `O(V^2)`.

## Traversal

Purpose: visit reachable vertices.

- `Traversal/BFS_list.py`: BFS with adjacency list, time `O(V + E)`, auxiliary space `O(V)`.
- `Traversal/BFS_matrix.py`: BFS with adjacency matrix, time `O(V^2)`, auxiliary space `O(V)`.
- `Traversal/DFS_list.py`: DFS with adjacency list, time `O(V + E)`, auxiliary space `O(V)`.
- `Traversal/DFS_matrix.py`: DFS with adjacency matrix, time `O(V^2)`, auxiliary space `O(V)`.

Key idea:
- `discovered`: already in queue or stack.
- `visited`: already removed from queue or stack and processed.

## Topological Sort

Purpose: order tasks with prerequisites.

Requirement:
- Directed acyclic graph, also called a DAG.

Files:
- `Topological_sort/Kahn_list.py`: Kahn's algorithm with adjacency list, time `O(V + E)`.
- `Topological_sort/Kahn_matrix.py`: Kahn's algorithm with adjacency matrix, time `O(V^2)`.
- `Topological_sort/DFS_topological_list.py`: DFS topological sort with adjacency list, time `O(V + E)`.
- `Topological_sort/DFS_topological_matrix.py`: DFS topological sort with adjacency matrix, time `O(V^2)`.

## Shortest Path

Purpose: find minimum distance paths.

- BFS shortest distance: unweighted graph only.
- Dijkstra: single-source shortest path, no negative edge.
- Bellman-Ford: single-source shortest path, allows negative edges, detects negative cycles.
- Floyd-Warshall: all-pairs shortest path, allows negative edges, detects negative cycles.

Files:
- `Shortest_path/Dijkstra_list_linear.py`: Dijkstra with adjacency list and linear search, time `O(V^2 + E)`, usually `O(V^2)`.
- `Shortest_path/Dijkstra_list.py`: Dijkstra with adjacency list and built-in priority queue, allows duplicate heap entries, time `O((V + E) log V)`.
- `Shortest_path/Dijkstra_list_decrease_key.py`: Dijkstra with adjacency list and custom min heap with `decrease_key`, time `O((V + E) log V)`.
- `Shortest_path/Dijkstra_matrix.py`: Dijkstra with adjacency matrix and linear search, time `O(V^2)`.
- `Shortest_path/Dijkstra_matrix_heap.py`: Dijkstra with adjacency matrix and built-in priority queue, time `O(V^2 + E log V)`.
- `Shortest_path/Bellman_ford_list.py`: time `O(VE)`.
- `Shortest_path/Bellman_ford_matrix.py`: time `O(V^2 + VE)`, worst `O(V^3)`.
- `Shortest_path/Floyd_warshall_list.py`: time `O(V^3 + E)`.
- `Shortest_path/Floyd_warshall_matrix.py`: time `O(V^3)`.

Dijkstra mind map:
- Problem: shortest paths from one start vertex to all other vertices.
- Requirement: edge weights must be non-negative.
- Core tables: `distance` records the best known distance, `previous` records the path, `visited` records finalized vertices.
- Linear-search version: repeatedly scan all unvisited vertices to find the smallest `distance`, time `O(V^2 + E)`.
- Built-in priority-queue version: use `heapq`, insert duplicate entries when a distance improves, and ignore old entries after serving.
- Decrease-key priority-queue version: use a custom min heap plus `index_map`, update the existing heap entry when a distance improves.
- Matrix linear-search version: scan all vertices to choose the next vertex, then scan a full row for neighbours, time `O(V^2)`.
- Matrix heap version: scan matrix rows plus heap updates, time `O(V^2 + E log V)`. For dense graphs, this is often simplified to `O(E log V)`.

## Minimum Spanning Tree

Purpose: connect all vertices with minimum total weight.

Requirement:
- Connected, undirected, weighted graph.

Files:
- `Minimum_spanning_tree/Prim_list.py`: Prim with adjacency list and priority queue, time `O(E log E)`.
- `Minimum_spanning_tree/Prim_matrix.py`: Prim with adjacency matrix, time `O(V^2)`.
- `Minimum_spanning_tree/Kruskal_list.py`: Kruskal with standard disjoint set, time `O(E log E)`.
- `Minimum_spanning_tree/Kruskal_matrix.py`: Kruskal with matrix, time `O(V^2 + E log E)`.
- `Minimum_spanning_tree/Kruskal_set_array_list.py`: Kruskal with set-array disjoint set.
- `Minimum_spanning_tree/Kruskal_set_array_matrix.py`: Kruskal with set-array disjoint set.
- `Minimum_spanning_tree/Kruskal_union_find_list.py`: Kruskal with array-based union-find.
- `Minimum_spanning_tree/Kruskal_union_find_matrix.py`: Kruskal with array-based union-find.

Recommended implementations:
- For a sparse graph or the lecture's Kruskal method, use `Kruskal_union_find_list.py`. It uses the lecture-style negative-size parent array, union by size, and path compression.
- For a dense graph already stored as a matrix, use `Prim_matrix.py`, which runs in `O(V^2)` time without sorting all edges.
- The set-array Kruskal files are retained as teaching versions. Moving the smaller set gives `O(V log V)` total movement across successful unions, but the array union-find is the preferred general implementation.

## Union Find

Purpose: track connected components and detect cycles.

Files:
- `Union_find/Disjoint_set.py`: dictionary parent + rank.
- `Union_find/Set_array_disjoint_set.py`: lecture-style set array + map array.
- `Union_find/Array_union_find.py`: parent array with negative size at roots.
