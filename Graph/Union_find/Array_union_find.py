# Optimized extension of Lecture05's negative-size parent array.
# The video (~44:00--61:00) demonstrates root walking and union by size.
# This class additionally compresses paths; Array_union_find_no_compression.py
# keeps the demonstrated walk-only find and its O(log N) worst-case analysis.
# The component parent forest is NOT the MST: MST edges are stored separately.
#
# Let N be the number of stored items.
# parent[index] < 0 means the index is a root.
# abs(parent[index]) is the set size.
# Dictionary index_map lookups are average O(1); item-based bounds assume this.
# Path lengths below have a worst-case guarantee independent of hashing.
#
# Space Complexity: O(N)
# make_set: amortized O(1), assuming average O(1) dictionary operations;
#   a single insertion can take O(N) when a list/dictionary resizes.
# find_index: O(log N) single-call worst case, O(alpha(N)) amortized.
#   Union by size bounds tree height: whenever a node's depth increases,
#   its component size at least doubles, so this happens at most log2(N) times.
#   Path compression shortens paths further, but does not make every call O(1).
# find/union/same_set/size: O(log N) single-call worst case and O(alpha(N))
#   amortized, under the dictionary assumption. union includes two finds;
#   only linking the roots after finding them takes O(1).
# With N singleton creations and M subsequent operations, total work is
#   O(N + M alpha(N)) under these assumptions; alpha is inverse Ackermann.
# Amortized describes a bound over any operation sequence, not average inputs.
# Recursive find_index uses O(log N) stack space in the worst case.
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

        # Additional optimization: after finding the root, bypass ancestors.
        # This changes parent links, but not membership or the root's size.
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
