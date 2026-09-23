"""Sort (weight, from_key, to_key) edges without comparing vertex labels.

The lecture suggests quicksort around 31:00. Its O(E log E) statement is an
average-case bound for ordinary quicksort, not a worst-case guarantee.
Kruskal requires ascending weights, not any particular sorting algorithm.
Counting sort needs a suitably small integer range K (O(E + K)); radix sort
needs a suitable digit representation (O(d(E + b))). Neither is a general
linear-time replacement for arbitrary comparable weights.
"""


def sort_edges(edges):
    """Default Python sort: O(E log E) worst-case time, O(E) extra space.

    Sorting compares only weights; distinct, non-orderable vertex keys work.
    Empty and singleton lists take O(1); comparisons are assumed O(1).
    """
    edges.sort(key=lambda edge: edge[0])


def quick_sort_edges(edges):
    """In-place teaching quicksort using a last-element pivot (Lomuto).

    Average O(E log E) for random distinct-key order; worst O(E^2), e.g.
    sorted, reverse-sorted or all-equal weights. This is not randomized.
    Only weights are compared. Tied edges need not retain their input order.
    Process the smaller partition now and defer the larger to keep the
    explicit stack O(log E), even when runtime is quadratic. No recursion.
    Pass sorter=quick_sort_edges to any Kruskal entry point to use it.
    """
    if len(edges) < 2:
        return
    pending = [(0, len(edges) - 1)]
    while pending:
        low, high = pending.pop()
        while low < high:
            pivot_weight = edges[high][0]
            split = low
            for index in range(low, high):
                if edges[index][0] < pivot_weight:
                    edges[split], edges[index] = edges[index], edges[split]
                    split += 1
            edges[split], edges[high] = edges[high], edges[split]

            # Only defer non-trivial ranges. Each nested smaller partition
            # is at most half the current range, bounding pending stack size.
            if split - low < high - split:
                if split + 1 < high:
                    pending.append((split + 1, high))
                high = split - 1
            else:
                if low < split - 1:
                    pending.append((low, split - 1))
                low = split + 1
