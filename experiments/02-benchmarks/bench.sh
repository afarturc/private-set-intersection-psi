#!/usr/bin/env bash
#
# Benchmarks three PSI protocols (naive hashing, Diffie-Hellman, OT-based)
# over a range of set sizes using the psi.exe binary from the ENCRYPTO PSI
# suite, and writes one CSV row per (protocol, n) measurement.
#
# Usage: PSI_DIR=/path/to/PSI ./bench.sh
set -u

PSI_DIR="${PSI_DIR:-$HOME/PSI}"
OUT="${OUT:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/results.csv}"
SIZES=(50 100 500 1000 5000 10000 50000 100000)
PROTOS=(0 2 3)

if [[ ! -x "$PSI_DIR/psi.exe" ]]; then
  echo "psi.exe not found in $PSI_DIR — set PSI_DIR to your PSI checkout." >&2
  exit 1
fi

echo "protocol,n,time_s,sent_MB,recv_MB" > "$OUT"

cd "$PSI_DIR"
for p in "${PROTOS[@]}"; do
  for n in "${SIZES[@]}"; do
    echo ">> protocol=$p n=$n"
    o0=$(mktemp); o1=$(mktemp)
    ./psi.exe -r 0 -p "$p" -b 16 -n "$n" > "$o0" 2>&1 &
    pid0=$!
    sleep 0.2
    ./psi.exe -r 1 -p "$p" -b 16 -n "$n" > "$o1" 2>&1
    wait "$pid0"
    t=$(grep -oP 'Required time:\s*\K[0-9.]+' "$o1" | tail -1)
    s=$(grep -oP 'Data sent:\s*\K[0-9.]+' "$o1" | tail -1)
    r=$(grep -oP 'Data received:\s*\K[0-9.]+' "$o1" | tail -1)
    echo "$p,$n,$t,$s,$r" >> "$OUT"
    rm -f "$o0" "$o1"
  done
done
echo "Done -> $OUT"
