import csv
import matplotlib.pyplot as plt
from collections import defaultdict

PROTO_NAMES = {0: "Naive hashing", 2: "Diffie-Hellman", 3: "OT-based"}

data = defaultdict(list)
with open("/home/afartur/Documents/MSI/2S/TRP/ASS2/step_3/results.csv") as f:
    for row in csv.DictReader(f):
        p = int(row["protocol"])
        data[p].append((int(row["n"]), float(row["time_s"]),
                        float(row["sent_MB"]), float(row["recv_MB"])))

for p in data:
    data[p].sort()

fig, ax = plt.subplots(figsize=(8, 5))
for p, rows in data.items():
    ns = [r[0] for r in rows]
    ts = [r[1] for r in rows]
    ax.plot(ns, ts, marker="o", label=PROTO_NAMES[p])
ax.set_xscale("log"); ax.set_yscale("symlog", linthresh=0.1)
ax.set_xlabel("Set size (n)"); ax.set_ylabel("Time (s)")
ax.set_title("PSI: execution time vs set size")
ax.grid(True, which="both", ls=":"); ax.legend()
fig.tight_layout()
fig.savefig("/home/afartur/Documents/MSI/2S/TRP/ASS2/step_3/time_vs_n.png", dpi=150)

fig, ax = plt.subplots(figsize=(8, 5))
for p, rows in data.items():
    ns = [r[0] for r in rows]
    total = [r[2] + r[3] for r in rows]
    ax.plot(ns, total, marker="o", label=PROTO_NAMES[p])
ax.set_xscale("log"); ax.set_yscale("symlog", linthresh=0.1)
ax.set_xlabel("Set size (n)"); ax.set_ylabel("Total data exchanged (MB)")
ax.set_title("PSI: total data exchanged vs set size")
ax.grid(True, which="both", ls=":"); ax.legend()
fig.tight_layout()
fig.savefig("/home/afartur/Documents/MSI/2S/TRP/ASS2/step_3/data_vs_n.png", dpi=150)
print("OK")
