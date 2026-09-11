def fibonacci_recursive(n: int) -> int:
    """
    Return the nth Fibonacci number using plain recursion.

    Time complexity: O(2^n)
    Auxiliary space: O(n)

    Recursive relation: F(n)=F(n−1)+F(n−2)
    """

    # Reject invalid input.
    if n < 0:
        raise ValueError("n must be non-negative")

    # Base cases:
    # F(0) = 0
    # F(1) = 1
    if n <= 1:
        return n

    # Recursively calculate the two previous Fibonacci numbers.
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_top_down(
        n: int,
        memo: list[int]
) -> int:
    """
    Return F(n) using recursion and memoisation.

    Time complexity: O(n)
    Auxiliary space: O(n){
        Memo array: (O(n))
        Recursion stack: (O(n))
        }
    """

    # Base cases.
    if n <= 1:
        return n

    # Return the saved answer if it already exists.
    if memo[n] != -1:
        return memo[n]

    # Calculate the answer and save it.
    memo[n] = (
            fibonacci_top_down(n - 1, memo)
            + fibonacci_top_down(n - 2, memo)
    )

    return memo[n]


def fibonacci_bottom_up(n: int) -> int:
    """
    Return the nth Fibonacci number using bottom-up dynamic programming.

    Time complexity: O(n)
    Auxiliary space: O(n)
    """

    # Reject invalid input.
    if n < 0:
        raise ValueError("n must be non-negative")

    # Handle F(0) separately.
    if n == 0:
        return 0

    # dp[i] stores the value of F(i).
    dp = [0] * (n + 1)

    # Base cases.
    dp[0] = 0
    dp[1] = 1

    # Calculate the Fibonacci numbers from smaller
    # subproblems to larger subproblems.
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

def fibonacci_optimised(n: int) -> int:
    """
    Return the nth Fibonacci number using constant auxiliary space.

    Time complexity: O(n)
    Auxiliary space: O(1)
    """

    # Reject invalid input.
    if n < 0:
        raise ValueError("n must be non-negative")

    # Base cases.
    if n <= 1:
        return n

    # previous stores F(i - 2).
    previous = 0

    # current stores F(i - 1).
    current = 1

    for i in range(2, n + 1):
        # Calculate F(i).
        next_value = previous + current

        # Move the two stored values one position forward.
        previous = current
        current = next_value

    return current





