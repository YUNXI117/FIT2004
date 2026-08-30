class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def append(self, data):
        new_node = LinkedListNode(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node

        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def __iter__(self):
        current = self.head

        while current is not None:
            yield current.data
            current = current.next

    def __len__(self):
        return self.size

class Vertex:
    def __init__(self, key):
        self.key = key
        self.edges = LinkedList()

    def add_edge(self, edge):
        self.edges.append(edge)

    def __str__(self):
        return str(self.key)

class Edge:
    def __init__(self, from_vertex, to_vertex, weight=1):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    def __str__(self):
        return f"{self.from_vertex} -> {self.to_vertex}({self.weight})"

class MapGraph:
    def __init__(self, directed = False):
        self.vertices = {}
        self.directed = directed

    def add_vertex(self, key):
        if key not in self.vertices:
            self.vertices[key] = Vertex(key)

    def get_vertex(self, key):
        return self.vertices.get(key)

    def add_edge(self, from_key, to_key, weight = 1):
        self.add_vertex(from_key)
        self.add_vertex(to_key)

        from_vertex = self.vertices[from_key]
        to_vertex = self.vertices[to_key]

        edge = Edge(from_vertex, to_vertex, weight)
        from_vertex.add_edge(edge)

        if not self.directed:
            reverse_edge = Edge(to_vertex, from_vertex, weight)
            to_vertex.add_edge(reverse_edge)

    def get_neighbours(self, key):
        vertex = self.get_vertex(key)

        if vertex is None:
            return []

        neighbours = []

        for edge in vertex.edges:
            neighbours.append(edge.to_vertex)

        return neighbours

    def print_graph(self):
        for key in self.vertices:
            vertex = self.vertices[key]

            print(f"{vertex}: ", end = "")

            for edge in vertex.edges:
                print(f"{edge.to_vertex}({edge.weight})", end = "")

            print()
