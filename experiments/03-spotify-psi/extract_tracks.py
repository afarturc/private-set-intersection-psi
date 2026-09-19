"""
Extract Spotify Track IDs (22-char base62 from Track URI) from a Liked Songs
CSV export and write one ID per line. If --pad-to N is given and the input has
fewer rows, pad the output with fake IDs so both parties end up with the same
element count (the PSI binary requires equal n on both sides).
"""
import argparse
import csv
import secrets
import string

ALPHABET = string.ascii_letters + string.digits  # base62-ish for fake IDs

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pad-to", type=int, default=0)
    args = ap.parse_args()

    ids = []
    seen = set()
    with open(args.inp, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uri = row.get("Track URI", "")
            if not uri.startswith("spotify:track:"):
                continue
            tid = uri.split(":", 2)[2].strip()
            if tid and tid not in seen:
                seen.add(tid)
                ids.append(tid)

    pad = 0
    while args.pad_to and len(ids) < args.pad_to:
        fake = "FAKE" + "".join(secrets.choice(ALPHABET) for _ in range(18))
        if fake not in seen:
            seen.add(fake)
            ids.append(fake)
            pad += 1

    with open(args.out, "w") as out:
        for tid in ids:
            out.write(tid + "\n")
    print(f"Wrote {len(ids)} ids to {args.out} (real: {len(ids)-pad}, padded: {pad})")

if __name__ == "__main__":
    main()
