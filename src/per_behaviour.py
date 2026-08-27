"""Precision, recall and F1 SPLIT BY BEHAVIOUR, for ODD, EVEN and ALL.

Rule 22: averages hide events. A single combined score can look survivable
while one of the two detectors is scoring nothing at all.

Same matching rules as tune.py - same TOLERANCE, same type-must-match, same
greedy pairing - so the totals reconcile with validate.py. Reads only.
"""
import json, glob
import numpy as np
from speeds import (pixels_to_metres, drop_fragments,
                    find_hesitations, find_uturns, FPS)
import speeds
from odd_only import odd_trips, even_trips, all_trips
from tune import TOLERANCE, labelled_events
speeds.H = np.load("homography_camC.npz")["H"]

LOCKED = dict(max_speed=0.30, min_seconds=2.00, max_gap=0.00, window=5,
              min_angle=135.0, sustain=1.00, span_seconds=1.50, min_speed=0.20)

def score(trips_fn):
    trips = trips_fn()
    truth = labelled_events(trips_fn)
    tally = {"HESITATION": [0, 0, 0], "UTURN": [0, 0, 0]}   # hits, misses, false
    for clip, tl in trips.items():
        path = glob.glob(f"data/output/*{clip}_traj.json")
        if not path:
            continue
        with open(path[0]) as f:
            tr = drop_fragments(json.load(f))
        for trip_no, t_start, t_end in tl:
            want = truth.get((clip, trip_no), [])
            got = []
            for tid, pts in tr.items():
                w = pixels_to_metres(pts)
                if w[0][1] > 0.5:
                    continue
                if not (t_start - 3 <= (w[0][2] - 1) / FPS <= t_end):
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
            used = set()
            for wtype, wt in want:
                found = False
                for i, (gtype, gt) in enumerate(got):
                    if i in used or gtype != wtype:
                        continue
                    if abs(gt - wt) <= TOLERANCE:
                        used.add(i); found = True; break
                tally[wtype][0 if found else 1] += 1
            for i, (gtype, gt) in enumerate(got):
                if i not in used:
                    tally[gtype][2] += 1
    return tally

def line(name, h, m, f):
    p = h / (h + f) if h + f else 0.0
    r = h / (h + m) if h + m else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    warn = "   <-- SCORED NOTHING" if h == 0 and (m or f) else ""
    print(f"  {name:<12} {h:2d} hits {m:2d} miss {f:2d} false   "
          f"P={p:.0%}  R={r:.0%}  F1={f1:.0%}{warn}")

for label, fn in [("ODD  (tuning)", odd_trips),
                  ("EVEN (HELD-OUT)", even_trips),
                  ("ALL  (context)", all_trips)]:
    t = score(fn)
    print(f"\n{label}")
    th, tm, tf = 0, 0, 0
    for b in ("HESITATION", "UTURN"):
        h, m, f = t[b]
        line(b, h, m, f)
        th, tm, tf = th + h, tm + m, tf + f
    line("COMBINED", th, tm, tf)

print("\nRule 22: averages hide events. Report the split, not just the total.")