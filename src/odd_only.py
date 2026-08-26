"""Which tracks belong to ODD (tuning) trips?
Built from data/trip.csv, the labels, NOT from detector output.
Day 15 validation is meaningless if thresholds were chosen while even trips
were visible."""
import csv

def odd_trips():
    """Returns {clip: [(trip_no, start_sec, end_sec)]} for ODD trips only."""
    out = {}
    with open("data/trip.csv", newline="") as f:
        for row in csv.DictReader(f):
            t = row["trip"].strip()
            if not t or row["valid"].strip() != "TRIP":
                continue
            n = int(t)
            if n % 2 == 0:
                continue
            out.setdefault(row["clip"].strip(), []).append(
                (n, float(row["start_sec"]), float(row["end_sec"])))
    return out

if __name__ == "__main__":
    d = odd_trips()
    total = sum(len(v) for v in d.values())
    for clip in sorted(d, key=lambda c: int(c.replace("clip", ""))):
        print(f"{clip:>7}: {d[clip]}")
    print(f"\n{total} odd trips across {len(d)} clips")