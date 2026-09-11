# N: Quantity of different types' items
# M: The capacity of the backpack

# Time Complexity:O(N*M)
# Auxiliary Space:O(M)
def unbounded_knapsack(items, capacity):
    dp = [0] * (capacity + 1)

    for current_capacity in range(1, capacity + 1):
        dp[current_capacity] = dp[current_capacity - 1]

        for weight, profit in items:
            if weight <= current_capacity:
                dp[current_capacity] = max(
                    dp[current_capacity],
                    dp[current_capacity - weight] + profit
                )

    return dp[capacity]

# Time Complexity:O(N*M)
# Auxiliary Space:O(N*M)
def zero_one_knapsack(weights, values, capacity):
    n = len(weights)

    dp = [
        [0] * (capacity + 1)
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = values[i - 1]

        for current_capacity in range(capacity + 1):
            # Do not include item i.
            dp[i][current_capacity] = dp[i - 1][current_capacity]

            # Include item i.
            if weight <= current_capacity:
                dp[i][current_capacity] = max(
                    dp[i - 1][current_capacity],
                    value + dp[i - 1][current_capacity - weight]
                )

    return dp[n][capacity]

# Time Complexity:O(N*M)
# Auxiliary Space:O(M)
def zero_one_optimal_knapsack(
        items: list[tuple[int, int]],
        max_capacity: int
) -> int:
    """
    items 中每个元素为 (weight, value)
    max_capacity 是背包最大容量

    返回背包能够获得的最大总价值。
    """

    # dp[c] 表示容量不超过 c 时能够获得的最大价值
    dp = [0] * (max_capacity + 1)

    # 每次处理一件物品
    for weight, value in items:

        # 必须从大容量向小容量倒序更新
        for capacity in range(
                max_capacity,
                weight - 1,
                -1
        ):
            # 不选择当前物品：dp[capacity]
            do_not_take = dp[capacity]

            # 选择当前物品：
            # 当前物品价值 + 剩余容量原来的最优价值
            take = dp[capacity - weight] + value

            dp[capacity] = max(do_not_take, take)

    return dp[max_capacity]