# Lecture-style disjoint set using set_array + map_array.
#
# Let N be the number of stored items.
# map_array[item] stores which set index the item belongs to.
# Dictionary map_array lookups are average O(1).
#
# Space Complexity: O(N)
# make_set: average O(1)
# find: average O(1)
# one union: O(size of smaller set), because those items move sets
# all successful unions: O(N log N), because smaller sets are moved into larger sets
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
