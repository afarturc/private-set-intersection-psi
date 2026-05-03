#!/usr/bin/env bash
set -u
PSI=/home/afartur/PSI
OUT=/home/afartur/Documents/MSI/2S/TRP/ASS2/step_3/results.csv
SIZES=(50 100 500 1000 5000 10000 50000 100000)
PROTOS=(0 2 3)

echo "protocol,n,time_s,sent_MB,recv_MB" > "$OUT"

cd "$PSI"
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
