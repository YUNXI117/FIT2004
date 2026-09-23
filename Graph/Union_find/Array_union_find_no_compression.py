"""Lecture05 parent-array Union-Find (about 44:00--61:00).

Unlike ArrayUnionFind, find_index only walks to the root: NO path compression.
parent[i] < 0: i is a root and -parent[i] is its component's size.
parent[i] >= 0: parent[i] is a parent INDEX, not an original graph vertex key.
The internal parent forest describes components; it is not the returned MST.

Let N be the number of items; log N means log(max(2, N)).
Assume average O(1) dictionary operations and O(1) array indexing:
* make_set: amortized O(1); a resizing insertion can individually cost O(N).
* find/find_index/same_set/size: O(log N) worst case, O(1) best case.
* union: two finds plus O(1) root linking, hence O(log N) worst case.
* N creations and M later operations: O(N + M log N) total.
* Stored space O(N); each find/union uses O(1) extra space (iterative).
The O(log N) height follows from union by size: a node's depth grows only
when its component joins one at least as large, doubling its component size.
Without path compression, do NOT claim O(alpha(N)) amortized operations.
Hash collisions can invalidate the O(1) dictionary assumption for item APIs;
the find_index bound itself uses only arrays and is a strict worst-case bound.
"""


class ArrayUnionFindNoCompression:
    def __init__(self):
        self.items = []
        self.index_map = {}
        self.parent = []

    def make_set(self, item):
        if item in self.index_map:
            return
        self.index_map[item] = len(self.items)
        self.items.append(item)
        self.parent.append(-1)

    def find_index(self, index):
        # Read parent links until a negative-size root; do not rewrite links.
        while self.parent[index] >= 0:
            index = self.parent[index]
        return index

    def find(self, item):
        return self.items[self.find_index(self.index_map[item])]

    def union(self, item1, item2):
        # FIT1008 ADT contract: callers pass items, not precomputed roots.
        # Therefore union must perform Find internally, even when a caller has
        # just used same_set and found the roots for the membership check.
        root1 = self.find_index(self.index_map[item1])
        root2 = self.find_index(self.index_map[item2])
        if root1 == root2:
            return False  # The proposed graph edge would form a cycle.

        # More negative means larger: attach the smaller ROOT to the larger.
        # Linking item1 to item2 instead of their roots can corrupt components.
        if self.parent[root1] > self.parent[root2]:
            root1, root2 = root2, root1
        self.parent[root1] += self.parent[root2]
        self.parent[root2] = root1
        return True

    def same_set(self, item1, item2):
        return self.find(item1) == self.find(item2)

    def size(self, item):
        return -self.parent[self.find_index(self.index_map[item])]
