# -*- coding: utf-8 -*-
"""
Run many DayanDivination simulations and count occurrences of each original hexagram.
Usage:
    python test_hexagram_counts.py --trials 10000
Optional:
    --seed N    # set random seed for reproducibility
"""
import argparse
from collections import Counter
from dayan_divination import DayanDivination

# optional plotting
try:
    import matplotlib.pyplot as plt
    _HAS_MATPLOTLIB = True
except Exception:
    _HAS_MATPLOTLIB = False

def main():
    parser = argparse.ArgumentParser(description="Count original hexagrams from many DayanDivination runs")
    parser.add_argument("--trials", type=int, default=100000, help="number of simulations to run")
    parser.add_argument("--seed", type=int, default=None, help="optional random seed")
    args = parser.parse_args()

    if args.seed is not None:
        import random
        random.seed(args.seed)

    sim = DayanDivination(verbose=False)
    counter = Counter()

    for i in range(args.trials):
        res = sim.run()
        key = res.get('original_binary')
        counter[key] += 1

    total = sum(counter.values())

    print(f"Total trials: {total}")
    print(f"Unique original hexagrams: {len(counter)}\n")

    # Sort by count desc
    for k, v in counter.most_common():
        pct = v / total * 100
        print(f"{k}: {v} ({pct:.2f}%)")

    # Plot bar graph if matplotlib is available, otherwise show a simple ASCII bar chart
    labels, values = zip(*counter.most_common()) if counter else ([], [])

    if _HAS_MATPLOTLIB and values:
        try:
            x = range(len(labels))
            plt.figure(figsize=(12, 6))
            plt.bar(x, values, color='tab:blue')
            plt.xticks(x, labels, rotation=90, fontsize=8)
            plt.ylabel('Counts')
            plt.title('Original Hexagram Counts')
            plt.tight_layout()
            out_path = 'hexagram_counts.png'
            plt.savefig(out_path)
            print(f"Saved bar graph to {out_path}")
            try:
                plt.show()
            except Exception:
                # In some headless environments, show() may fail; that's okay.
                pass
        except Exception as e:
            print(f"Failed to create matplotlib plot: {e}")
    else:
        # ASCII fallback
        if not _HAS_MATPLOTLIB:
            print('\nmatplotlib not available — showing ASCII bar chart instead. Install with: pip install matplotlib')
        print('\nTop hexagram counts (ASCII bar chart):')
        max_label = max((len(l) for l in labels), default=0)
        max_value = max(values) if values else 0
        scale = max(1, max_value // 50)
        for lbl, val in zip(labels, values):
            bar = '#' * (val // scale)
            print(f"{lbl.rjust(max_label)} | {bar} {val}")

if __name__ == '__main__':
    main()
