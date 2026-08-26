"""Tune thresholds against ODD trips ONLY.

Never reads even trips. Never reads results.json (which covers all clips).
Matches detected events to labelled events with a tolerance window, because
tracks start 1-2 s after the labelled trip start on every clip measured.
"""
import json, glob, os, csv, sys
import numpy as np
from speeds import (pixels_to_metres, drop_fragments,
                    find_hesitations, find_uturns, FPS)
import speeds
from odd_only import odd_trips

speeds.H = np.load("homography_camC.npz")["H"]
TOLERANCE = 3.0          # seconds either side counts as a match

def labelled_events():
    """{(clip, trip): [(type, start_sec)]} for ODD trips only."""
    odd = odd_trips()
    trip_clip = {n: c for c, v in odd.items() for n, _, _ in v}
    out = {}
    with open("data/event.csv", newline="") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [n.strip() for n in reader.fieldnames]
        for row in reader:
            trip = int(row["trip"])
            if trip not in trip_clip:
                continue
            key = (trip_clip[trip], trip)
            out.setdefault(key, []).append(
                (row["event_type"].strip(), float(row["start_sec"])))
    return out


def run(max_speed, min_seconds, max_gap, window,
        min_angle, sustain, span_seconds, min_speed):
    """Returns hits, misses, false positives across all ODD trips."""
    odd = odd_trips()
    truth = labelled_events()
    hits = misses = false = 0

    for clip, trips in odd.items():
        path = glob.glob(f"data/output/*{clip}_traj.json")
        if not path:
            print(f"  !! no traj file for {clip}")
            continue
        with open(path[0]) as f:
            tr = drop_fragments(json.load(f))

        for trip_no, t_start, t_end in trips:
            want = truth.get((clip, trip_no), [])
            got = []
            for tid, pts in tr.items():
                w = pixels_to_metres(pts)
                if w[0][1] > 0.5:
                    continue
                track_start = (w[0][2] - 1) / FPS
                if not (t_start - 3 <= track_start <= t_end):
                    continue                       # not this trip's track
                for a, b, d in find_hesitations(w, max_speed=max_speed,
                        min_seconds=min_seconds, max_gap=max_gap, window=window):
                    got.append(("HESITATION", a))
                for t, ang in find_uturns(w, min_angle=min_angle,
                        sustain=sustain, span_seconds=span_seconds,
                        window=window, min_speed=min_speed):
                    got.append(("UTURN", t))

            used = set()
            for wtype, wt in want:
                found = False
                for i, (gtype, gt) in enumerate(got):
                    if i in used or gtype != wtype:
                        continue
                    if abs(gt - wt) <= TOLERANCE:
                        used.add(i); found = True; break
                hits += found
                misses += not found
            false += len(got) - len(used)

    return hits, misses, false


if __name__ == "__main__":
    base = dict(max_speed=0.3, min_seconds=2.0, max_gap=1.0, window=5,
                min_angle=135.0, sustain=1.0, span_seconds=1.5, min_speed=0.15)
    h, m, f = run(**base)
    print(f"BASELINE (definitions.md): {h} hits, {m} misses, {f} false positives")


    for name, values in [("max_speed", (0.25, 0.30, 0.35, 0.40)),
                         ("max_gap", (0.0, 0.5, 1.0, 1.5, 2.0)),
                         ("min_seconds", (1.5, 2.0, 2.5, 3.0)),
                         ("min_angle", (120.0, 135.0, 150.0, 165.0)),
                         ("min_speed", (0.05, 0.10, 0.15, 0.20, 0.25))]:
        print()
        print(f"{name} sweep (one variable, all else fixed):")
        for v in values:
            cfg = dict(base); cfg[name] = v
            h, m, f = run(**cfg)
            flag = "  <- baseline" if v == base[name] else ""
            print(f"  {name}={v:<6} {h:2d} hits  {m:2d} misses  {f:2d} false{flag}")

    print()
    print("candidate combinations:")
    for label, changes in [("baseline", {}),
                           ("gap=0", {"max_gap": 0.0}),
                           ("spd=0.20", {"min_speed": 0.20}),
                           ("gap=0 + spd=0.20", {"max_gap": 0.0, "min_speed": 0.20})]:
        cfg = dict(base); cfg.update(changes)
        h, m, f = run(**cfg)
        p = h / (h + f) if h + f else 0
        r = h / (h + m) if h + m else 0
        print(f"  {label:<20} {h:2d} hits {m:2d} miss {f:2d} false   P={p:.0%} R={r:.0%}")
