"""
Plot the PSI benchmark results produced by bench.sh: execution time and total
data exchanged as a function of the set size, one line per protocol.

Usage: python3 plot.py [results.csv]
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

PROTO_NAMES = {0: "Naive hashing", 2: "Diffie-Hellman", 3: "OT-based"}

HERE = Path(__file__).resolve().parent
results = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "results.csv"

data = defaultdict(list)
with results.open() as f:
    for row in csv.DictReader(f):
        p = int(row["protocol"])
        data[p].append((int(row["n"]), float(row["time_s"]),
                        float(row["sent_MB"]), float(row["recv_MB"])))

for p in data:
    data[p].sort()


def plot(value, ylabel, title, filename):
    fig, ax = plt.subplots(figsize=(8, 5))
    for p, rows in data.items():
        ax.plot([r[0] for r in rows], [value(r) for r in rows],
                marker="o", label=PROTO_NAMES[p])
    ax.set_xscale("log")
    ax.set_yscale("symlog", linthresh=0.1)
    ax.set_xlabel("Set size (n)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, which="both", ls=":")
    ax.legend()
    fig.tight_layout()
    fig.savefig(HERE / filename, dpi=150)


plot(lambda r: r[1], "Time (s)",
     "PSI: execution time vs set size", "time_vs_n.png")
plot(lambda r: r[2] + r[3], "Total data exchanged (MB)",
     "PSI: total data exchanged vs set size", "data_vs_n.png")
print(f"Wrote time_vs_n.png and data_vs_n.png to {HERE}")
