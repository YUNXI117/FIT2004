class Vertex:
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return str(self.key)

class Edge:
    def __init__(self, from_vertex, to_vertex, weight = 1):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        return f"{self.from_vertex} -> {self.to_vertex} ({self.weight})"

class AdjacencyMatrixGraph:
    def __init__(self, directed = False):
        self.vertices = []  # index -> Vertex object
        self.index_map = {} # key -> index
        self.matrix = [] # 2D matrix
        self.directed = directed

    def add_vertex(self, key):
        if key in self.index_map:
            return


