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


def main():
    parser = argparse.ArgumentParser(description="Count original hexagrams from many DayanDivination runs")
    parser.add_argument("--trials", type=int, default=10000, help="number of simulations to run")
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


if __name__ == '__main__':
    main()
