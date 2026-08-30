class ArrayUnionFind:
    def __init__(self):
        self.items = []
        self.index_map = {}
        self.parent = []

    def make_set(self, item):
        if item in self.index_map:
            return

        index = len(self.items)
        self.items.append(item)
        self.index_map[item] = index

        # Negative number means this index is the root.
        # The absolute value is the size of this set.
        self.parent.append(-1)

    def find_index(self, index):
        if self.parent[index] < 0:
            return index

        self.parent[index] = self.find_index(self.parent[index])
        return self.parent[index]

    def find(self, item):
        index = self.index_map[item]
        root_index = self.find_index(index)
        return self.items[root_index]

    def union(self, item1, item2):
        root_index1 = self.find_index(self.index_map[item1])
        root_index2 = self.find_index(self.index_map[item2])

        if root_index1 == root_index2:
            return False

        # More negative means bigger set, for example -5 is bigger than -2.
        if self.parent[root_index1] > self.parent[root_index2]:
            root_index1, root_index2 = root_index2, root_index1

        self.parent[root_index1] += self.parent[root_index2]
        self.parent[root_index2] = root_index1
        return True

    def same_set(self, item1, item2):
        return self.find(item1) == self.find(item2)

    def size(self, item):
        root_index = self.find_index(self.index_map[item])
        return -self.parent[root_index]
