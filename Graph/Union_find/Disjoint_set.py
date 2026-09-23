# Additional implementation: dictionary parent + rank + path compression.
# Lecture05 explicitly demonstrates negative SIZE at parent-array roots;
# this rank-based implementation is an extension, not the same representation.
# Rank is a height bound, NOT component size or necessarily the current height
# after compression. Increase rank only when merging two equal-rank roots.
#
# Let N be the number of stored items.
# Dictionary lookups are average O(1).
#
# Space Complexity: O(N)
# make_set: amortized O(1) under the dictionary assumption; resizing can be O(N)
# find: O(alpha(N)) amortized, with path compression
# union: O(alpha(N)) amortized, with path compression + union by rank
# Single find/full union: O(log N) worst-case parent steps. Linking found roots
# alone is O(1). All these timings assume average O(1) dictionary operations.
# N creations + M later operations: O(N + M alpha(N)) under that assumption.
# alpha is inverse Ackermann; amortized bounds apply to any operation sequence,
# not merely random inputs. Recursive find has O(log N) worst-case stack depth.
class DisjointSet:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, item):
        if item in self.parent:
            return

        self.parent[item] = item
        self.rank[item] = 0

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])

        return self.parent[item]

    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 == root2:
            return False

        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

        return True
