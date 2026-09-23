# Lecture05 set/map-table version (~36:00--44:00).
# set_array uses Python lists to enumerate component members (not Python sets).
# map_array uses a dictionary so vertex labels need not be consecutive integers.
# Python_set_disjoint_set.py implements the separately mentioned built-in-set option.
#
# Let N be the number of stored items.
# map_array[item] stores which set index the item belongs to.
# Dictionary map_array lookups are average O(1).
#
# Space Complexity: O(N)
# make_set: amortized O(1) assuming average O(1) dictionary operations
# find: average O(1)
# one union: moves min(a, b) items for different components of sizes a and b;
#   O(1 + min(a, b)) amortized work with average O(1) hashing/list appends.
#   A single union can cost O(N), including list resizing. Same-set: average O(1).
# all successful unions: O(N log N) total movement, NOT O(N) for every edge.
#   A moved item's component at least doubles, so it moves at most log2(N) times.
#   Equal-size repeated merges give the worst total movement order.
# N creations + M union attempts: O(N + M + N log N) under hashing assumptions.
#   This is an amortized sequence bound, not an average over merge sequences.
#   Without smaller-into-larger merging, total movement can instead be O(N^2).
# All component lists combined contain N items; empty slots are retained.
# Temporary list resizing can use O(N) space; total stored/peak space stays O(N).
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
            # Every moved vertex must point to its NEW component slot.
            self.set_array[set_index1].append(item)
            self.map_array[item] = set_index1

        self.set_array[set_index2] = []
        return True

    def same_set(self, item1, item2):
        return self.find(item1) == self.find(item2)
