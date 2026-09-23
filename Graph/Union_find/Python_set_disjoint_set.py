"""Concrete version of the Python-set option mentioned around 32:00--35:00.

The lecture mentions built-in sets, then illustrates a set/map table. It does
not specify this exact Python class. Here each component is a Python set and
map_array gives its slot directly; scanning all sets would NOT be O(1) find.
Small-to-large merging is essential to the total movement bound.

For N items, assume average O(1) dict/set access and unit-cost key operations:
* make_set: amortized O(1); find/same_set: average O(1).
* union: O(1 + min(a, b)) expected/amortized work for component sizes a, b;
  one merge may cost O(N). Same-component union is average O(1).
* All successful unions: O(N log N) total expected/amortized work. Every
  moved item joins a component at least twice as large, so moves O(log N) times.
* N creations + M union attempts: O(N + M + N log N) under these assumptions.
* Stored space O(N), including empty slots; O(N) peak extra space on resizing.
The movement count has a worst-case guarantee over any merge sequence;
hash-table timings additionally rely on average-case hashing assumptions.
"""


class PythonSetDisjointSet:
    def __init__(self):
        self.set_array = []
        self.map_array = {}

    def make_set(self, item):
        if item in self.map_array:
            return
        self.map_array[item] = len(self.set_array)
        self.set_array.append({item})

    def find(self, item):
        return self.map_array[item]

    def union(self, item1, item2):
        root1, root2 = self.find(item1), self.find(item2)
        if root1 == root2:
            return False
        if len(self.set_array[root1]) < len(self.set_array[root2]):
            root1, root2 = root2, root1

        # Mutate the larger set; constructing large | small each time would
        # repeatedly copy the larger component and spoil the movement bound.
        for item in self.set_array[root2]:
            self.set_array[root1].add(item)
            self.map_array[item] = root1
        self.set_array[root2].clear()
        return True

    def same_set(self, item1, item2):
        return self.find(item1) == self.find(item2)
