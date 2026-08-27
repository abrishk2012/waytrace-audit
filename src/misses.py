"""Name every miss and every false positive on the HELD-OUT (even) trips.

Reuses tune.py's matching rules exactly - same TOLERANCE, same type-must-match,
same greedy pairing - so what this prints reconciles with validate.py's counts.
Reads only. Writes nothing. Changes no threshold.
"""
import json, glob, csv
import numpy as np
from speeds import (pixels_to_metres, drop_fragments,
                    find_hesitations, find_uturns, FPS)
import speeds
from odd_only import even_trips
from tune import TOLERANCE, labelled_events
speeds.H = np.load("homography_camC.npz")["H"]

LOCKED = dict(max_speed=0.30, min_seconds=2.00, max_gap=0.00, window=5,
              min_angle=135.0, sustain=1.00, span_seconds=1.50, min_speed=0.20)

even = even_trips()
truth = labelled_events(even_trips)
hits = misses = false = 0

for clip in sorted(even, key=lambda c: int(c.replace("clip", ""))):
    path = glob.glob(f"data/output/*{clip}_traj.json")
    if not path:
        print(f"  !! no traj file for {clip}")
        continue
    with open(path[0]) as f:
        tr = drop_fragments(json.load(f))
    for trip_no, t_start, t_end in even[clip]:
        want = truth.get((clip, trip_no), [])
        got = []
        for tid, pts in tr.items():
            w = pixels_to_metres(pts)
            if w[0][1] > 0.5:
                continue
            track_start = (w[0][2] - 1) / FPS
            if not (t_start - 3 <= track_start <= t_end):
                continue
            for a, b, d in find_hesitations(w, max_speed=LOCKED["max_speed"],
                    min_seconds=LOCKED["min_seconds"],
                    max_gap=LOCKED["max_gap"], window=LOCKED["window"]):
                got.append(("HESITATION", a))
            for t, ang in find_uturns(w, min_angle=LOCKED["min_angle"],
                    sustain=LOCKED["sustain"],
                    span_seconds=LOCKED["span_seconds"],
                    window=LOCKED["window"], min_speed=LOCKED["min_speed"]):
                got.append(("UTURN", t))

        if not want and not got:
            continue
        print(f"\n{clip}  trip {trip_no}  ({t_start:.1f}-{t_end:.1f}s)")
        used = set()
        for wtype, wt in want:
            found = None
            for i, (gtype, gt) in enumerate(got):
                if i in used or gtype != wtype:
                    continue
                if abs(gt - wt) <= TOLERANCE:
                    used.add(i); found = gt; break
            if found is None:
                print(f"   MISS            {wtype:<11} labelled {wt:.1f}s")
                misses += 1
            else:
                print(f"   hit             {wtype:<11} labelled {wt:.1f}s -> {found:.1f}s")
                hits += 1
        for i, (gtype, gt) in enumerate(got):
            if i not in used:
                print(f"   FALSE POSITIVE  {gtype:<11} detected {gt:.1f}s")
                false += 1

print(f"\nEVEN totals: {hits} hits, {misses} misses, {false} false positives")
print("must match validate.py: 5 hits, 4 misses, 3 false positives")