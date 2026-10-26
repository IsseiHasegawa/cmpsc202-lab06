"""Solve coin change using naive recursion, memoization, and tabulation."""

from time import perf_counter


def coin_change_recursive(coins, amount):
    """Return the minimum coin count, or infinity if exact change is impossible.

    Coins must be positive integers, and amount must be a nonnegative integer.
    Each denomination can be used any number of times.
    """
    if amount == 0:
        return 0

    minimum_coins = float("inf")
    for coin in coins:
        if coin <= amount:
            candidate = 1 + coin_change_recursive(coins, amount - coin)
            minimum_coins = min(minimum_coins, candidate)

    return minimum_coins


def coin_change_memoized(coins, amount, memo):
    """Return the minimum coin count using cached results for each amount.

    Coins must be positive integers, and amount must be a nonnegative integer.
    Each denomination can be used any number of times. Impossible amounts are
    cached as infinity. Use a fresh memo dictionary for a different coin set.
    """
    if amount == 0:
        return 0
    if amount in memo:
        return memo[amount]

    minimum_coins = float("inf")
    for coin in coins:
        if coin <= amount:
            candidate = 1 + coin_change_memoized(coins, amount - coin, memo)
            minimum_coins = min(minimum_coins, candidate)

    memo[amount] = minimum_coins
    return minimum_coins


def coin_change_dp(coins, amount):
    """Return the minimum coin count using bottom-up dynamic programming.

    Coins must be positive integers, and amount must be a nonnegative integer.
    Each denomination can be used any number of times. Return infinity if
    exact change is impossible.
    """
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount]


if __name__ == "__main__":
    coins = [1, 2, 5]
    amount = 11

    start = perf_counter()
    result = coin_change_recursive(coins, amount)
    elapsed = perf_counter() - start

    print(f"Coins: {coins}")
    print(f"Amount: {amount}")
    print(f"Naive recursive minimum number of coins: {result}")
    print(f"Naive recursive execution time: {elapsed:.6f} seconds")

    memo = {}
    start = perf_counter()
    result = coin_change_memoized(coins, amount, memo)
    elapsed = perf_counter() - start

    print(f"Memoized minimum number of coins: {result}")
    print(f"Memoized execution time: {elapsed:.6f} seconds")

    start = perf_counter()
    result = coin_change_dp(coins, amount)
    elapsed = perf_counter() - start

    print(f"Bottom-up DP minimum number of coins: {result}")
    print(f"Bottom-up DP execution time: {elapsed:.6f} seconds")
