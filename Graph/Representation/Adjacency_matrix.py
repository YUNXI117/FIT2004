class Vertex:
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return str(self.key)


class Edge:
    def __init__(self, from_vertex, to_vertex, weight=1):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        return f"{self.from_vertex} -> {self.to_vertex} ({self.weight})"


class AdjacencyMatrixGraph:
    def __init__(self, directed=False):
        self.vertices = []          # index -> Vertex object
        self.index_map = {}         # key -> index
        self.matrix = []            # 2D matrix
        self.directed = directed

    def add_vertex(self, key):
        if key in self.index_map:
            return

        new_vertex = Vertex(key)
        self.vertices.append(new_vertex)
        self.index_map[key] = len(self.vertices) - 1

        for row in self.matrix:
            row.append(None)

        new_row = [None] * len(self.vertices)
        self.matrix.append(new_row)

    def add_edge(self, from_key, to_key, weight=1):
        self.add_vertex(from_key)
        self.add_vertex(to_key)

        from_index = self.index_map[from_key]
        to_index = self.index_map[to_key]

        self.matrix[from_index][to_index] = weight

        if not self.directed:
            self.matrix[to_index][from_index] = weight

    def remove_edge(self, from_key, to_key):
        if from_key not in self.index_map or to_key not in self.index_map:
            return

        from_index = self.index_map[from_key]
        to_index = self.index_map[to_key]

        self.matrix[from_index][to_index] = None

        if not self.directed:
            self.matrix[to_index][from_index] = None

    def has_edge(self, from_key, to_key):
        if from_key not in self.index_map or to_key not in self.index_map:
            return False

        from_index = self.index_map[from_key]
        to_index = self.index_map[to_key]

        return self.matrix[from_index][to_index] is not None

    def get_weight(self, from_key, to_key):
        if not self.has_edge(from_key, to_key):
            return None

        from_index = self.index_map[from_key]
        to_index = self.index_map[to_key]

        return self.matrix[from_index][to_index]

    def get_neighbours(self, key):
        if key not in self.index_map:
            return []

        neighbours = []
        vertex_index = self.index_map[key]

        for to_index in range(len(self.vertices)):
            weight = self.matrix[vertex_index][to_index]

            if weight is not None:
                neighbours.append(self.vertices[to_index])

        return neighbours

    def get_edges(self, key):
        if key not in self.index_map:
            return []

        edges = []
        from_index = self.index_map[key]
        from_vertex = self.vertices[from_index]

        for to_index in range(len(self.vertices)):
            weight = self.matrix[from_index][to_index]

            if weight is not None:
                to_vertex = self.vertices[to_index]
                edges.append(Edge(from_vertex, to_vertex, weight))

        return edges

    def print_matrix(self):
        print("   ", end="")

        for vertex in self.vertices:
            print(vertex, end="  ")

        print()

        for i in range(len(self.vertices)):
            print(self.vertices[i], end="  ")

            for j in range(len(self.vertices)):
                value = self.matrix[i][j]

                if value is None:
                    print(".", end="  ")
                else:
                    print(value, end="  ")

            print()