# Empirical Comparison of Coin Change Algorithms

I compared naive recursion, top-down memoization, and bottom-up tabulation using coins `[1, 2, 5]` and amounts 5, 10, 15, 20, 25, and 30 on Python 3.15.1, macOS 26.6.2 (arm64). Run `python3 coin_change.py --compare` to repeat the experiment. For each approach and amount, `timeit.Timer.autorange()` selected a batch size taking at least 0.2 seconds; I then measured five batches and reported the median batch time divided by its call count, in milliseconds per call. Every memoized call received a new empty dictionary, and every bottom-up call built a new table. Timing included these initializations and the call wrapper but excluded validation and printing. All three approaches returned the same minimum coin counts before timing; exact timings can vary between runs.

| Amount | Minimum Coins | Naive Recursive (ms) | Memoized (ms) | Bottom-Up DP (ms) |
| --- | --- | --- | --- | --- |
| 5 | 1 | 0.001385 | 0.000822 | 0.000536 |
| 10 | 2 | 0.020644 | 0.001953 | 0.001117 |
| 15 | 3 | 0.295163 | 0.003045 | 0.001642 |
| 20 | 4 | 4.247945 | 0.004149 | 0.002220 |
| 25 | 5 | 61.558942 | 0.005238 | 0.002725 |
| 30 | 6 | 881.741375 | 0.006266 | 0.003239 |

Naive recursion became dramatically slower as the amount increased: its runtime grew from about 0.0014 ms at amount 5 to 882 ms at amount 30 because it repeatedly solves the same subproblems. Both DP approaches grew approximately linearly over these inputs, consistent with their O(kV) time complexity for k denominations and target amount V, compared with the exponential worst-case growth of naive recursion. Memoization stores subproblem results, while tabulation computes them iteratively. Bottom-up DP was faster than memoization at every measured amount in this run, consistent with avoiding recursive calls and dictionary lookups. The measurements cover small amounts and one coin set, so they demonstrate the trend rather than establish a universal speed ranking.
