#Top-down(Recursion / Memoisation)
# -1 -> have not calculated
# infinity -> have calculated, bute the value compose cannot be use
# N: number of coin type
# M: target amount
# Time complexity: O(N * M)
# Auxiliary Space: O(M) for memo + O(M) for recursion stack = O(M)
# Input Space:O(N)
# Total Space: O(M+N)
def coin_change_top_down(
        coins: list[int],
        target: int
) -> int:
    """
    Return the minimum number of coins needed to make target exactly.
    Return -1 if the target cannot be formed.
    """

    # Create the memo array.
    # None means that the state has not been computed yet.
    memo: list[float | None] = [None] * (target + 1)

    # Base case: no coin is needed to make value 0.
    memo[0] = 0

    def solve(value: int) -> float:
        """
        Return the minimum number of coins needed to make value.
        """

        # Return the stored result if already computed.
        if memo[value] is not None:
            return memo[value]

        # Initially, assume that value cannot be formed.
        minimum_coins = float("inf")

        # Try every coin as the last selected coin.
        for coin in coins:
            if coin <= value:
                result = solve(value - coin)

                # Only use a reachable subproblem.
                if result != float("inf"):
                    candidate = result + 1

                    minimum_coins = min(
                        minimum_coins,
                        candidate
                    )

        # Store the result in the memo array.
        memo[value] = minimum_coins

        return minimum_coins

    # Start solving from the original target.
    answer = solve(target)

    if answer == float("inf"):
        return -1

    return int(answer)


# N:number of coins
# M: target
#Bottom-up(Iteration / Tabulation)
# Time Complexity :O(N*M)
# Input Space:O(N)
# Auxiliary Space:O(M) for dp
# Total Space: O(M+N)
def min_coins_bottom_up(
        coins: list[int],
        target: int
) -> int:
    """
    Return the minimum number of coins needed to make target exactly.
    Return -1 if the target cannot be formed.
    """

    if target < 0:
        return -1

    if any(coin <= 0 for coin in coins):
        raise ValueError("Coin values must be positive.")

    # Initially, every positive value is unreachable.
    dp = [float("inf")] * (target + 1)

    # Base case.
    dp[0] = 0

    # Compute the states from smaller values to larger values.
    for value in range(1, target + 1):

        # Try every coin as the last selected coin.
        for coin in coins:
            if coin <= value:
                previous = dp[value - coin]

                # Only use a reachable previous state.
                if previous != float("inf"):
                    candidate = previous + 1

                    dp[value] = min(
                        dp[value],
                        candidate
                    )

    # Check whether the target can be formed.
    if dp[target] == float("inf"):
        return -1

    return int(dp[target])

# Add the solution, so that we can not only know the number of the coin
# we used to compose the amount, also know which coin we use to
# compose the amount
#
#     Time Complexity:
#     DP computation: O(N * M)
#     Backtracking: O(K), where K <= M
#     Total: O(N * M + K) = O(N * M)
#
# Input Space:
# O(N) for the input coin list.
#
# Auxiliary Space:
# O(M) for dp and O(M) for last_coin.
# Therefore, total auxiliary space is O(M).
#
# Output Space:
# O(K) for selected_coins.
#
# Total Space:
# O(N + M + K) = O(N + M), since K <= M.
#
def coin_change_with_solution(coins, target):
    """
    Return the minimum number of coins and one optimal solution.
    Return (-1, []) if the target cannot be formed.
    """

    if target < 0:
        return -1, []

    if any(coin <= 0 for coin in coins):
        raise ValueError("Coin values must be positive.")

    # dp[value] stores the minimum number of coins.
    dp = [float("inf")] * (target + 1)

    # last_coin[value] stores the final coin in an optimal solution.
    last_coin = [None] * (target + 1)

    # Base case.
    dp[0] = 0

    # Fill the DP table from smaller values to larger values.
    for value in range(1, target + 1):
        for coin in coins:
            if (
                    coin <= value
                    and dp[value - coin] != float("inf")
            ):
                candidate = dp[value - coin] + 1

                # Record both the new optimal value
                # and the coin that produced it.
                if candidate < dp[value]:
                    dp[value] = candidate
                    last_coin[value] = coin

    # Check whether the target can be formed.
    if dp[target] == float("inf"):
        return -1, []

    # Reconstruct one optimal solution.
    selected_coins = []
    remaining = target

    while remaining > 0:
        coin = last_coin[remaining]

        selected_coins.append(coin)
        remaining = remaining - coin

    return int(dp[target]), selected_coins


