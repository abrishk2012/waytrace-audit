"""Run both detectors over the clips and write an event log.

ODD/EVEN GUARD
--------------
DEFAULT:  processes ODD (tuning) trips only  ->  data/output/results_odd.json
--all:    processes every labelled trip       ->  data/output/results.json

`--all` is for DAY 15 ONLY, and once only. Before Day 15 the held-out (even)
trips are never read, never counted and never displayed. Enforced by code, not
by memory: the guard filters tracks against data/trip.csv before any detector
runs, so no downstream tool can see a held-out trip by accident.

Why it exists: on Day 13 this script processed all 13 clips, so detector output
became visible for even trips. No threshold was ever chosen against them
(tune.py reads odd trips only, by construction), but "never observed" stopped
being true. The guard restores it for everything after Day 13.

Also the handover point between processing and display (the Day 1 decision).
Nothing downstream re-runs YOLO.
"""
import json, glob, os, sys
import numpy as np
from speeds import (pixels_to_metres, drop_fragments,
                    find_hesitations, find_uturns, FPS)
import speeds
from odd_only import odd_trips, all_trips, trip_for_track

MAX_SPEED    = 0.30   # swept 0.25-0.40, unimprovable
MIN_SECONDS  = 2.00   # swept 1.5-3.0, unimprovable
MAX_GAP      = 0.00   # TUNED 1.0 -> 0.0, removed 3 false positives, cost 0 hits
WINDOW       = 5      # locked Day 8
MIN_ANGLE    = 135.0  # swept 120-165, unimprovable
SUSTAIN      = 1.00
SPAN_SECONDS = 1.50
MIN_SPEED    = 0.20   # TUNED 0.15 -> 0.20, removed 2 more false positives

speeds.H = np.load("homography_camC.npz")["H"]

ALL = "--all" in sys.argv
if ALL:
    print("*** --all: processing EVERY trip including HELD-OUT. Day 15 only. ***")


def to_json_safe(v):
    """numpy float32 -> python float, at the ONE point data leaves the maths
    and enters the file. Two float32 crashes on Day 13 came from converting at
    the point of use instead of the point of exit."""
    return float(v)


def position_at(world, t):
    """x, y in metres at time t seconds. Nearest stored point."""
    best, gap_best = world[0], 1e9
    for x, y, fr in world:
        gap = abs((fr - 1) / FPS - t)
        if gap < gap_best:
            best, gap_best = (x, y, fr), gap
    return round(to_json_safe(best[0]), 3), round(to_json_safe(best[1]), 3)


trips_by_clip = all_trips() if ALL else odd_trips()
events = []
seen_trips = []
skipped = 0

clips = sorted(glob.glob("data/output/*_traj.json"))
print(f"{len(clips)} clip files found, "
      f"{sum(len(v) for v in trips_by_clip.values())} trips in scope")

for path in clips:
    clip = os.path.basename(path).split("_")[-2]
    in_scope = trips_by_clip.get(clip, [])
    if not in_scope:
        continue

    with open(path) as f:
        tr = drop_fragments(json.load(f))

    for tid, pts in tr.items():
        w = pixels_to_metres(pts)
        if w[0][1] > 0.5:
            continue
        track_start = (w[0][2] - 1) / FPS
        trip_no = trip_for_track(clip, track_start, in_scope)
        if trip_no is None:
            skipped += 1
            continue
        seen_trips.append((clip, trip_no, tid))

        for a, b, d in find_hesitations(w, max_speed=MAX_SPEED,
                                        min_seconds=MIN_SECONDS,
                                        max_gap=MAX_GAP, window=WINDOW):
            x, y = position_at(w, a)
            events.append({"clip": clip, "trip": trip_no, "track_id": tid,
                           "type": "HESITATION",
                           "start_sec": round(a, 1), "end_sec": round(b, 1),
                           "duration_sec": round(d, 1), "x_m": x, "y_m": y,
                           "confidence": round(min(1.0, d / MIN_SECONDS), 2)})

        for t, ang in find_uturns(w, min_angle=MIN_ANGLE, sustain=SUSTAIN,
                                  span_seconds=SPAN_SECONDS, window=WINDOW,
                                  min_speed=MIN_SPEED):
            x, y = position_at(w, t)
            deg = to_json_safe(ang)
            events.append({"clip": clip, "trip": trip_no, "track_id": tid,
                           "type": "UTURN",
                           "start_sec": round(t, 1), "end_sec": round(t + 1, 1),
                           "duration_sec": 1.0, "x_m": x, "y_m": y,
                           "angle_deg": round(deg, 1),
                           "confidence": round(min(1.0,
                                        (deg - MIN_ANGLE) / 45.0 + 0.5), 2)})

out_path = "data/output/results.json" if ALL else "data/output/results_odd.json"
with open(out_path, "w") as f:
    json.dump({"scope": "ALL_TRIPS" if ALL else "ODD_TRIPS_ONLY",
               "trips_examined": [{"clip": c, "trip": n, "track_id": t}
                                  for c, n, t in sorted(seen_trips)],
               "thresholds": {"max_speed": MAX_SPEED, "min_seconds": MIN_SECONDS,
                              "max_gap": MAX_GAP, "window": WINDOW,
                              "min_angle": MIN_ANGLE, "sustain": SUSTAIN,
                              "span_seconds": SPAN_SECONDS,
                              "min_speed": MIN_SPEED},
               "events": events}, f, indent=2)

h = sum(1 for e in events if e["type"] == "HESITATION")
print(f"\n{len(seen_trips)} trips matched to tracks, "
      f"{skipped} tracks skipped as out of scope")
print(f"{len(events)} events -> {out_path}  ({h} hesitations, "
      f"{len(events) - h} u-turns)")

zero = [t for t in seen_trips
        if not any(e["clip"] == t[0] and e["trip"] == t[1] for e in events)]
print(f"{len(zero)} trips examined with ZERO events "
      f"(on a clean trip, zero is the correct answer - Rule 38)")
