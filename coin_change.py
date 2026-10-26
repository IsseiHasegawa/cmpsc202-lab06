"""Solve the coin change problem using naive recursion."""

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


if __name__ == "__main__":
    coins = [1, 2, 5]
    amount = 11

    start = perf_counter()
    result = coin_change_recursive(coins, amount)
    elapsed = perf_counter() - start

    print(f"Coins: {coins}")
    print(f"Amount: {amount}")
    print(f"Minimum number of coins: {result}")
    print(f"Execution time: {elapsed:.6f} seconds")