# not use dynamic programming, use recurrence
# Time Complexity: O(N^M)
# Input Space: O(N)
# Auxiliary Space: O(M)
# Total Space: O(N + M)
def coin_change_recursive(
        coins: list[int],
        value: int
) -> float:
    """
    Return the minimum number of coins needed to make value exactly.
    Return infinity if the value cannot be formed.
    """

    # Base case.
    if value == 0:
        return 0

    minimum_coins = float("inf")

    # Try every possible final coin.
    for coin in coins:
        if coin <= value:
            result = coin_change_recursive(
                coins,
                value - coin
            )

            if result != float("inf"):
                candidate = result + 1
                minimum_coins = min(
                    minimum_coins,
                    candidate
                )

    return minimum_coins


def minimum_coins_brute_force(
        coins: list[int],
        target: int
) -> int:
    """
    Validate the input and return -1 if no solution exists.
    """

    if target < 0:
        return -1

    if any(coin <= 0 for coin in coins):
        raise ValueError("Coin values must be positive.")

    answer = coin_change_recursive(coins, target)

    if answer == float("inf"):
        return -1

    return int(answer)

# 有多少种combinator 组成目前的amount， 无顺序
def count_coin_combinations(
        coins: list[int],
        target: int
) -> int:
    """
    Return the number of different coin combinations
    that make the target value exactly.

    Different orders are treated as the same combination.

    Example:
        [1, 2] and [2, 1] are the same combination.

    Let:
        N = number of coin denominations
        M = target value

    Time Complexity: O(N * M)
    Input Space: O(N)
    Auxiliary Space: O(M)
    Output Space: O(1)
    Total Space: O(N + M)
    """

    if target < 0:
        return 0

    if any(coin <= 0 for coin in coins):
        raise ValueError("Coin values must be positive.")

    # dp[value] stores the number of combinations
    # that make 'value' exactly.
    #
    # Auxiliary space: O(M)
    dp = [0] * (target + 1)

    # There is one way to make value 0:
    # select no coins.
    dp[0] = 1

    # Process one coin denomination at a time.
    # Keeping coins in the outer loop prevents
    # different orders from being counted separately.
    for coin in coins:

        # Move forwards because each coin denomination
        # may be used an unlimited number of times.
        for value in range(coin, target + 1):

            # Add the current coin to every combination
            # that previously formed value - coin.
            dp[value] += dp[value - coin]

    return dp[target]


def count_ordered_coin_sequences(
        coins: list[int],
        target: int
) -> int:
    """
    Return the number of ordered coin sequences
    that make the target value exactly.

    Different orders are treated as different solutions.

    Example:
        [1, 2] and [2, 1] are different sequences.

    Let:
        N = number of coin denominations
        M = target value

    Time Complexity: O(N * M)
    Input Space: O(N)
    Auxiliary Space: O(M)
    Output Space: O(1)
    Total Space: O(N + M)
    """

    if target < 0:
        return 0

    if any(coin <= 0 for coin in coins):
        raise ValueError("Coin values must be positive.")

    # dp[value] stores the number of ordered sequences
    # that make 'value' exactly.
    #
    # Auxiliary space: O(M)
    dp = [0] * (target + 1)

    # There is one way to make value 0:
    # select no coins.
    dp[0] = 1

    # Compute the number of sequences for every value.
    for value in range(1, target + 1):

        # Try every coin as the last coin in the sequence.
        for coin in coins:
            if coin <= value:

                # Append the current coin to every sequence
                # that makes value - coin.
                dp[value] += dp[value - coin]

    return dp[target]























