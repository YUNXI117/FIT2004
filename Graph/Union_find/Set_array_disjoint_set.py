class SetArrayDisjointSet:
    def __init__(self):
        self.set_array = []
        self.map_array = {}

    def make_set(self, item):
        if item in self.map_array:
            return

        set_index = len(self.set_array)
        self.set_array.append([item])
        self.map_array[item] = set_index

    def find(self, item):
        return self.map_array[item]

    def union(self, item1, item2):
        set_index1 = self.find(item1)
        set_index2 = self.find(item2)

        if set_index1 == set_index2:
            return False

        if len(self.set_array[set_index1]) < len(self.set_array[set_index2]):
            set_index1, set_index2 = set_index2, set_index1

        for item in self.set_array[set_index2]:
            self.set_array[set_index1].append(item)
            self.map_array[item] = set_index1

        self.set_array[set_index2] = []
        return True

    def same_set(self, item1, item2):
        return self.find(item1) == self.find(item2)
