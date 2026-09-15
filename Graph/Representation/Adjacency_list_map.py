# Adjacency list graph implemented with a dictionary/map.
#
# V: number of vertices
# E: number of edges
# deg(u): number of outgoing edges from vertex u
#
# Space Complexity: O(V + E)
# add_vertex: average O(1), worst O(V) because dictionary operations can collide
# add_edge: average O(deg(from) + deg(to)) for undirected graphs, because this
#   implementation scans the edge list to update an existing edge instead of
#   storing duplicate edges. For directed graphs, it is O(deg(from)).
# get_vertex: average O(1)
# get_neighbours: O(deg(key))
# get_edges: average O(1), returns the stored edge list directly
# print_graph: O(V + E)

class Vertex:
    def __init__(self, key):
        self.key = key
        self.edges = []

    def add_edge(self, edge):
        for existing_edge in self.edges:
            if existing_edge.to_vertex is edge.to_vertex:
                existing_edge.weight = edge.weight
                return

        self.edges.append(edge)

    def __str__(self):
        return str(self.key)

class Edge:
    def __init__(self, from_vertex, to_vertex, weight=1):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        return f"{self.from_vertex} -> {self.to_vertex} {self.weight}"

class MapGraph:
    def __init__(self, directed = False):
        self.vertices = {}
        self.directed = directed

    def add_vertex(self, key):
        if key not in self.vertices:
            self.vertices[key] = Vertex(key)

    def add_edge(self, from_key, to_key, weight = 1):
        if weight is None:
            raise ValueError("Edge weight cannot be None.")

        self.add_vertex(from_key)
        self.add_vertex(to_key)

        from_vertex = self.vertices[from_key]
        to_vertex = self.vertices[to_key]

        edge = Edge(from_vertex, to_vertex, weight)
        from_vertex.add_edge(edge)

        if not self.directed:
            reverse_edge = Edge(to_vertex, from_vertex, weight)
            to_vertex.add_edge(reverse_edge)


    def get_vertex(self, key):
        return self.vertices.get(key)

    def get_neighbours(self, key):
        vertex = self.get_vertex(key)

        if vertex is None:
            return []

        neighbours = []

        for edge in vertex.edges:
            neighbours.append(edge.to_vertex)

        return neighbours

    def get_edges(self, key):
        vertex = self.get_vertex(key)

        if vertex is None:
            return []

        return vertex.edges

    def print_graph(self):
        for key in self.vertices:
            vertex = self.vertices[key]
            print(f"{vertex}: ", end="")

            for edge in vertex.edges:
                print(f"{edge.to_vertex}({edge.weight})", end="")

            print()




