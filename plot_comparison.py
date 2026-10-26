"""Plot the recorded report data; requires matplotlib.

Run with: uv run --python 3.14 --with matplotlib plot_comparison.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator


def main():
    """Create a log-scale runtime plot from the report's existing table."""
    directory = Path(__file__).resolve().parent
    rows = []
    for line in (directory / "empirical_comparison.md").read_text().splitlines():
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells[0].isdigit():
                rows.append([float(cell) for cell in cells])

    amounts = [row[0] for row in rows]
    fig, ax = plt.subplots(figsize=(9, 5.5), layout="constrained")
    series = [
        (2, "Naive recursive", "#b44722", "o"),
        (3, "Memoized", "#2463a6", "s"),
        (4, "Bottom-up DP", "#16806a", "^"),
    ]
    for column, label, color, marker in series:
        ax.plot(
            amounts, [row[column] for row in rows],
            label=label, color=color, marker=marker, linewidth=2, markersize=6,
        )

    ax.set_yscale("log")
    ax.set_xticks(amounts)
    ax.set_xlabel("Target amount")
    ax.set_ylabel("Median runtime per call (ms, logarithmic scale)")
    ax.set_title("Coin Change: Runtime Comparison\nCoins = [1, 2, 5]", pad=14)
    ax.yaxis.set_major_locator(LogLocator(base=10, numticks=9))
    ax.grid(axis="both", which="major", color="#dddddd", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", frameon=True)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(directory / "empirical_comparison.png", dpi=180)
    plt.close(fig)
    print("Created empirical_comparison.png from the report table.")


if __name__ == "__main__":
    main()
