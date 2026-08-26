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

def trip_for_track(clip, track_start_sec, trips_in_clip, tolerance=3.0):
    """Which labelled trip does this track belong to? None if no match.

    ONE place decides track-to-trip membership. tune.py, build_events.py and
    anything later all call this, so the odd/even split cannot drift between
    tools (the same principle as one unit-conversion point).

    Tracks begin 0.1-1.8 s AFTER the labelled trip start on every clip
    measured (YOLO needs the person properly in frame), so the window opens
    early by `tolerance` and closes at the labelled end.
    """
    for trip_no, t_start, t_end in trips_in_clip:
        if t_start - tolerance <= track_start_sec <= t_end:
            return trip_no
    return None


def all_trips():
    """Every labelled TRIP, odd and even. DAY 15 ONLY."""
    import csv
    out = {}
    with open("data/trip.csv", newline="") as f:
        r = csv.DictReader(f)
        r.fieldnames = [n.strip() for n in r.fieldnames]
        for row in r:
            t = row["trip"].strip()
            if not t or row["valid"].strip() != "TRIP":
                continue
            out.setdefault(row["clip"].strip(), []).append(
                (int(t), float(row["start_sec"]), float(row["end_sec"])))
    return out
