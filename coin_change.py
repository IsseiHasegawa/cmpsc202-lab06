"""Solve coin change using naive recursion, memoization, and tabulation."""

import argparse
import platform
from statistics import median
from time import perf_counter
from timeit import Timer


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


def run_comparison():
    """Print median per-call timings from five calibrated timing batches."""
    coins = [1, 2, 5]
    amounts = [5, 10, 15, 20, 25, 30]

    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Coins: {coins}")
    print("Each timing is the median of five batches, in milliseconds per call.")
    print("Batch sizes are calibrated by timeit.Timer.autorange().")
    print("Every memoized call starts with an empty dictionary.")
    print()
    print("| Amount | Minimum Coins | Naive Recursive (ms) | Memoized (ms) | Bottom-Up DP (ms) |")
    print("| --- | --- | --- | --- | --- |")

    for amount in amounts:
        operations = (
            lambda: coin_change_recursive(coins, amount),
            lambda: coin_change_memoized(coins, amount, {}),
            lambda: coin_change_dp(coins, amount),
        )
        # Validate results outside the timed batches.
        results = [operation() for operation in operations]
        if len(set(results)) != 1:
            raise AssertionError(f"Results disagree for amount {amount}: {results}")

        timings = []
        for operation in operations:
            timer = Timer(operation)
            number, _ = timer.autorange()
            batches = timer.repeat(repeat=5, number=number)
            timings.append(median(batches) / number * 1000)

        recursive_ms, memoized_ms, dp_ms = timings
        print(
            f"| {amount} | {results[0]} | {recursive_ms:.6f} | "
            f"{memoized_ms:.6f} | {dp_ms:.6f} |"
        )


def run_demo():
    """Show the result and runtime of each approach on the assignment example."""
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compare", action="store_true", help="benchmark all three approaches"
    )
    args = parser.parse_args()
    if args.compare:
        run_comparison()
    else:
        run_demo()
